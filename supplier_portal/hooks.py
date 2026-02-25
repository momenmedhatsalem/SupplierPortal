app_name = "supplier_portal"
app_title = "Supplier Portal"
app_publisher = "Justyol"
app_description = "Supplier-facing portal for Justyol"
app_email = "info@justyol.com"
app_license = "MIT"

# Website route rules - serves the Vue SPA for all /suppliers/* routes
website_route_rules = [
    {"from_route": "/suppliers/<path:app_path>", "to_route": "suppliers"},
]

# Guest-accessible methods (no login required)
guest_methods = [
    "supplier_portal.api.auth.register_supplier",
]

# Whitelisted methods
override_whitelisted_methods = {}

# DocType events
doc_events = {}

# Fixtures - export custom fields when doing bench export-fixtures
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in", [
                "Supplier-custom_portal_status",
                "Supplier-custom_portal_registration_date",
                "Supplier-custom_business_description",
                "Supplier-custom_product_categories",
                "Supplier-custom_bank_name",
                "Supplier-custom_bank_iban",
                "Supplier-custom_trade_license",
                "Supplier-custom_tax_certificate",
            ]]
        ]
    }
]
