app_name = "budget_control"
app_title = "Budget Control"
app_publisher = "Golden Link"
app_description = "Budget control for Purchase Orders, Invoices and Payments"
app_email = "admin@golden-link.com"
app_license = "MIT"
app_version = "0.0.1"

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "=", "Budget Control"]]
    }
]

doc_events = {
    "Purchase Order": {
        "before_submit":          "budget_control.overrides.purchase_order.before_submit",
        "after_cancel":           "budget_control.overrides.purchase_order.after_cancel",
        "on_update_after_submit": "budget_control.overrides.purchase_order.on_update_after_submit",
    },
    "Purchase Invoice": {
        "after_submit": "budget_control.overrides.purchase_invoice.after_submit",
        "after_cancel": "budget_control.overrides.purchase_invoice.after_cancel",
    },
    "Payment Entry": {
        "after_submit": "budget_control.overrides.payment_entry.after_submit",
        "after_cancel": "budget_control.overrides.payment_entry.after_cancel",
    },
    "Budget": {
        "before_save": "budget_control.overrides.budget.before_save",
        "on_submit":   "budget_control.overrides.budget.on_submit",
    },
}
