# Budget Control Reporting Dashboard
## 📊 Complete Presentation Guide

---

## 📋 Table of Contents
1. **Dashboard Overview** - What you're looking at
2. **Step 1: Accessing the Dashboard** - How to get there
3. **Step 2: Understanding the KPI Cards** - Reading the core metrics  
4. **Step 3: Interpreting Budget Health** - Status colors explained
5. **Step 4: Analyzing Utilisation Trends** - Which projects matter most
6. **Step 5: Taking Action** - Responding to alerts
7. **FAQ & Troubleshooting** - Common questions answered

---

## 🎯 Dashboard Overview

The **Budget Control Dashboard** is an executive-level view of your organization's budget health across all projects and expense categories.

**Key Purpose**: 
- Real-time visibility into budget consumption
- Early warning system for budget overruns
- Data-driven decision-making on project spending
- Compliance tracking against approved budgets

**Who Should Use This?**
- ✅ Finance Managers
- ✅ Project Managers  
- ✅ CFO/Controllers
- ✅ Cost Center Heads
- ✅ Procurement Teams

---

## Step 1️⃣ : Accessing the Dashboard

### Method A: Direct URL Navigation
```
https://your-domain.com/app/budget-control-dashboard
```

### Method B: Using the Menu
1. Open your ERPNext home page
2. Click on **Accounting Module** (or use search)
3. Navigate to **Budget Control** section
4. Select **Budget Control Dashboard**

### Method C: Using the Report
1. Go to **Accounting → Purchase Orders → Budget Control Summary**
2. The dashboard link is available in the module section

### ✨ First-Time Setup
On your first visit:
- Dashboard loads automatically for the current company
- Covers the current fiscal year
- Shows all projects with active budgets
- Auto-refreshes every 5 minutes

---

## Step 2️⃣ : Understanding the KPI Cards

The dashboard displays **4 primary Key Performance Indicators (KPIs)** in colored cards:

### 📊 Card 1: Total Budget Allocated (Purple)
```
Label: 📊 Total Budget Allocated
Value: ₹ XXX Cr
Subtitle: Allocated across 45 budgets
```
**What it means:**
- Sum of all approved budget amounts across your organization
- Represents maximum authorized spending
- Includes all active projects in the current fiscal year

**How to interpret:**
- 🟢 Reference point: Compare actual spending against this amount
- Higher number = more total authorization available
- Should remain static unless new budgets are created

---

### 🛒 Card 2: Reserved Against POs (Red)
```
Label: 🛒 Reserved Against Purchase Orders
Value: ₹ XXX Cr  
Subtitle: Open purchase order commitments
```
**What it means:**
- Amount committed through submitted (but not yet invoiced) Purchase Orders
- Shows what you've promised to pay but haven't yet
- Reduces as POs get invoiced

**How to interpret:**
- 🟢 **Healthy**: Reserved < 60% of budget
- 🟡 **Warning**: Reserved 60-80% of budget
- 🔴 **Critical**: Reserved > 80% of budget
- ⛔ **Overbudget**: Reserved > 100% of budget

**Example:**
- Budget: ₹100 Cr
- Reserved: ₹75 Cr
- Meaning: 75 Crore is already committed in POs; only ₹25 Cr remains

---

### 💳 Card 3: Actual Expense (Blue)
```
Label: 💳 Actual Expense
Value: ₹ XXX Cr
Subtitle: Invoiced and recognized expenses
```
**What it means:**
- Amount officially invoiced and recognized as expense
- Based on submitted Purchase Invoices
- Represents cash that will flow out or has flowed out

**How to interpret:**
- 🟢 Actual Expense reduces budget availability immediately
- Can occur before or after payment
- Actual + Reserved = Total committed spend

**Example:**
- If Reserved = ₹75 Cr + Actual = ₹15 Cr = Total Spend = ₹90 Cr

---

### ✅ Card 4: Available Budget (Green)
```
Label: ✅ Available Budget  
Value: ₹ XXX Cr
Subtitle: Remaining allocation buffer
```
**What it means:**
- Budget Amount - (Reserved + Actual)
- Money still available to commit/spend
- Critical for new purchase approvals

