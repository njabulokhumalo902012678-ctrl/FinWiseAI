# FinWise AI — Intelligent Personal Finance Management System

Track your money. Understand your spending. Plan your future.

## Description
FinWise AI is a Python desktop application (Tkinter GUI + SQLite database) that lets
users record income and expenses, view category and monthly breakdowns as charts,
receive an AI-generated prediction of next month's spending (Linear Regression), and
get rule-based budgeting recommendations.

## Problem Solved
Many people track spending inconsistently or not at all, making it hard to see where
money goes or plan ahead. FinWise AI automates the tracking, analysis, and forecasting.

## Features
- Secure account registration/login (SHA-256 password hashing)
- Add income and categorized expenses
- Dashboard: total income, total expenses, balance, top spending category
- Charts: spending-by-category pie chart, monthly income vs. expenses bar chart
- AI expense prediction (scikit-learn Linear Regression) once 2+ months of data exist
- Rule-based budgeting recommendations (overspending, category concentration,
  month-over-month change, savings rate)
- Exportable text summary report

## Technologies
- Python 3
- Tkinter (GUI)
- SQLite (database)
- Pandas (data analysis)
- Scikit-learn (Linear Regression prediction)
- Matplotlib (charts, embedded in Tkinter)

## Installation
```bash
pip install pandas scikit-learn matplotlib
```
Tkinter and sqlite3 ship with standard Python on Windows/macOS. On Linux:
```bash
sudo apt install python3-tk
```

## How to Run
```bash
python main.py
```
1. Register a new account, then log in.
2. Add a few income and expense records (use different dates/months to unlock
   the AI prediction, which needs at least 2 distinct months of expense data).
3. View your dashboard: totals, charts, prediction, and recommendations.
4. Click "Export Report" to save a summary to the `reports/` folder.

## Project Structure
```
FinWiseAI/
├── main.py              # entry point
├── database.py          # SQLite connection + table creation
├── login.py             # login/registration UI
├── dashboard.py         # main window: stats, charts, AI panel
├── income.py            # add income window
├── expenses.py          # add expense window
├── analysis.py          # pandas-based totals/breakdowns
├── prediction.py        # Linear Regression expense forecast
├── recommendations.py   # rule-based budgeting tips
├── reports.py           # text report generation
├── database/            # finance.db created here at runtime
├── models/              # reserved for a saved model file, if added later
└── reports/             # exported .txt reports saved here
```

## Future Improvements
- Bank account integration
- Mobile application
- AI chatbot financial assistant
- Receipt scanning via OCR
- Savings goals and multi-currency support
- Cloud synchronization
