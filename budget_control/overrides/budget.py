import frappe
from frappe.utils import flt


def before_save(doc, method=None):
    b = flt(doc.budget_amount)
    r = flt(doc.custom_reserved_po)
    a = flt(doc.custom_actual_expense)
    doc.custom_available_budget = b - r - a
    doc.custom_utilisation_pct  = (r + a) / b * 100 if b else 0


def on_submit(doc, method=None):
    pass  # Handled by Server Script budget_on_submit_backfill
