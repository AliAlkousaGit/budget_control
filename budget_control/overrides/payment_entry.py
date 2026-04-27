import frappe
from frappe.utils import flt
from budget_control.utils import is_enabled, find_budget_by_date, recalc_and_save


def after_submit(doc, method=None):
    if not is_enabled() or doc.payment_type != "Pay":
        return
    if frappe.db.get_value("Payment Entry", doc.name, "custom_advance_processed"):
        return

    advance_totals = {}
    for ref in doc.references:
        if ref.reference_doctype != "Purchase Order":
            continue
        po = frappe.get_doc("Purchase Order", ref.reference_name)
        po_total = sum(flt(i.amount) for i in po.items)
        if not po_total:
            continue
        for item in po.items:
            project = item.project or po.project
            if not project or not item.expense_account:
                continue
            share = flt(item.amount) / po_total
            adv   = flt(ref.allocated_amount) * share
            key = (po.company, project, item.expense_account, po.transaction_date)
            advance_totals[key] = advance_totals.get(key, 0) + adv

    for (company, project, account, payment_date), adv in advance_totals.items():
        bgt = find_budget_by_date(company, project, account, payment_date)
        if not bgt:
            continue
        recalc_and_save(
            bgt.name,
            flt(bgt.custom_reserved_po),
            flt(bgt.custom_actual_expense),
            flt(bgt.custom_advance_paid) + adv,
        )

    frappe.db.set_value("Payment Entry", doc.name, "custom_advance_processed", 1)


def after_cancel(doc, method=None):
    if not is_enabled() or doc.payment_type != "Pay":
        return

    advance_totals = {}
    for ref in doc.references:
        if ref.reference_doctype != "Purchase Order":
            continue
        po = frappe.get_doc("Purchase Order", ref.reference_name)
        po_total = sum(flt(i.amount) for i in po.items)
        if not po_total:
            continue
        for item in po.items:
            project = item.project or po.project
            if not project or not item.expense_account:
                continue
            share = flt(item.amount) / po_total
            adv   = flt(ref.allocated_amount) * share
            key = (po.company, project, item.expense_account, po.transaction_date)
            advance_totals[key] = advance_totals.get(key, 0) + adv

    for (company, project, account, payment_date), adv in advance_totals.items():
        bgt = find_budget_by_date(company, project, account, payment_date)
        if not bgt:
            continue
        recalc_and_save(
            bgt.name,
            flt(bgt.custom_reserved_po),
            flt(bgt.custom_actual_expense),
            max(0, flt(bgt.custom_advance_paid) - adv),
        )

    frappe.db.set_value("Payment Entry", doc.name, "custom_advance_processed", 0)
