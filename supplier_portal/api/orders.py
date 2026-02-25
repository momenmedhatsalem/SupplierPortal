import frappe
from frappe import _
from supplier_portal.api.auth import get_current_supplier_name


@frappe.whitelist()
def get_orders(status=None, from_date=None, to_date=None, search=None, page=1, page_size=20):
    """Get paginated orders containing the current supplier's items."""
    supplier = get_current_supplier_name()
    page = int(page)
    page_size = min(int(page_size), 100)
    offset = (page - 1) * page_size

    conditions = ["soi.supplier = %(supplier)s", "so.docstatus = 1"]
    params = {"supplier": supplier, "limit": page_size, "offset": offset}

    if status:
        conditions.append("so.custom_sales_status = %(status)s")
        params["status"] = status

    if from_date:
        conditions.append("so.transaction_date >= %(from_date)s")
        params["from_date"] = from_date

    if to_date:
        conditions.append("so.transaction_date <= %(to_date)s")
        params["to_date"] = to_date

    if search:
        conditions.append("(so.name LIKE %(search)s OR so.customer_name LIKE %(search)s)")
        params["search"] = f"%{search}%"

    where_clause = " AND ".join(conditions)

    # Get orders with item count for this supplier
    orders = frappe.db.sql("""
        SELECT
            so.name,
            so.transaction_date,
            so.customer_name,
            so.grand_total,
            so.currency,
            so.custom_sales_status,
            so.custom_logistics_status,
            so.shopify_order_number,
            COUNT(soi.name) as item_count,
            SUM(soi.amount) as supplier_total
        FROM `tabSales Order` so
        INNER JOIN `tabSales Order Item` soi ON soi.parent = so.name
        WHERE {where_clause}
        GROUP BY so.name
        ORDER BY so.transaction_date DESC, so.creation DESC
        LIMIT %(limit)s OFFSET %(offset)s
    """.format(where_clause=where_clause), params, as_dict=True)

    # Get total count
    total = frappe.db.sql("""
        SELECT COUNT(DISTINCT so.name) as count
        FROM `tabSales Order` so
        INNER JOIN `tabSales Order Item` soi ON soi.parent = so.name
        WHERE {where_clause}
    """.format(where_clause=where_clause), params, as_dict=True)[0].count

    return {
        "data": orders,
        "page": page,
        "page_size": page_size,
        "total": total,
        "has_more": (page * page_size) < total,
    }


@frappe.whitelist()
def get_order_detail(order_name):
    """Get order detail with only the current supplier's line items."""
    supplier = get_current_supplier_name()

    # Validate supplier has items in this order
    has_items = frappe.db.exists(
        "Sales Order Item",
        {"parent": order_name, "supplier": supplier}
    )
    if not has_items:
        frappe.throw(_("Order not found or you don't have access to it."), frappe.PermissionError)

    # Get order header
    order = frappe.db.get_value(
        "Sales Order",
        order_name,
        [
            "name", "transaction_date", "customer_name", "grand_total",
            "currency", "custom_sales_status", "custom_logistics_status",
            "shopify_order_number", "delivery_date"
        ],
        as_dict=True
    )

    if not order:
        frappe.throw(_("Order not found."), frappe.DoesNotExistError)

    # Get only this supplier's items
    items = frappe.db.sql("""
        SELECT
            soi.name,
            soi.item_code,
            soi.item_name,
            soi.custom_sku as sku,
            soi.custom_color as color,
            soi.custom_size as size,
            soi.qty,
            soi.rate,
            soi.amount,
            soi.custom_status as status,
            soi.custom_out_of_stock as out_of_stock,
            soi.image,
            soi.custom_product_image as product_image
        FROM `tabSales Order Item` soi
        WHERE soi.parent = %(order_name)s
        AND soi.supplier = %(supplier)s
        ORDER BY soi.idx
    """, {"order_name": order_name, "supplier": supplier}, as_dict=True)

    order["items"] = items
    order["supplier_total"] = sum(item.amount or 0 for item in items)
    order["supplier_item_count"] = len(items)

    return order


@frappe.whitelist()
def update_item_status(order_name, item_name, new_status):
    """Update a Sales Order Item's custom_status.

    Validates ownership and enforces status transition rules.
    """
    supplier = get_current_supplier_name()

    # Valid status transitions
    valid_transitions = {
        "New Order": ["Preparing", "Cancelled"],
        "Preparing": ["Shipped", "Cancelled"],
        "Shipped": ["Delivered in WH"],
        "Delivered in WH": [],
        "Cancelled": [],
    }

    # Validate item belongs to this supplier and this order
    item = frappe.db.get_value(
        "Sales Order Item",
        {"name": item_name, "parent": order_name, "supplier": supplier},
        ["name", "custom_status"],
        as_dict=True
    )
    if not item:
        frappe.throw(_("Item not found or you don't have access to it."), frappe.PermissionError)

    current_status = item.custom_status or "New Order"

    # Validate transition
    allowed = valid_transitions.get(current_status, [])
    if new_status not in allowed:
        frappe.throw(
            _("Cannot change status from '{0}' to '{1}'. Allowed: {2}").format(
                current_status, new_status, ", ".join(allowed) or "none"
            )
        )

    # Update the status
    frappe.db.set_value("Sales Order Item", item_name, "custom_status", new_status)
    frappe.db.commit()

    return {
        "success": True,
        "message": _("Status updated to {0}").format(new_status),
        "item_name": item_name,
        "new_status": new_status,
    }
