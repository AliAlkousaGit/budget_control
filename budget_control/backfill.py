"""
budget_control.budget_control.backfill
=========================================
Historical data backfill.

Run from bench console:
    bench --site erp16.golden-link.com execute budget_control.budget_control.backfill.run

This script:
  1. Resets all custom tracking fields on submitted Budget records to 0
  2. Rebuilds Actual Expense from submitted Purchase Invoices
  3. Rebuilds Reserved Against PO from submitted (open) Purchase Orders
  4. Rebuilds Advance Paid from Payment Entries linked to POs
  5. Recalculates Available Budget and Utilisation % on all records

Safe to run multiple times — it resets before recalculating (idempotent).
"""

import frappe
from frappe.utils import flt
from erpnext.accounts.utils import get_fiscal_year


def get_fy_name(date, company):
    try:
        result = get_fiscal_year(date, company=company, as_dict=True)
        return result[0].name if result else None
    except Exception:
        return None


def find_budget_name(company, fy, project, account):
    rows = frappe.db.get_all(
        "Budget",
        filters={
            "company":        company,
            "fiscal_year":    fy,
            "budget_against": "Project",
            "project":        project,
            "account":        account,
            "docstatus":      1,
        },
        pluck="name",
        limit=1,
    )
    return rows[0] if rows else None


def run():
    print("=" * 60)
    print("Budget Control — Historical Backfill Starting")
    print("=" * 60)

    # ── Step 1: Reset ────────────────────────────────────────────
    frappe.db.sql("""
        UPDATE `tabBudget`
        SET
            custom_reserved_po      = 0,
            custom_actual_expense   = 0,
            custom_advance_paid     = 0,
            custom_available_budget = budget_amount,
            custom_utilisation_pct  = 0
        WHERE docstatus = 1
          AND budget_against = 'Project'
    """)
    frappe.db.commit()
    print("Step 1 ✓  Reset all Budget tracking fields to 0")

    # ── Step 2: Actual Expense from submitted Purchase Invoices ──
    pi_items = frappe.db.sql("""
        SELECT
            pi.company,
            pi.posting_date,
            COALESCE(pii.project, pi.project) AS project,
            pii.expense_account,
            SUM(pii.amount) AS total_amount
        FROM `tabPurchase Invoice Item` pii
        INNER JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
        WHERE pi.docstatus = 1
          AND (pii.project IS NOT NULL OR pi.project IS NOT NULL)
          AND pii.expense_account IS NOT NULL
        GROUP BY pi.company, pi.posting_date,
                 COALESCE(pii.project, pi.project),
                 pii.expense_account
    """, as_dict=True)

    count = 0
    for row in pi_items:
        if not row.project:
            continue
        fy = get_fy_name(row.posting_date, row.company)
        if not fy:
            continue
        bname = find_budget_name(row.company, fy, row.project, row.expense_account)
        if bname:
            frappe.db.sql("""
                UPDATE `tabBudget`
                SET custom_actual_expense = custom_actual_expense + %s
                WHERE name = %s
            """, (flt(row.total_amount), bname))
            count += 1

    frappe.db.commit()
    print(f"Step 2 ✓  Actual Expense built from {len(pi_items)} PI line groups ({count} matched budgets)")

    # ── Step 3: Reserved Against PO (open commitments) ──────────
    po_items = frappe.db.sql("""
        SELECT
            po.name          AS po_name,
            po.company,
            po.transaction_date,
            poi.project,
            poi.expense_account,
            poi.amount,
            poi.name         AS poi_name
        FROM `tabPurchase Order Item` poi
        INNER JOIN `tabPurchase Order` po ON po.name = poi.parent
        WHERE po.docstatus = 1
          AND poi.project IS NOT NULL
          AND poi.expense_account IS NOT NULL
    """, as_dict=True)

    count = 0
    for row in po_items:
        fy = get_fy_name(row.transaction_date, row.company)
        if not fy:
            continue

        # Amount already invoiced for this specific PO line
        invoiced = flt(frappe.db.sql("""
            SELECT COALESCE(SUM(pii.amount), 0)
            FROM `tabPurchase Invoice Item` pii
            INNER JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
            WHERE pii.purchase_order = %s
              AND pii.po_detail = %s
              AND pi.docstatus = 1
        """, (row.po_name, row.poi_name))[0][0])

        open_amount = max(0, flt(row.amount) - invoiced)
        if open_amount <= 0:
            continue

        bname = find_budget_name(row.company, fy, row.project, row.expense_account)
        if bname:
            frappe.db.sql("""
                UPDATE `tabBudget`
                SET custom_reserved_po = custom_reserved_po + %s
                WHERE name = %s
            """, (open_amount, bname))
            count += 1

    frappe.db.commit()
    print(f"Step 3 ✓  Reserved Against PO built from {len(po_items)} PO lines ({count} matched budgets)")

    # ── Step 4: Advance Paid from Payment Entries ────────────────
    pe_refs = frappe.db.sql("""
        SELECT
            pe.company,
            per.reference_name   AS po_name,
            per.allocated_amount
        FROM `tabPayment Entry Reference` per
        INNER JOIN `tabPayment Entry` pe ON pe.name = per.parent
        WHERE per.reference_doctype = 'Purchase Order'
          AND pe.docstatus          = 1
          AND pe.payment_type       = 'Pay'
    """, as_dict=True)

    count = 0
    for ref in pe_refs:
        items = frappe.db.get_all(
            "Purchase Order Item",
            filters={"parent": ref.po_name},
            fields=["project", "expense_account", "amount"],
        )
        po_total = sum(flt(i.amount) for i in items)
        if not po_total:
            continue

        po_date = frappe.db.get_value("Purchase Order", ref.po_name, "transaction_date")
        fy = get_fy_name(po_date, ref.company)
        if not fy:
            continue

        for item in items:
            if not item.project or not item.expense_account:
                continue
            share = flt(item.amount) / po_total
            adv   = flt(ref.allocated_amount) * share
            bname = find_budget_name(ref.company, fy, item.project, item.expense_account)
            if bname:
                frappe.db.sql("""
                    UPDATE `tabBudget`
                    SET custom_advance_paid = custom_advance_paid + %s
                    WHERE name = %s
                """, (adv, bname))
                count += 1

    frappe.db.commit()
    print(f"Step 4 ✓  Advance Paid built from {len(pe_refs)} Payment Entry references ({count} matched budgets)")

    # ── Step 5: Final recalc of Available + Utilisation ─────────
    frappe.db.sql("""
        UPDATE `tabBudget`
        SET
            custom_available_budget = budget_amount
                                      - COALESCE(custom_reserved_po, 0)
                                      - COALESCE(custom_actual_expense, 0),
            custom_utilisation_pct  = CASE
                WHEN budget_amount > 0
                THEN (COALESCE(custom_reserved_po, 0) + COALESCE(custom_actual_expense, 0))
                     / budget_amount * 100
                ELSE 0
            END,
            custom_last_recalc      = NOW()
        WHERE docstatus = 1
          AND budget_against = 'Project'
    """)
    frappe.db.commit()
    print("Step 5 ✓  Available Budget and Utilisation % recalculated")

    total = frappe.db.count("Budget", {"docstatus": 1, "budget_against": "Project"})
    print("=" * 60)
    print(f"Backfill COMPLETE — {total} Budget records updated")
    print("=" * 60)
