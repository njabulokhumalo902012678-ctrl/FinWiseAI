"""
recommendations.py
AI Feature 3: Rule-based budgeting recommendations, combining
simple Python logic with the user's analyzed financial data.
"""

from analysis import get_totals, get_category_breakdown, get_monthly_expenses


def generate_recommendations(user_id):
    tips = []

    total_income, total_expenses, balance = get_totals(user_id)

    if total_income == 0 and total_expenses == 0:
        return ["Add some income and expenses to start receiving personalized recommendations."]

    # Rule: spending exceeds income
    if total_expenses > total_income:
        tips.append(
            "⚠️ Your total expenses currently exceed your total income. "
            "Consider reducing discretionary spending or increasing income."
        )

    # Rule: category concentration
    breakdown = get_category_breakdown(user_id)
    if not breakdown.empty and total_expenses > 0:
        top_category = breakdown.index[0]
        top_amount = breakdown.iloc[0]
        top_pct = (top_amount / total_expenses) * 100

        if top_category == "Food" and top_pct > 30:
            tips.append(f"🍽️ Food spending is {top_pct:.0f}% of your expenses. Consider setting a food budget.")
        elif top_pct > 40:
            tips.append(
                f"📊 '{top_category}' makes up {top_pct:.0f}% of your spending — "
                "this is your largest category. Consider reviewing it."
            )

    # Rule: month-over-month increase in any category (compares last two months overall)
    monthly = get_monthly_expenses(user_id)
    if len(monthly) >= 2:
        last, prev = monthly.iloc[-1], monthly.iloc[-2]
        if prev > 0:
            change_pct = ((last - prev) / prev) * 100
            if change_pct > 15:
                tips.append(
                    f"📈 Your overall spending increased by {change_pct:.0f}% compared with last month. "
                    "Consider reviewing recent purchases."
                )
            elif change_pct < -15:
                tips.append(f"✅ Great job — spending decreased by {abs(change_pct):.0f}% compared with last month.")

    # Rule: healthy savings
    if total_income > 0:
        savings_rate = (balance / total_income) * 100
        if savings_rate >= 20:
            tips.append(f"💰 You're saving {savings_rate:.0f}% of your income — that's a healthy savings rate.")
        elif 0 <= savings_rate < 10:
            tips.append(f"💡 You're saving only {savings_rate:.0f}% of your income. Aim for at least 10–20%.")

    if not tips:
        tips.append("Your finances look balanced right now. Keep tracking to spot new trends.")

    return tips
