import frappe
from frappe import _
from supplier_portal.api.auth import get_current_supplier_name


@frappe.whitelist()
def get_stock_summary():
    """Get aggregated stock summary for the current supplier."""
    supplier = get_current_supplier_name()

    items = frappe.db.sql("""
        SELECT
            i.name as item_code,
            COALESCE(SUM(b.actual_qty), 0) as total_stock
        FROM `tabItem` i
        LEFT JOIN `tabBin` b ON b.item_code = i.name
        WHERE i.default_supplier = %(supplier)s
        AND i.disabled = 0
        GROUP BY i.name
    """, {"supplier": supplier}, as_dict=True)

    total_items = len(items)
    total_stock = sum(item.total_stock for item in items)
    low_stock = sum(1 for item in items if 0 < item.total_stock < 10)
    out_of_stock = sum(1 for item in items if item.total_stock <= 0)
    in_stock = total_items - low_stock - out_of_stock

    if total_items == 0:
        health = "Unknown"
    elif low_stock == 0 and out_of_stock == 0:
        health = "Healthy"
    elif (low_stock + out_of_stock) < total_items * 0.3:
        health = "Good"
    else:
        health = "Low"

    return {
        "total_items": total_items,
        "total_stock": int(total_stock),
        "in_stock": in_stock,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "health": health,
    }


@frappe.whitelist()
def get_stock_levels(search=None, stock_filter=None, page=1, page_size=20):
    """Get per-item stock levels for the current supplier."""
    supplier = get_current_supplier_name()
    page = int(page)
    page_size = min(int(page_size), 100)
    offset = (page - 1) * page_size

    conditions = ["i.default_supplier = %(supplier)s", "i.disabled = 0"]
    params = {"supplier": supplier, "limit": page_size, "offset": offset}
    having_clause = ""

    if search:
        conditions.append("(i.item_name LIKE %(search)s OR i.item_code LIKE %(search)s)")
        params["search"] = f"%{search}%"

    if stock_filter == "low_stock":
        having_clause = "HAVING total_stock > 0 AND total_stock < 10"
    elif stock_filter == "out_of_stock":
        having_clause = "HAVING total_stock <= 0"
    elif stock_filter == "in_stock":
        having_clause = "HAVING total_stock >= 10"

    where_clause = " AND ".join(conditions)

    items = frappe.db.sql("""
        SELECT
            i.name as item_code,
            i.item_name,
            i.item_group,
            i.image,
            COALESCE(SUM(b.actual_qty), 0) as total_stock,
            COALESCE(SUM(b.reserved_qty), 0) as reserved_qty
        FROM `tabItem` i
        LEFT JOIN `tabBin` b ON b.item_code = i.name
        WHERE {where_clause}
        GROUP BY i.name
        {having_clause}
        ORDER BY total_stock ASC
        LIMIT %(limit)s OFFSET %(offset)s
    """.format(where_clause=where_clause, having_clause=having_clause), params, as_dict=True)

    return {
        "data": [
            {
                "item_code": item.item_code,
                "item_name": item.item_name,
                "item_group": item.item_group,
                "image": item.image,
                "total_stock": int(item.total_stock),
                "reserved_qty": int(item.reserved_qty),
                "available_qty": int(item.total_stock - item.reserved_qty),
                "stock_status": (
                    "out_of_stock" if item.total_stock <= 0
                    else "low_stock" if item.total_stock < 10
                    else "in_stock"
                ),
            }
            for item in items
        ],
        "page": page,
        "page_size": page_size,
    }
