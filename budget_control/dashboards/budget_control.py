"""
Budget Control Dashboard Page
==============================
Simple interactive dashboard for budget monitoring with project filtering.
Path: /app/budget-control-dashboard
"""

from frappe import _
import frappe
from frappe.utils import flt, today, add_days


@frappe.whitelist()
def get_dashboard_data(project=None):
    """Get dashboard data as JSON for AJAX call."""
    try:
        html = get_dashboard_html(project)
        return {
            "html": html,
            "status": "success"
        }
    except Exception as e:
        frappe.log_error(f"Dashboard error: {str(e)}")
        return {
            "html": f"<div style='color: red; padding: 20px;'>Error loading dashboard: {str(e)}</div>",
            "status": "error"
        }


def get_dashboard_html(project=None):
    """Generate simple dashboard HTML content."""

    # Get filter options and data
    projects = get_project_options()
    kpis = get_kpis(project)
    chart_data = get_chart_data(project)

    # Build project filter dropdown
    project_options = '<option value="">All Projects</option>'
    for p in projects:
        selected = ' selected' if project == p['name'] else ''
        project_options += f'<option value="{p["name"]}"{selected}>{p["name"]}</option>'

    html = f"""
    <div class="budget-dashboard">
        <style>
            .budget-dashboard {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background: #f8f9fa;
                padding: 20px;
                min-height: 100vh;
            }}

            .dashboard-header {{
                background: white;
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 24px;
            }}

            .header-title {{
                font-size: 24px;
                font-weight: 700;
                color: #2d3748;
                margin-bottom: 16px;
            }}

            .filter-section {{
                display: flex;
                gap: 16px;
                align-items: center;
                flex-wrap: wrap;
            }}

            .filter-label {{
                font-weight: 600;
                color: #4a5568;
            }}

            .filter-select {{
                padding: 8px 12px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background: white;
                font-size: 14px;
                min-width: 200px;
            }}

            .kpi-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 24px;
            }}

            .kpi-card {{
                background: white;
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                border-left: 4px solid;
                transition: transform 0.2s;
            }}

            .kpi-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 16px rgba(0,0,0,0.12);
            }}

            .kpi-card.budget {{ border-left-color: #667eea; }}
            .kpi-card.reserved {{ border-left-color: #f5576c; }}
            .kpi-card.actual {{ border-left-color: #00f2fe; }}
            .kpi-card.available {{ border-left-color: #43e97b; }}

            .kpi-title {{
                font-size: 14px;
                font-weight: 600;
                color: #718096;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 12px;
            }}

            .kpi-value {{
                font-size: 28px;
                font-weight: 700;
                color: #2d3748;
                margin-bottom: 8px;
            }}

            .kpi-subtitle {{
                font-size: 12px;
                color: #a0aec0;
            }}

            .charts-section {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 20px;
            }}

            .chart-card {{
                background: white;
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }}

            .chart-title {{
                font-size: 18px;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 20px;
            }}

            .chart-placeholder {{
                height: 300px;
                background: #f7fafc;
                border: 2px dashed #e2e8f0;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #a0aec0;
                font-size: 16px;
            }}

            .simple-chart {{
                height: 300px;
                position: relative;
            }}

            .chart-bar {{
                display: flex;
                align-items: end;
                height: 250px;
                margin-top: 20px;
                padding: 0 20px;
                gap: 8px;
            }}

            .bar-container {{
                flex: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 4px;
            }}

            .bar {{
                width: 100%;
                background: #667eea;
                border-radius: 4px 4px 0 0;
                transition: all 0.3s;
                position: relative;
            }}

            .bar.actual {{
                background: #f5576c;
            }}

            .bar.available {{
                background: #43e97b;
            }}

            .bar-label {{
                font-size: 10px;
                color: #718096;
                text-align: center;
                writing-mode: vertical-rl;
                transform: rotate(180deg);
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                max-height: 60px;
            }}

            .bar-value {{
                font-size: 11px;
                font-weight: 600;
                color: #2d3748;
                position: absolute;
                top: -20px;
                left: 50%;
                transform: translateX(-50%);
            }}

            .chart-legend {{
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 16px;
            }}

            .legend-item {{
                display: flex;
                align-items: center;
                gap: 6px;
                font-size: 12px;
                color: #718096;
            }}

            .legend-color {{
                width: 12px;
                height: 12px;
                border-radius: 2px;
            }}

            .status-indicators {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
            }}

            .status-item {{
                display: flex;
                align-items: center;
                padding: 12px;
                background: #f7fafc;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            }}

            .status-icon {{
                font-size: 20px;
                margin-right: 12px;
            }}

            .status-content {{
                flex: 1;
            }}

            .status-count {{
                font-size: 18px;
                font-weight: 700;
                color: #2d3748;
            }}

            .status-label {{
                font-size: 12px;
                color: #718096;
            }}
        </style>

        <div class="dashboard-header">
            <div class="header-title">💰 Budget Control Dashboard</div>
            <div class="filter-section">
                <span class="filter-label">Filter by Project:</span>
                <select class="filter-select" id="project-filter" onchange="filterDashboard()">
                    {project_options}
                </select>
                <button onclick="refreshDashboard()" style="padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 6px; cursor: pointer;">
                    🔄 Refresh
                </button>
            </div>
        </div>

        <div class="kpi-grid">
            <div class="kpi-card budget">
                <div class="kpi-title">📊 Total Budget</div>
                <div class="kpi-value">{kpis['total_budget']}</div>
                <div class="kpi-subtitle">{kpis['budget_count']} budgets</div>
            </div>

            <div class="kpi-card reserved">
                <div class="kpi-title">🛒 Reserved (PO)</div>
                <div class="kpi-value">{kpis['total_reserved']}</div>
                <div class="kpi-subtitle">Purchase orders</div>
            </div>

            <div class="kpi-card actual">
                <div class="kpi-title">💳 Actual Expense</div>
                <div class="kpi-value">{kpis['total_actual']}</div>
                <div class="kpi-subtitle">Invoiced expenses</div>
            </div>

            <div class="kpi-card available">
                <div class="kpi-title">✅ Available Budget</div>
                <div class="kpi-value">{kpis['total_available']}</div>
                <div class="kpi-subtitle">Remaining balance</div>
            </div>
        </div>

        <div class="charts-section">
            <div class="chart-card">
                <div class="chart-title">📈 Budget Status Overview</div>
                <div class="status-indicators">
                    <div class="status-item">
                        <div class="status-icon">🟢</div>
                        <div class="status-content">
                            <div class="status-count">{kpis['healthy_count']}</div>
                            <div class="status-label">Healthy (≤75%)</div>
                        </div>
                    </div>
                    <div class="status-item">
                        <div class="status-icon">🟡</div>
                        <div class="status-content">
                            <div class="status-count">{kpis['warning_count']}</div>
                            <div class="status-label">Warning (75-95%)</div>
                        </div>
                    </div>
                    <div class="status-item">
                        <div class="status-icon">🔴</div>
                        <div class="status-content">
                            <div class="status-count">{kpis['critical_count']}</div>
                            <div class="status-label">Critical (95-100%)</div>
                        </div>
                    </div>
                    <div class="status-item">
                        <div class="status-icon">⛔</div>
                        <div class="status-content">
                            <div class="status-count">{kpis['overbudget_count']}</div>
                            <div class="status-label">Over Budget (>100%)</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="chart-card">
                <div class="chart-title">📊 Budget vs Actual by Project</div>
                {get_simple_chart_html(project)}
            </div>
        </div>

        <script>
            function filterDashboard() {{
                const project = document.getElementById('project-filter').value;
                frappe.call({{
                    method: 'budget_control.dashboards.budget_control.get_dashboard_data',
                    args: {{ project: project }},
                    callback: function(r) {{
                        if (r.message && r.message.status === 'success') {{
                            document.querySelector('.budget-dashboard').innerHTML = r.message.html;
                        }}
                    }}
                }});
            }}

            function refreshDashboard() {{
                filterDashboard();
            }}
        </script>
    </div>
    """
    return html
        
