"""
Budget Control Summary Report
================================
Displays all active Budget records with their tracking metrics:
  - Budget Amount
  - Reserved Against PO
  - Actual Expense
  - Advance Paid
  - Available Budget
  - Utilisation %
  - Status (Healthy / Warning / Critical / Overbudget)

Filters: Company, Fiscal Year, Project, Status
Export: PDF, CSV, Excel
"""

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data    = get_data(filters)
    chart   = get_chart(data)
    # Generate summary message as plain text to avoid rendering issues
    message = get_summary_text(data)
    return columns, data, message, chart


def get_columns():
    return [
        {"label": _("Budget ID"),         "fieldname": "name",                  "fieldtype": "Link",     "options": "Budget",  "width": 160},
        {"label": _("Company"),           "fieldname": "company",               "fieldtype": "Link",     "options": "Company", "width": 140},
        {"label": _("Fiscal Year"),       "fieldname": "fiscal_year",           "fieldtype": "Link",     "options": "Fiscal Year", "width": 110},
        {"label": _("Project"),           "fieldname": "project",               "fieldtype": "Link",     "options": "Project", "width": 160},
        {"label": _("Account"),           "fieldname": "account",               "fieldtype": "Link",     "options": "Account", "width": 200},
        {"label": _("Budget Amount"),     "fieldname": "budget_amount",         "fieldtype": "Currency", "width": 140},
        {"label": _("Reserved (PO)"),     "fieldname": "custom_reserved_po",    "fieldtype": "Currency", "width": 140},
        {"label": _("Actual Expense"),    "fieldname": "custom_actual_expense", "fieldtype": "Currency", "width": 140},
        {"label": _("Advance Paid"),      "fieldname": "custom_advance_paid",   "fieldtype": "Currency", "width": 120},
        {"label": _("Available Budget"),  "fieldname": "custom_available_budget","fieldtype": "Currency", "width": 140},
        {"label": _("Utilisation %"),     "fieldname": "custom_utilisation_pct","fieldtype": "Percent",  "width": 110},
        {"label": _("Status"),            "fieldname": "status",                "fieldtype": "Data",     "width": 110},
    ]


def get_summary_text(data):
    """Generate summary text for the report."""
    if not data:
        return "No budgets found for selected filters."
    
    total_budget   = sum(flt(r.get("budget_amount", 0)) for r in data)
    total_reserved = sum(flt(r.get("custom_reserved_po", 0)) for r in data)
    total_actual   = sum(flt(r.get("custom_actual_expense", 0)) for r in data)
    total_available = sum(flt(r.get("custom_available_budget", 0)) for r in data)
    
    # Count status breakdown
    healthy = sum(1 for r in data if "🟢" in r.get("status", ""))
    warning = sum(1 for r in data if "🟡" in r.get("status", ""))
    critical = sum(1 for r in data if "🔴" in r.get("status", "") and "Overbudget" not in r.get("status", ""))
    overbudget = sum(1 for r in data if "Overbudget" in r.get("status", ""))
    
    text = f"""
Budget Control Summary — {len(data)} Budgets

KPI Summary:
  • Total Budget Allocated:  {format_currency(total_budget)}
  • Reserved Against POs:    {format_currency(total_reserved)}
  • Actual Expense:          {format_currency(total_actual)}
  • Available Budget:        {format_currency(total_available)}

Health Status:
  🟢 Healthy:   {healthy} budgets
  🟡 Warning:   {warning} budgets
  🔴 Critical:  {critical} budgets
  ⛔ Overbudget: {overbudget} budgets
    """
    return text


def format_currency(value):
    """Format value as currency."""
    value = flt(value)
    if value >= 1000000:
        return f"₹ {value/1000000:.2f}M"
    elif value >= 1000:
        return f"₹ {value/1000:.2f}K"
    else:
        return f"₹ {value:.2f}"


def get_data(filters):
    conditions = ["b.docstatus = 1"]
    values     = {}

    if filters.get("company"):
        conditions.append("b.company = %(company)s")
        values["company"] = filters["company"]

    if filters.get("fiscal_year"):
        conditions.append("b.fiscal_year = %(fiscal_year)s")
        values["fiscal_year"] = filters["fiscal_year"]

    if filters.get("budget_against"):
        conditions.append("b.budget_against = %(budget_against)s")
        values["budget_against"] = filters["budget_against"]

    if filters.get("project"):
        conditions.append("b.project = %(project)s")
        values["project"] = filters["project"]

    where = " AND ".join(conditions)

    rows = frappe.db.sql(
        f"""
        SELECT
            b.name,
            b.company,
            b.fiscal_year,
            b.project,
            b.account,
            b.budget_amount,
            COALESCE(b.custom_reserved_po,     0) AS custom_reserved_po,
            COALESCE(b.custom_actual_expense,  0) AS custom_actual_expense,
            COALESCE(b.custom_advance_paid,    0) AS custom_advance_paid,
            COALESCE(b.custom_available_budget, b.budget_amount) AS custom_available_budget,
            COALESCE(b.custom_utilisation_pct, 0) AS custom_utilisation_pct
        FROM `tabBudget` b
        WHERE {where}
        ORDER BY b.custom_utilisation_pct DESC, b.project ASC
        """,
        values,
        as_dict=True,
    )

    for row in rows:
        pct = flt(row.custom_utilisation_pct)
        if pct > 100:
            row["status"] = "🔴 Overbudget"
        elif pct >= 95:
            row["status"] = "🔴 Critical"
        elif pct >= 75:
            row["status"] = "🟡 Warning"
        else:
            row["status"] = "🟢 Healthy"

    # Apply status filter if provided
    if filters.get("status"):
        status_map = {
            "Healthy": "🟢",
            "Warning": "🟡",
            "Critical": "🔴",
            "Overbudget": "Overbudget"
        }
        filter_status = filters["status"]
        rows = [r for r in rows if (
            (filter_status == "Overbudget" and "Overbudget" in r["status"]) or
            (filter_status != "Overbudget" and status_map.get(filter_status, "") in r["status"])
        )]

    return rows


def get_chart(data):
    if not data or len(data) < 2:
        return None

    # Get top 12 budgets by utilisation
    top_data = sorted(data, key=lambda x: flt(x.get("custom_utilisation_pct", 0)), reverse=True)[:12]
    
    labels = [f"{r['project'][:15]}" for r in top_data]
    budget = [flt(r["budget_amount"]) for r in top_data]
    reserved = [flt(r["custom_reserved_po"]) for r in top_data]
    actual = [flt(r["custom_actual_expense"]) for r in top_data]
    available = [flt(r["custom_available_budget"]) for r in top_data]
    utilisation = [flt(r["custom_utilisation_pct"]) for r in top_data]

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": "Reserved (PO)",    "values": reserved, "chartType": "bar"},
                {"name": "Actual Expense",   "values": actual,   "chartType": "bar"},
                {"name": "Available",        "values": available, "chartType": "bar"},
                {"name": "Utilisation %",    "values": utilisation, "chartType": "line"},
            ],
        },
        "type": "mixed",
        "colors": ["#ff9f43", "#1e7d34", "#5e64ff", "#ff4757"],
        "title": "Budget Utilisation Analysis — Top 12 Projects by Spend",
        "barOptions": {"stacked": 1},
    }