**How to interpret:**
- 🟢 **Positive (Green)**: Budget surplus, can approve new purchases
- 🔴 **Zero or Negative**: Budget exhausted, no new commitments
- Used by procurement to approve/reject new POs

**Formula:**
```
Available = Total Budget - Reserved PO - Actual Expense
```

---

## Step 3️⃣ : Interpreting Budget Health Status

### Health Status Breakdown (4 Categories)

#### 🟢 Healthy (0-75% Utilisation)
- **Status**: All good ✅
- **Action**: Continue normal operations
- **Utilisation Range**: 0% to 75% of budget consumed
- **Count**: Number of budgets in healthy state

#### 🟡 Warning (75-95% Utilisation)
- **Status**: Attention needed ⚠️
- **Action**: Monitor spending, plan controls
- **Utilisation Range**: 75% to 95% of budget consumed
- **What to do**:
  - Review pending POs in this category
  - Discuss with project managers
  - Plan for budget amendments if needed

#### 🔴 Critical (95-100% Utilisation)
- **Status**: Action required 🚨
- **Action**: Restrict new purchases
- **Utilisation Range**: 95% to 100% of budget consumed
- **What to do**:
  - Urgent meeting with project owner
  - Review all pending POs
  - Evaluate budget amendment or cost reduction
  - Approve new POs only with CFO sign-off

#### ⛔ Overbudget (>100% Utilisation)
- **Status**: Crisis ❌
- **Action**: Immediate escalation
- **Utilisation Range**: Already spent more than approved
- **What to do**:
  - Immediate CEO/CFO notification
  - Emergency budget review
  - Cost recovery plan
  - Prevent further commitments

---

### Reading the Health Summary Box

```
Health Status Breakdown
🟢 45 Healthy     (62% of budgets - operating normally)
🟡 18 Warning     (25% of budgets - needs monitoring)  
🔴 8  Critical    (11% of budgets - action required)
⛔ 2  Overbudget  (2% of budgets - crisis state)
```

**Quick Interpretation:**
- If most budgets are 🟢: Organization is spending prudently
- If 25%+ are 🟡+🔴+⛔: Systemic overspending issues
- If any ⛔: Immediate escalation needed

---

## Step 4️⃣ : Analyzing Utilisation Trends

### The Utilisation % Metric

**Definition:** 
```
Utilisation % = (Reserved PO + Actual Expense) / Budget Amount × 100
```

**Example Breakdown:**
```
Project: Buildings & Infrastructure
Account: Construction Costs

Budget Amount:        ₹100 Crore
Reserved (Open POs):   ₹60 Crore
Actual (Invoiced):     ₹20 Crore
Available:            ₹20 Crore

Utilisation % = (60 + 20) / 100 × 100 = 80% 
Status: 🟡 Warning
```

### What Different Utilisation Levels Mean

| Utilisation | Budget | Reserved | Actual | Status | Action |
|---|---|---|---|---|---|
| 25% | ₹100Cr | ₹15Cr | ₹10Cr | 🟢 Healthy | Green light for new POs |
| 65% | ₹100Cr | ₹50Cr | ₹15Cr | 🟢 Healthy | Monitor closely |
| 80% | ₹100Cr | ₹60Cr | ₹20Cr | 🟡 Warning | Approval needed |
| 97% | ₹100Cr | ₹70Cr | ₹27Cr | 🔴 Critical | CFO approval only |
| 105% | ₹100Cr | ₹80Cr | ₹30Cr | ⛔ Overbudget | Emergency action |

---

## Step 5️⃣ : Taking Action

### Chart: Top Projects by Utilisation

The dashboard shows your **top 10-12 projects** ranked by how much of their budget they've consumed.

**How to read it:**
- **Left side (Bars)**: Reserved + Actual amounts in ₹
- **Right side (Line)**: Utilisation percentage trend
- **Order**: Highest utilisation first (most concerning)