def get_project_options():
    """Get list of projects with budgets."""
    result = frappe.db.sql("""
        SELECT DISTINCT project as name
        FROM `tabBudget`
        WHERE docstatus = 1 AND budget_against = 'Project' AND project IS NOT NULL
        ORDER BY project
    """, as_dict=True)
    return result or []


def get_kpis(project=None):
    """Get KPI data with optional project filter."""
    conditions = ["docstatus = 1", "budget_against = 'Project'"]
    values = {}

    if project:
        conditions.append("project = %(project)s")
        values["project"] = project

    where_clause = " AND ".join(conditions)

    result = frappe.db.sql(f"""
        SELECT
            COALESCE(SUM(budget_amount), 0) as total_budget,
            COALESCE(SUM(custom_reserved_po), 0) as total_reserved,
            COALESCE(SUM(custom_actual_expense), 0) as total_actual,
            COALESCE(SUM(custom_available_budget), 0) as total_available,
            COUNT(*) as budget_count,
            SUM(CASE WHEN custom_utilisation_pct <= 75 THEN 1 ELSE 0 END) as healthy_count,
            SUM(CASE WHEN custom_utilisation_pct > 75 AND custom_utilisation_pct < 95 THEN 1 ELSE 0 END) as warning_count,
            SUM(CASE WHEN custom_utilisation_pct >= 95 AND custom_utilisation_pct <= 100 THEN 1 ELSE 0 END) as critical_count,
            SUM(CASE WHEN custom_utilisation_pct > 100 THEN 1 ELSE 0 END) as overbudget_count
        FROM `tabBudget`
        WHERE {where_clause}
    """, values, as_dict=True)

    data = result[0] if result else {}

    def fmt(val):
        val = flt(val)
        if val >= 10000000:
            return f"₹{val/10000000:.1f}Cr"
        elif val >= 100000:
            return f"₹{val/100000:.1f}L"
        elif val >= 1000:
            return f"₹{val/1000:.1f}K"
        return f"₹{val:.0f}"

    return {
        'total_budget': fmt(data.get('total_budget', 0)),
        'total_reserved': fmt(data.get('total_reserved', 0)),
        'total_actual': fmt(data.get('total_actual', 0)),
        'total_available': fmt(data.get('total_available', 0)),
        'budget_count': int(data.get('budget_count', 0)),
        'healthy_count': int(data.get('healthy_count', 0) or 0),
        'warning_count': int(data.get('warning_count', 0) or 0),
        'critical_count': int(data.get('critical_count', 0) or 0),
        'overbudget_count': int(data.get('overbudget_count', 0) or 0),
    }


