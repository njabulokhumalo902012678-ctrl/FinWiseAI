"""
analysis.py
Data analysis helpers: totals, category breakdowns, monthly summaries.
Uses pandas to make the AI/prediction step simple.
"""

import pandas as pd
from database import get_connection


def get_income_df(user_id) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM income WHERE user_id = ? ORDER BY date", conn, params=(user_id,)
    )
    conn.close()
    return df


def get_expense_df(user_id) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM expenses WHERE user_id = ? ORDER BY date", conn, params=(user_id,)
    )
    conn.close()
    return df


def get_totals(user_id):
    """Return (total_income, total_expenses, balance)."""
    income_df = get_income_df(user_id)
    expense_df = get_expense_df(user_id)

    total_income = float(income_df["amount"].sum()) if not income_df.empty else 0.0
    total_expenses = float(expense_df["amount"].sum()) if not expense_df.empty else 0.0
    balance = total_income - total_expenses
    return total_income, total_expenses, balance


def get_category_breakdown(user_id) -> pd.Series:
    """Return total spent per category, sorted descending."""
    df = get_expense_df(user_id)
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("category")["amount"].sum().sort_values(ascending=False)


def get_monthly_expenses(user_id) -> pd.Series:
    """Return total expenses grouped by calendar month (YYYY-MM), sorted chronologically."""
    df = get_expense_df(user_id)
    if df.empty:
        return pd.Series(dtype=float)
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    return df.groupby("month")["amount"].sum().sort_index()


def get_monthly_income(user_id) -> pd.Series:
    df = get_income_df(user_id)
    if df.empty:
        return pd.Series(dtype=float)
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    return df.groupby("month")["amount"].sum().sort_index()


def highest_spending_category(user_id):
    breakdown = get_category_breakdown(user_id)
    if breakdown.empty:
        return None, 0.0
    return breakdown.index[0], float(breakdown.iloc[0])
