"""
reports.py
Generates a simple text-based monthly summary report and saves it to disk.
"""

import os
from datetime import datetime

from analysis import get_totals, get_category_breakdown, get_monthly_expenses, get_monthly_income

REPORTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")


def generate_report_text(user_id, fullname):
    total_income, total_expenses, balance = get_totals(user_id)
    breakdown = get_category_breakdown(user_id)
    monthly_expenses = get_monthly_expenses(user_id)
    monthly_income = get_monthly_income(user_id)

    lines = []
    lines.append("=" * 50)
    lines.append("FINWISE AI - FINANCIAL SUMMARY REPORT")
    lines.append("=" * 50)
    lines.append(f"User: {fullname}")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("-" * 50)
    lines.append(f"Total Income:   {total_income:,.2f}")
    lines.append(f"Total Expenses: {total_expenses:,.2f}")
    lines.append(f"Balance:        {balance:,.2f}")
    lines.append("-" * 50)
    lines.append("Spending by Category:")
    if breakdown.empty:
        lines.append("  (no expenses recorded yet)")
    else:
        for category, amount in breakdown.items():
            lines.append(f"  {category:<15} {amount:,.2f}")
    lines.append("-" * 50)
    lines.append("Monthly Breakdown:")
    all_months = sorted(set(list(monthly_income.index) + list(monthly_expenses.index)))
    if not all_months:
        lines.append("  (no records yet)")
    else:
        for month in all_months:
            inc = monthly_income.get(month, 0.0)
            exp = monthly_expenses.get(month, 0.0)
            lines.append(f"  {month}: Income {inc:,.2f} | Expenses {exp:,.2f} | Net {inc - exp:,.2f}")
    lines.append("=" * 50)

    return "\n".join(lines)


def save_report(user_id, fullname):
    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    text = generate_report_text(user_id, fullname)
    filename = f"report_{fullname.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join(REPORTS_FOLDER, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path, text
