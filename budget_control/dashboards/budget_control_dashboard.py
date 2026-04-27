"""
Budget Control Executive Dashboard
===================================
Provides comprehensive budget visibility with:
  - KPI Summary Cards
  - Health Status Breakdown (Pie Chart)
  - Budget Utilisation Trends
  - Project Comparison (Bar Chart)
  - Critical Alerts
  - Quick Action Links
"""

from frappe import _


def get_dashboard_data():
    """Return dashboard configuration."""
    return {
        "dashboard_name": "Budget Control Dashboard",
        "cards": [
            {
                "card_type": "number",
                "label": _("Total Budget Allocated"),
                "doctype": "Budget",
                "docstatus": 1,
                "func": "budget_control.budget_control.dashboards.budget_control_dashboard.get_total_budget",
                "color": "#667eea"
            },
            {
                "card_type": "number",
                "label": _("Reserved Against POs"),
                "doctype": "Budget",
                "docstatus": 1,
                "func": "budget_control.budget_control.dashboards.budget_control_dashboard.get_total_reserved",
                "color": "#f5576c"
            },
            {
                "card_type": "number",
                "label": _("Actual Expenses"),
                "doctype": "Budget",
                "docstatus": 1,
                "func": "budget_control.budget_control.dashboards.budget_control_dashboard.get_total_actual",
                "color": "#00f2fe"
            },
            {
                "card_type": "number",
                "label": _("Available Budget"),
                "doctype": "Budget",
                "docstatus": 1,
                "func": "budget_control.budget_control.dashboards.budget_control_dashboard.get_total_available",
                "color": "#43e97b"
            },
        ],
        "dashboard_charts": [
            {
                "chart_name": "Budget Health Status",
                "chart_type": "Pie",
                "doctype": "Budget",
                "based_on": "status",
                "positions": "0-3"
            },
            {
                "chart_name": "Budget Utilisation - Top 10",
                "doctype": "Budget",
                "report": "Budget Control Summary",
                "positions": "4-8"
            },
        ],
        "widgets": [
            {
                "type": "shortcut",
                "label": _("Budget Control Report"),
                "icon": "fa fa-bar-chart-o",
                "action": "frappe.ui.form.open_grid_report({doctype: 'Budget', name: 'Budget Control Summary'})",
                "color": "#667eea"
            },
            {
                "type": "shortcut",
                "label": _("Critical Budgets"),
                "icon": "fa fa-exclamation-triangle",
                "action": "frappe.set_route('query-report', 'Budget Control Summary', {status: 'Critical'})",
                "color": "#ff4757"
            },
            {
                "type": "shortcut",
                "label": _("View All Budgets"),
                "icon": "fa fa-list",
                "action": "frappe.set_route('list', 'Budget', {docstatus: 1})",
                "color": "#5e64ff"
            },
            {
                "type": "shortcut",
                "label": _("Create New Budget"),
                "icon": "fa fa-plus-circle",
                "action": "frappe.new_doc('Budget')",
                "color": "#43e97b"
            },
        ]
    }


# KPI Calculation Functions
import frappe
from frappe.utils import flt


def get_total_budget():
    """Get total budget amount across all active budgets."""
    result = frappe.db.sql("""
        SELECT COALESCE(SUM(budget_amount), 0)
        FROM `tabBudget`
        WHERE docstatus = 1 AND budget_against = 'Project'
    """)
    total = flt(result[0][0]) if result else 0
    return format_amount(total)


def get_total_reserved():
    """Get total reserved amount against POs."""
    result = frappe.db.sql("""
        SELECT COALESCE(SUM(custom_reserved_po), 0)
        FROM `tabBudget`
        WHERE docstatus = 1 AND budget_against = 'Project'
    """)
    total = flt(result[0][0]) if result else 0
    return format_amount(total)


def get_total_actual():
    """Get total actual expense recognized."""
    result = frappe.db.sql("""
        SELECT COALESCE(SUM(custom_actual_expense), 0)
        FROM `tabBudget`
        WHERE docstatus = 1 AND budget_against = 'Project'
    """)
    total = flt(result[0][0]) if result else 0
    return format_amount(total)


def get_total_available():
    """Get total available budget."""
    result = frappe.db.sql("""
        SELECT COALESCE(SUM(custom_available_budget), 0)
        FROM `tabBudget`
        WHERE docstatus = 1 AND budget_against = 'Project'
    """)
    total = flt(result[0][0]) if result else 0
    return format_amount(total)


def format_amount(value):
    """Format amount in readable format."""
    value = flt(value)
    if value >= 10000000:
        return f"₹ {value/10000000:.1f}Cr"
    elif value >= 100000:
        return f"₹ {value/100000:.1f}L"
    elif value >= 1000:
        return f"₹ {value/1000:.1f}K"
    else:
        return f"₹ {value:.0f}"