def get_chart_data(project=None):
    """Get chart data for visualisation."""
    # This will be used for implementing actual charts later
    return {}


def get_simple_chart_html(project=None):
    """Generate simple bar chart HTML."""
    # Get top 8 projects by budget amount
    conditions = ["docstatus = 1", "budget_against = 'Project'"]
    values = {}

    if project:
        conditions.append("project = %(project)s")
        values["project"] = project

    where_clause = " AND ".join(conditions)

    result = frappe.db.sql(f"""
        SELECT project, budget_amount, custom_actual_expense, custom_available_budget
        FROM `tabBudget`
        WHERE {where_clause}
        ORDER BY budget_amount DESC
        LIMIT 8
    """, values, as_dict=True)

    if not result:
        return '<div class="chart-placeholder">No budget data available</div>'

    # Calculate max value for scaling
    max_budget = max(flt(r['budget_amount']) for r in result)
    max_value = max_budget if max_budget > 0 else 1

    chart_html = '<div class="simple-chart">'
    chart_html += '<div class="chart-bar">'

    for r in result:
        budget = flt(r['budget_amount'])
        actual = flt(r['custom_actual_expense'])
        available = flt(r['custom_available_budget'])

        # Calculate heights as percentage of max
        budget_height = (budget / max_value) * 200
        actual_height = (actual / max_value) * 200
        available_height = (available / max_value) * 200

        project_name = r['project'][:12] + '...' if len(r['project']) > 12 else r['project']

        chart_html += f'''
        <div class="bar-container">
            <div class="bar-value">{format_amount(budget)}</div>
            <div class="bar" style="height: {budget_height}px;"></div>
            <div class="bar actual" style="height: {actual_height}px;"></div>
            <div class="bar available" style="height: {available_height}px;"></div>
            <div class="bar-label" title="{r['project']}">{project_name}</div>
        </div>
        '''

    chart_html += '</div>'
    chart_html += '''
    <div class="chart-legend">
        <div class="legend-item">
            <div class="legend-color" style="background: #667eea;"></div>
            <span>Budget</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #f5576c;"></div>
            <span>Actual</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #43e97b;"></div>
            <span>Available</span>
        </div>
    </div>
    '''
    chart_html += '</div>'

    return chart_html


def format_amount(value):
    """Format amount for display."""
    value = flt(value)
    if value >= 10000000:
        return f"₹{value/10000000:.1f}Cr"
    elif value >= 100000:
        return f"₹{value/100000:.1f}L"
    elif value >= 1000:
        return f"₹{value/1000:.1f}K"
    return f"₹{value:.0f}"
