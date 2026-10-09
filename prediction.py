"""
prediction.py
AI Feature 1: Expense Prediction.
Uses scikit-learn Linear Regression on the user's monthly expense totals
to estimate spending for the next month.
"""

import numpy as np
from sklearn.linear_model import LinearRegression

from analysis import get_monthly_expenses

MIN_MONTHS_REQUIRED = 2  # need at least 2 months of data to fit a trend


def predict_next_month_expense(user_id):
    """
    Returns (predicted_amount, monthly_series) or (None, monthly_series)
    if there isn't enough data yet.
    """
    monthly = get_monthly_expenses(user_id)

    if len(monthly) < MIN_MONTHS_REQUIRED:
        return None, monthly

    X = np.arange(len(monthly)).reshape(-1, 1)  # month index: 0, 1, 2, ...
    y = monthly.values

    model = LinearRegression()
    model.fit(X, y)

    next_index = np.array([[len(monthly)]])
    prediction = model.predict(next_index)[0]

    # Spending can't sensibly be predicted as negative
    prediction = max(0.0, float(prediction))
    return prediction, monthly
