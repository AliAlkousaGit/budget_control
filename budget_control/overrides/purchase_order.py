import frappe
from frappe.utils import flt
from budget_control.utils import (
    is_enabled, get_settings, find_budget_by_date,
    recalc_and_save, get_po_commitments,
)


def before_submit(doc, method=None):
    if not is_enabled():
        return

    settings = get_settings()
    warn_pct = flt(settings.warn_threshold_pct or 80)
    action   = settings.control_action or "Stop"

    commitments = get_po_commitments(doc)
    if not commitments:
        return

    total_committed = 0
    messages = []

    for (project, account), po_amount in commitments.items():
        bgt = find_budget_by_date(doc.company, project, account, doc.transaction_date)
        if not bgt:
            continue

        budget_amt = flt(bgt.budget_amount)
        reserved   = flt(bgt.custom_reserved_po)
        actual     = flt(bgt.custom_actual_expense)
        advance    = flt(bgt.custom_advance_paid)
        available  = budget_amt - reserved - actual
        new_util   = (reserved + actual + po_amount) / budget_amt * 100 if budget_amt else 0

        if available < po_amount:
            msg = (
                f"<b>Insufficient Budget</b><br>"
                f"Project: <b>{project}</b> | Account: <b>{account}</b><br>"
                f"Available: <b>{frappe.format_value(available, {'fieldtype':'Currency'})}</b> | "
                f"This PO needs: <b>{frappe.format_value(po_amount, {'fieldtype':'Currency'})}</b>"
            )
            if action == "Stop":
                frappe.throw(msg, title="Budget Control — Stopped")
            else:
                messages.append(("red", msg))
                doc.custom_budget_warning = 1
        elif new_util >= warn_pct:
            messages.append(("orange",
                f"Budget Warning: Utilisation will reach <b>{new_util:.1f}%</b> "
                f"for Project <b>{project}</b> / Account <b>{account}</b>."
            ))
            doc.custom_budget_warning = 1

        recalc_and_save(bgt.name, reserved + po_amount, actual, advance)
        total_committed += po_amount

    for indicator, msg in messages:
        frappe.msgprint(msg, alert=True, indicator=indicator)

    frappe.db.set_value("Purchase Order", doc.name, {
        "custom_budget_status":    "Reserved",
        "custom_committed_amount": total_committed,
    })


def after_cancel(doc, method=None):
    if not is_enabled():
        return

    budget_groups = {}
    for item in doc.items:
        project = item.project or doc.project
        if not project or not item.expense_account:
            continue

        key = (project, item.expense_account)
        budget_groups.setdefault(key, 0)
        budget_groups[key] += flt(item.amount)

    for (project, account), po_amount in budget_groups.items():
        bgt = find_budget_by_date(doc.company, project, account, doc.transaction_date)
        if not bgt:
            continue

        invoiced = flt(frappe.db.sql("""
            SELECT COALESCE(SUM(pii.amount), 0)
            FROM `tabPurchase Invoice Item` pii
            JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
            WHERE pii.purchase_order = %s
              AND pii.expense_account = %s
              AND pi.docstatus = 1
        """, (doc.name, account))[0][0])

        open_amount  = max(0, po_amount - invoiced)
        new_reserved = max(0, flt(bgt.custom_reserved_po) - open_amount)

        recalc_and_save(
            bgt.name,
            new_reserved,
            flt(bgt.custom_actual_expense),
            flt(bgt.custom_advance_paid),
        )

    frappe.db.set_value("Purchase Order", doc.name, "custom_budget_status", "Cancelled")


def on_update_after_submit(doc, method=None):
    """
    Catches workflow-based cancellation (Rejected state = docstatus 2).
    Fires when PO is updated after submit — detects docstatus=2 and releases budget.
    """
    if not is_enabled():
        return
    if doc.docstatus != 2:
        return
    if doc.custom_budget_status == "Cancelled":
        return  # Already processed

    after_cancel(doc, method)
