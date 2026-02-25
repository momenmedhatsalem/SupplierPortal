import frappe
from frappe import _


def get_current_supplier_name():
    """Get the Supplier name linked to the current logged-in user via portal_users."""
    user = frappe.session.user
    if not user or user == "Guest":
        frappe.throw(_("Please log in to access the supplier portal"), frappe.AuthenticationError)

    supplier = frappe.db.get_value(
        "Portal User",
        {"user": user, "parenttype": "Supplier"},
        "parent"
    )
    if not supplier:
        frappe.throw(_("Your account is not linked to any supplier"), frappe.PermissionError)

    return supplier


@frappe.whitelist(allow_guest=True)
def register_supplier(
    email,
    password,
    company_name,
    contact_name,
    phone,
    country,
    business_description=None,
    product_categories=None,
):
    """Register a new supplier via the portal.

    Creates a Website User, a Supplier document, and links them via portal_users.
    """
    # Validate email not already registered
    if frappe.db.exists("User", email):
        frappe.throw(_("An account with this email already exists. Please log in instead."))

    # Validate required fields
    if not email or not password or not company_name or not contact_name:
        frappe.throw(_("Email, password, company name, and contact name are required."))

    if len(password) < 8:
        frappe.throw(_("Password must be at least 8 characters long."))

    # Check if supplier name already exists
    if frappe.db.exists("Supplier", company_name):
        frappe.throw(_("A supplier with this company name already exists. Please contact support."))

    try:
        # 1. Create User (Website User)
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": contact_name,
            "user_type": "Website User",
            "send_welcome_email": 0,
        })
        user.append("roles", {"role": "Suppliers"})
        user.insert(ignore_permissions=True)

        # Set password
        from frappe.utils.password import update_password
        update_password(email, password)

        # 2. Create Supplier document
        supplier = frappe.get_doc({
            "doctype": "Supplier",
            "supplier_name": company_name,
            "supplier_type": "Company",
            "country": country,
            "custom_portal_status": "Pending Approval",
            "custom_portal_registration_date": frappe.utils.today(),
            "custom_business_description": business_description or "",
            "custom_product_categories": product_categories or "",
        })
        supplier.append("portal_users", {"user": email})
        supplier.insert(ignore_permissions=True)

        # 3. Create Contact linked to Supplier
        contact = frappe.get_doc({
            "doctype": "Contact",
            "first_name": contact_name,
            "email_ids": [{"email_id": email, "is_primary": 1}],
            "phone_nos": [{"phone": phone, "is_primary_phone": 1}] if phone else [],
        })
        contact.append("links", {
            "link_doctype": "Supplier",
            "link_name": supplier.name,
        })
        contact.insert(ignore_permissions=True)

        frappe.db.commit()

        return {
            "success": True,
            "message": _("Registration successful! Your account is pending approval."),
            "supplier": supplier.name,
        }

    except frappe.exceptions.ValidationError:
        raise
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Supplier registration failed for {email}: {str(e)}")
        frappe.throw(_("Registration failed. Please try again or contact support."))


@frappe.whitelist()
def get_current_supplier():
    """Get the supplier profile for the currently logged-in user."""
    supplier_name = get_current_supplier_name()

    supplier = frappe.get_doc("Supplier", supplier_name)

    # Get primary contact info
    contact_name = supplier.supplier_primary_contact
    contact_data = {}
    if contact_name:
        contact = frappe.get_doc("Contact", contact_name)
        contact_data = {
            "contact_name": contact.first_name,
            "email": contact.email_id,
            "phone": contact.mobile_no or contact.phone,
        }

    # Get address
    address_data = {}
    if supplier.supplier_primary_address:
        address = frappe.get_doc("Address", supplier.supplier_primary_address)
        address_data = {
            "address_line1": address.address_line1,
            "address_line2": address.address_line2,
            "city": address.city,
            "state": address.state,
            "country": address.country,
            "pincode": address.pincode,
        }

    return {
        "name": supplier.name,
        "supplier_name": supplier.supplier_name,
        "country": supplier.country,
        "portal_status": supplier.custom_portal_status,
        "registration_date": str(supplier.custom_portal_registration_date or ""),
        "business_description": supplier.custom_business_description or "",
        "product_categories": supplier.custom_product_categories or "",
        "bank_name": supplier.custom_bank_name or "",
        "bank_iban": supplier.custom_bank_iban or "",
        "tax_id": supplier.tax_id or "",
        "website": supplier.website or "",
        "contact": contact_data,
        "address": address_data,
    }


@frappe.whitelist()
def update_supplier_profile(data):
    """Update supplier profile fields."""
    import json
    if isinstance(data, str):
        data = json.loads(data)

    supplier_name = get_current_supplier_name()
    supplier = frappe.get_doc("Supplier", supplier_name)

    # Only allow updating specific fields
    allowed_fields = [
        "custom_business_description",
        "custom_product_categories",
        "custom_bank_name",
        "custom_bank_iban",
        "website",
    ]

    for field in allowed_fields:
        if field in data:
            supplier.set(field, data[field])

    supplier.save(ignore_permissions=True)
    frappe.db.commit()

    return {"success": True, "message": _("Profile updated successfully.")}
