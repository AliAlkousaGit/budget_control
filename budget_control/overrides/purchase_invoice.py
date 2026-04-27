import frappe
from frappe.utils import flt
from budget_control.utils import (
    is_enabled, find_budget_by_date, recalc_and_save, update_po_budget_status,
)


def after_submit(doc, method=None):
    if not is_enabled():
        return
    if frappe.db.get_value("Purchase Invoice", doc.name, "custom_budget_processed"):
        return

    for item in doc.items:
        project = item.project or doc.project
        if not project or not item.expense_account:
            continue
        bgt = find_budget_by_date(doc.company, project, item.expense_account, doc.posting_date)
        if not bgt:
            continue
        pi_amount    = flt(item.amount)
        new_reserved = max(0, flt(bgt.custom_reserved_po) - pi_amount)
        new_actual   = flt(bgt.custom_actual_expense) + pi_amount
        recalc_and_save(bgt.name, new_reserved, new_actual, flt(bgt.custom_advance_paid))
        if item.purchase_order:
            update_po_budget_status(item.purchase_order)

    frappe.db.set_value("Purchase Invoice", doc.name, "custom_budget_processed", 1)


def after_cancel(doc, method=None):
    if not is_enabled():
        return

    for item in doc.items:
        project = item.project or doc.project
        if not project or not item.expense_account:
            continue
        bgt = find_budget_by_date(doc.company, project, item.expense_account, doc.posting_date)
        if not bgt:
            continue
        pi_amount    = flt(item.amount)
        new_reserved = flt(bgt.custom_reserved_po) + pi_amount
        new_actual   = max(0, flt(bgt.custom_actual_expense) - pi_amount)
        recalc_and_save(bgt.name, new_reserved, new_actual, flt(bgt.custom_advance_paid))
        if item.purchase_order:
            update_po_budget_status(item.purchase_order)

    frappe.db.set_value("Purchase Invoice", doc.name, "custom_budget_processed", 0)