**When to take action:**
1. 🟡 **Warning projects** → Review PO pipeline with PM
2. 🔴 **Critical projects** → Call urgent meeting
3. ⛔ **Overbudget projects** → CEO escalation

---

### Critical Alerts Section

Shows projects that need immediate attention (>90% utilization).

**Example Alert:**
```
⚠️ CRITICAL ALERTS (3 Issues)

[Alert Bar] | Project A / Consultancy | 96.5%
[Alert Bar] | Project B / Marketing   | 93.2%
[Alert Bar] | Project C / Training    | 91.8%
```

**What to do with each alert:**
1. Click the alert to see full budget details
2. Review all open POs for that project
3. Calculate invoice backlog (POs submitted but not invoiced)
4. Make go/no-go decision for pending approvals

---

### Quick Action Buttons

Located at the bottom of the dashboard:

#### 1. 📊 View Full Report
- Opens the detailed Budget Control Summary Report
- Shows ALL budgets with sortable columns
- Allows filtering and export
- **Use when**: Need detailed analysis or export to Excel

#### 2. 🔴 Critical Only  
- Shows only budgets with >95% utilisation
- Filters to budgets needing immediate action
- **Use when**: In crisis mode or focused escalation

#### 3. ➕ Create Budget
- Opens form to create a new budget
- **Use when**: Adding new projects or cost centers

#### 4. 📑 All Budgets
- Browsable list of all active budgets
- **Use when**: Looking for a specific budget to review

---

## 🎯 Step-by-Step Decision Guide

### Scenario 1: New PO Request Arrives
```
Q: Can we approve this ₹5 Cr PO?

Answer:
1. Check Available Budget card → Is it > ₹5 Cr?
   ✅ YES → Can approve
   ❌ NO → Cannot approve (budget exhausted)

2. If available, check budget health status:
   🟢 Healthy (0-75%) → Auto-approve
   🟡 Warning (75-95%) → Mgr approval needed
   🔴 Critical (95%+) → CFO approval required
   ⛔ Overbudget → Executive decision
```

### Scenario 2: End-of-Month Review
```
Steps:
1. Open dashboard (auto-refreshes data)
2. Check header KPIs for total spend status
3. Review health breakdown:
   - How many in 🔴 + ⛔?
   - Trend vs. last month?
4. Drill into critical budgets
5. Prepare report for steering committee
```

### Scenario 3: Budget Amendment Needed
```
Situation: Project running over budget

Steps:
1. Identify overbudget project in dashboard
2. Click to view full budget details
3. Assess true need:
   - How much additional required?
   - Is it delay/cost inflation/scope change?
4. Prepare business case for CFO
5. Submit amendment request
6. Dashboard auto-updates after approval
```

---

## 📚 FAQ & Troubleshooting

### Q1: When does the dashboard update?
**A:** 
- Auto-refreshes every 5 minutes
- Manual refresh: Click 🔄 Refresh Data button
- Real-time updates when POs/Invoices are submitted

### Q2: Why is my available budget negative?
**A:**
- You're overbudget (Reserved + Actual > Budget Amount)
- Check for:
  - Unbudgeted POs
  - Budget amendment pending approval
  - Invoices for old POs created after budget end date
- **Fix**: Either reduce spend or amend budget

### Q3: Reserved keeps increasing, where's the progress?
**A:**
- Reserved = Open POs not yet invoiced
- As invoices are submitted, Reserved decreases and Actual increases
- **Check**: Are invoices being created for those POs?

### Q4: Why are some status categories empty?
**A:**
- If 🟢 shows "0": All budgets over 75% util (concerning!)
- If 🔴+ ⛔ shows "0": Excellent budget control
- Normal view: Mix across all 4 categories

### Q5: How do I export budget data?
**A:**
1. Click "📊 View Full Report"
2. Use "Export" dropdown (PDF, CSV, Excel)
3. Or copy data to Excel for further analysis

### Q6: Can I see historical budget trends?
**A:**
- Dashboard shows current snapshot
- For trends:
  1. Run report multiple times and compare
  2. Use "Budget Control Summary" with date filters
  3. Contact Finance for detailed historical analysis

