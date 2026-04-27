import frappe
from frappe.utils import flt, now


def is_enabled():
    try:
        result = frappe.db.sql(
            "SELECT enable_budget_control FROM `tabBudget Control Settings` LIMIT 1"
        )
        return bool(result[0][0]) if result else True
    except Exception:
        return True


def get_settings():
    try:
        result = frappe.db.sql(
            "SELECT enable_budget_control, control_action, warn_threshold_pct "
            "FROM `tabBudget Control Settings` LIMIT 1",
            as_dict=True
        )
        if result:
            return result[0]
    except Exception:
        pass
    return frappe._dict(enable_budget_control=1, control_action="Stop", warn_threshold_pct=80)


def find_budget_by_date(company, project, account, date):
    if not all([company, project, account, date]):
        return None
    rows = frappe.db.sql("""
        SELECT name, budget_amount,
               COALESCE(custom_reserved_po,0)      AS custom_reserved_po,
               COALESCE(custom_actual_expense,0)   AS custom_actual_expense,
               COALESCE(custom_advance_paid,0)     AS custom_advance_paid,
               COALESCE(custom_available_budget,0) AS custom_available_budget,
               COALESCE(custom_utilisation_pct,0)  AS custom_utilisation_pct
        FROM `tabBudget`
        WHERE docstatus = 1
          AND budget_against = 'Project'
          AND company = %s
          AND project = %s
          AND account = %s
          AND budget_start_date <= %s
          AND budget_end_date   >= %s
        LIMIT 1
    """, (company, project, account, date, date), as_dict=True)
    return rows[0] if rows else None


def save_budget(budget_name, data):
    """Save fields on a submitted Budget using docstatus trick."""
    frappe.db.set_value("Budget", budget_name, "docstatus", 0, update_modified=False)
    frappe.db.set_value("Budget", budget_name, data, update_modified=False)
    frappe.db.set_value("Budget", budget_name, "docstatus", 1, update_modified=False)


def recalc_and_save(budget_name, reserved, actual, advance=None):
    """Recalculate available/utilisation and save all fields."""
    b = flt(frappe.db.get_value("Budget", budget_name, "budget_amount"))
    if advance is None:
        advance = flt(frappe.db.get_value("Budget", budget_name, "custom_advance_paid"))
    available = b - reserved - actual
    util = (reserved + actual) / b * 100 if b else 0
    save_budget(budget_name, {
        "custom_reserved_po":      reserved,
        "custom_actual_expense":   actual,
        "custom_advance_paid":     advance,
        "custom_available_budget": available,
        "custom_utilisation_pct":  util,
        "custom_last_recalc":      now(),
    })


def update_po_budget_status(po_name):
    po_total = flt(frappe.db.sql(
        "SELECT COALESCE(SUM(amount),0) FROM `tabPurchase Order Item` WHERE parent=%s",
        po_name)[0][0])
    inv_total = flt(frappe.db.sql("""
        SELECT COALESCE(SUM(pii.amount),0)
        FROM `tabPurchase Invoice Item` pii
        JOIN `tabPurchase Invoice` pi ON pi.name=pii.parent
        WHERE pii.purchase_order=%s AND pi.docstatus=1
    """, po_name)[0][0])
    status = "Fully Invoiced" if inv_total >= po_total else "Partially Invoiced"
    frappe.db.set_value("Purchase Order", po_name, "custom_budget_status", status)


def get_po_commitments(doc):
    commitments = {}
    for item in doc.items:
        project = item.project or doc.project
        if not project or not item.expense_account:
            continue
        key = (project, item.expense_account)
        commitments[key] = commitments.get(key, 0) + flt(item.amount)
    return commitments
