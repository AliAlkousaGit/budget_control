import frappe
from frappe import _


def get_context(context):
    """Get page context with dashboard HTML."""
    from budget_control.dashboards.budget_control import get_dashboard_html
    project = frappe.form_dict.get('project')
    context.dashboard_html = get_dashboard_html(project)
    context.title = "Budget Control Dashboard"
    return context
