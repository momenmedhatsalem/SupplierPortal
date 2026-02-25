import frappe
from frappe import _
from datetime import datetime, timedelta
from supplier_portal.api.auth import get_current_supplier_name


def calculate_rating(confirmation_rate, cancellation_rate, shipment_rate, stock_health):
    """Calculate overall performance rating (0-5 scale).

    Reuses the algorithm from supplier_performance_report.py:229-257.
    Weights: 30% confirmation + 30% cancellation (inverted) + 20% shipment + 20% stock.
    """
    score = 0
    score += (confirmation_rate / 100) * 1.5       # 30% weight, max 1.5
    score += ((100 - cancellation_rate) / 100) * 1.5  # 30% weight, max 1.5
    score += (shipment_rate / 100) * 1.0            # 20% weight, max 1.0

    stock_scores = {"Healthy": 1.0, "Good": 0.7, "Low": 0.3}
    score += stock_scores.get(stock_health, 0.5) * 1.0  # 20% weight, max 1.0

    return min(5.0, max(0.0, round(score, 1)))


def generate_recommendation(rating):
    """Generate recommendation based on rating.

    Reuses logic from supplier_performance_report.py:259-274.
    """
    if rating >= 4.5:
        return {"level": "excellent", "text": "Top Performer - Strategic Partner"}
    elif rating >= 3.5:
        return {"level": "good", "text": "Good Performance - Maintain Relationship"}
    elif rating >= 2.5:
        return {"level": "average", "text": "Average - Monitor Closely"}
    elif rating >= 1.5:
        return {"level": "below_average", "text": "Below Average - Performance Review Needed"}
    else:
        return {"level": "critical", "text": "Critical - Immediate Action Required"}


@frappe.whitelist()
def get_performance(from_date=None, to_date=None):
    """Get performance KPIs, rating, and recommendation for the current supplier."""
    supplier = get_current_supplier_name()

    if not from_date:
        from_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    if not to_date:
        to_date = datetime.now().strftime("%Y-%m-%d")

    # Get order status counts
    status_counts = frappe.db.sql("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN soi.custom_status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
            SUM(CASE WHEN soi.custom_status IN ('Shipped', 'Delivered in WH') THEN 1 ELSE 0 END) as shipped,
            SUM(CASE WHEN soi.custom_status != 'New Order' AND soi.custom_status != 'Cancelled' THEN 1 ELSE 0 END) as confirmed,
            SUM(soi.amount) as total_revenue,
            AVG(soi.amount) as avg_order_value
        FROM `tabSales Order Item` soi
        INNER JOIN `tabSales Order` so ON so.name = soi.parent
        WHERE soi.supplier = %(supplier)s
        AND so.transaction_date BETWEEN %(from_date)s AND %(to_date)s
        AND so.docstatus = 1
    """, {"supplier": supplier, "from_date": from_date, "to_date": to_date}, as_dict=True)[0]

    total = status_counts.total or 0
    cancelled = status_counts.cancelled or 0
    shipped = status_counts.shipped or 0
    confirmed = status_counts.confirmed or 0

    confirmation_rate = (confirmed / total * 100) if total > 0 else 0
    cancellation_rate = (cancelled / total * 100) if total > 0 else 0
    shipment_rate = (shipped / total * 100) if total > 0 else 0

    # Get stock health
    stock_data = get_stock_health(supplier)

    # Calculate rating and recommendation
    rating = calculate_rating(confirmation_rate, cancellation_rate, shipment_rate, stock_data["health"])
    recommendation = generate_recommendation(rating)

    return {
        "kpis": {
            "total_orders": total,
            "confirmed_orders": confirmed,
            "cancelled_orders": cancelled,
            "shipped_orders": shipped,
            "confirmation_rate": round(confirmation_rate, 1),
            "cancellation_rate": round(cancellation_rate, 1),
            "shipment_rate": round(shipment_rate, 1),
            "total_revenue": float(status_counts.total_revenue or 0),
            "avg_order_value": float(status_counts.avg_order_value or 0),
        },
        "stock": stock_data,
        "rating": rating,
        "recommendation": recommendation,
        "period": {"from_date": from_date, "to_date": to_date},
    }


def get_stock_health(supplier):
    """Calculate stock health for a supplier's items."""
    items = frappe.db.sql("""
        SELECT
            i.name as item_code,
            i.item_name,
            COALESCE(SUM(b.actual_qty), 0) as total_stock
        FROM `tabItem` i
        LEFT JOIN `tabBin` b ON b.item_code = i.name
        WHERE i.default_supplier = %(supplier)s
        AND i.disabled = 0
        GROUP BY i.name
    """, {"supplier": supplier}, as_dict=True)

    total_items = len(items)
    total_stock = sum(item.total_stock for item in items)
    low_stock = sum(1 for item in items if item.total_stock < 10)
    out_of_stock = sum(1 for item in items if item.total_stock <= 0)

    if total_items == 0:
        health = "Unknown"
    elif low_stock == 0:
        health = "Healthy"
    elif low_stock < total_items * 0.3:
        health = "Good"
    else:
        health = "Low"

    return {
        "total_items": total_items,
        "total_stock": int(total_stock),
        "low_stock_count": low_stock,
        "out_of_stock_count": out_of_stock,
        "health": health,
    }


@frappe.whitelist()
def get_trends(from_date=None, to_date=None):
    """Get trend data for charts (monthly order volume, revenue, status distribution)."""
    supplier = get_current_supplier_name()

    if not from_date:
        from_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if not to_date:
        to_date = datetime.now().strftime("%Y-%m-%d")

    # Monthly order volume and revenue
    monthly = frappe.db.sql("""
        SELECT
            DATE_FORMAT(so.transaction_date, '%%Y-%%m') as month,
            COUNT(*) as order_count,
            SUM(soi.amount) as revenue
        FROM `tabSales Order Item` soi
        INNER JOIN `tabSales Order` so ON so.name = soi.parent
        WHERE soi.supplier = %(supplier)s
        AND so.transaction_date BETWEEN %(from_date)s AND %(to_date)s
        AND so.docstatus = 1
        GROUP BY DATE_FORMAT(so.transaction_date, '%%Y-%%m')
        ORDER BY month
    """, {"supplier": supplier, "from_date": from_date, "to_date": to_date}, as_dict=True)

    # Status distribution (current snapshot, not date-filtered)
    status_distribution = frappe.db.sql("""
        SELECT
            COALESCE(soi.custom_status, 'New Order') as status,
            COUNT(*) as count
        FROM `tabSales Order Item` soi
        INNER JOIN `tabSales Order` so ON so.name = soi.parent
        WHERE soi.supplier = %(supplier)s
        AND so.docstatus = 1
        AND so.transaction_date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY soi.custom_status
    """, {"supplier": supplier, "from_date": from_date, "to_date": to_date}, as_dict=True)

    return {
        "monthly": [
            {"month": row.month, "order_count": row.order_count, "revenue": float(row.revenue or 0)}
            for row in monthly
        ],
        "status_distribution": [
            {"status": row.status, "count": row.count}
            for row in status_distribution
        ],
    }
