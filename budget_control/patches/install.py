"""
budget_control.patches.install.after_install
=============================================
Runs once after the app is installed.
Creates the Budget Control Settings singleton if it does not exist.
Does NOT run the historical backfill automatically — that must be
triggered manually from Budget Control Settings > Backfill button.
"""

import frappe


def execute():
    # Create the singleton settings record if it doesn't exist
    if not frappe.db.exists("Budget Control Settings", "Budget Control Settings"):
        doc = frappe.new_doc("Budget Control Settings")
        doc.enable_budget_control = 1
        doc.warn_threshold_pct    = 80
        doc.control_action        = "Stop"
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Budget Control Settings created.")
    else:
        print("Budget Control Settings already exists — skipped.")
