import frappe
from frappe import _
from supplier_portal.api.auth import get_current_supplier_name


@frappe.whitelist()
def get_products(search=None, page=1, page_size=20):
    """Get paginated product list for the current supplier with stock data."""
    supplier = get_current_supplier_name()
    page = int(page)
    page_size = min(int(page_size), 100)
    offset = (page - 1) * page_size

    conditions = ["i.default_supplier = %(supplier)s", "i.disabled = 0"]
    params = {"supplier": supplier, "limit": page_size, "offset": offset}

    if search:
        conditions.append("(i.item_name LIKE %(search)s OR i.item_code LIKE %(search)s)")
        params["search"] = f"%{search}%"

    where_clause = " AND ".join(conditions)

    products = frappe.db.sql("""
        SELECT
            i.name as item_code,
            i.item_name,
            i.item_group,
            i.image,
            i.standard_rate,
            COALESCE(SUM(b.actual_qty), 0) as stock_qty
        FROM `tabItem` i
        LEFT JOIN `tabBin` b ON b.item_code = i.name
        WHERE {where_clause}
        GROUP BY i.name
        ORDER BY i.item_name
        LIMIT %(limit)s OFFSET %(offset)s
    """.format(where_clause=where_clause), params, as_dict=True)

    # Get total count
    total = frappe.db.sql("""
        SELECT COUNT(*) as count
        FROM `tabItem` i
        WHERE {where_clause}
    """.format(where_clause=where_clause), params, as_dict=True)[0].count

    return {
        "data": [
            {
                **product,
                "stock_qty": int(product.stock_qty),
                "stock_status": (
                    "out_of_stock" if product.stock_qty <= 0
                    else "low_stock" if product.stock_qty < 10
                    else "in_stock"
                ),
            }
            for product in products
        ],
        "page": page,
        "page_size": page_size,
        "total": total,
        "has_more": (page * page_size) < total,
    }


@frappe.whitelist()
def get_product_detail(item_code):
    """Get detailed product information with stock and variant data."""
    supplier = get_current_supplier_name()

    # Validate ownership
    owner = frappe.db.get_value("Item", item_code, "default_supplier")
    if owner != supplier:
        frappe.throw(_("Product not found or you don't have access to it."), frappe.PermissionError)

    item = frappe.get_doc("Item", item_code)

    # Get stock by warehouse
    stock_data = frappe.db.sql("""
        SELECT warehouse, actual_qty, reserved_qty
        FROM `tabBin`
        WHERE item_code = %(item_code)s AND actual_qty != 0
    """, {"item_code": item_code}, as_dict=True)

    total_stock = sum(row.actual_qty for row in stock_data)

    # Get variants if this is a template item
    variants = []
    if item.has_variants:
        variants = frappe.db.sql("""
            SELECT
                i.name as item_code,
                i.item_name,
                i.image,
                COALESCE(SUM(b.actual_qty), 0) as stock_qty
            FROM `tabItem` i
            LEFT JOIN `tabBin` b ON b.item_code = i.name
            WHERE i.variant_of = %(item_code)s
            AND i.disabled = 0
            GROUP BY i.name
        """, {"item_code": item_code}, as_dict=True)

    return {
        "item_code": item.name,
        "item_name": item.item_name,
        "item_group": item.item_group,
        "description": item.description,
        "image": item.image,
        "standard_rate": float(item.standard_rate or 0),
        "stock_uom": item.stock_uom,
        "has_variants": item.has_variants,
        "variant_of": item.variant_of,
        "total_stock": int(total_stock),
        "stock_by_warehouse": [
            {
                "warehouse": row.warehouse,
                "qty": int(row.actual_qty),
                "reserved": int(row.reserved_qty or 0),
            }
            for row in stock_data
        ],
        "variants": [
            {
                "item_code": v.item_code,
                "item_name": v.item_name,
                "image": v.image,
                "stock_qty": int(v.stock_qty),
            }
            for v in variants
        ],
    }


@frappe.whitelist()
def update_product(item_code, data):
    """Update allowed product fields (validates ownership)."""
    import json
    if isinstance(data, str):
        data = json.loads(data)

    supplier = get_current_supplier_name()

    owner = frappe.db.get_value("Item", item_code, "default_supplier")
    if owner != supplier:
        frappe.throw(_("Product not found or you don't have access to it."), frappe.PermissionError)

    item = frappe.get_doc("Item", item_code)

    # Only allow updating specific fields
    allowed_fields = ["item_name", "description", "standard_rate", "image"]
    for field in allowed_fields:
        if field in data:
            item.set(field, data[field])

    item.save(ignore_permissions=True)
    frappe.db.commit()

    return {"success": True, "message": _("Product updated successfully.")}