### Q7: Why are Advance Paid cards not shown?
**A:**
- Advances are tracked separately (optional feature)
- Included in detailed report card
- Not included in utilisation % calculation

### Q8: Who has access to this dashboard?
**A:**
- Accounting Managers
- Accounts Users
- System Administrators
- Custom roles as configured

---

## 🎓 Training Checklist

For each stakeholder group, ensure they understand:

### For Project Managers
- [ ] How to read their project's utilisation %
- [ ] What "Reserved" vs "Actual" means for their POs
- [ ] When they need to request budget amendment
- [ ] How to access detailed project budget breakdown

### For Finance/Accounting Team
- [ ] How to read all 4 KPI cards
- [ ] Health status categories and thresholds
- [ ] How to drill into critical budgets
- [ ] How to generate reports for CFO
- [ ] Monthly/quarterly reporting process

### For Approvers (Mgrs/CFO)
- [ ] How to make approval decisions based on utilisation
- [ ] Escalation matrix for different budget states
- [ ] How to identify systemic overspending
- [ ] Budget amendment process

### For Executives
- [ ] High-level budget health metric
- [ ] Key risks and critical alerts
- [ ] Questions to ask during reviews
- [ ] When budgets need amendments

---

## 📞 Support & Next Steps

### Getting Help
- **Dashboard Questions**: Contact Finance team
- **Data Accuracy Issues**: Contact Finance/System Admin
- **Access Requests**: Contact System Admin
- **Training**: Schedule session with Finance manager

### Recommended Review Cadence
- **Daily**: Finance controller checks for critical alerts
- **Weekly**: Finance team review and report
- **Monthly**: Full steering committee review
- **Quarterly**: Budget amendment planning

### Integration with Existing Processes
- Dashboard integrates with:
  - ✅ Purchase Order workflow
  - ✅ Purchase Invoice posting
  - ✅ Payment reconciliation
  - ✅ Budget amendment process
  - ✅ Period-end closing

---

## 🚀 Advanced Features (Explained)

### Drill-Down from Dashboard to Details
1. Click any budget or project name
2. Opens full budget record showing:
   - Detailed transaction history
   - All related POs
   - All related Invoices
   - Amendment history

### Report Export Options
- **PDF**: Professional report for printing/sharing
- **CSV**: Import to Excel for custom analysis  
- **Excel**: With formatting and calculations

### Filters in Full Report
- **Company**: View specific company budgets
- **Fiscal Year**: Compare across years
- **Project**: Deep dive into one project
- **Status**: Filter by health status only

---

## 📊 Sample Dashboard Walkthrough

### Scenario: Weekly Review
```
Time: Monday 10:00 AM
Task: Quick budget health check before weekly standup

Steps:
1. Open dashboard
2. Glance at KPI cards:
   Total Budget:    ₹500 Cr ✅
   Reserved (PO):   ₹320 Cr (64%) 🟢
   Actual:          ₹100 Cr
   Available:       ₹80 Cr ✅
   
3. Check Health Summary:
   45 Healthy 🟢 / 18 Warning 🟡 / 8 Critical 🔴 / 2 Overbudget ⛔
   → 3 projects need attention (11% critical rate - acceptable)

4. Review Critical Alerts:
   - Project A: 96% util → Call PM, ask about pending invoices
   - Project B: 94% util → Monitor for next week
   - Project C: 91% util → Reviewing with CFO anyway

5. Action taken:
   - Email to Project A PM: "Please invoice against PO#xxx"
   - Flag Project C for next steering committee
   - Approve 3 pending POs (within budget)
   
Time spent: 5 minutes
Decision quality: 90%
```

---

## 🎯 Success Metrics

Your budget control is working well when:
- ✅ 80%+ budgets in 🟢 Healthy status
- ✅ <5% budgets in 🔴 Critical + ⛔ Overbudget combined
- ✅ No budget stays overbudget for >2 weeks
- ✅ Zero unplanned budget surprises
- ✅ Finance can answer any budget question in <2 min

---

**Last Updated:** April 2026  
**Dashboard Version:** 1.0  
**Training Materials:** Complete
