"""
main.py
Entry point for FinWise AI - Intelligent Personal Finance Management System.

Run with:
    python main.py

Requirements (install first):
    pip install pandas scikit-learn matplotlib
    (tkinter and sqlite3 ship with standard Python on Windows/macOS;
     on Linux you may need: sudo apt install python3-tk)
"""

from database import create_tables
from login import LoginWindow
from dashboard import Dashboard


def launch_dashboard(user_id, fullname):
    app = Dashboard(user_id, fullname)
    app.mainloop()


def main():
    create_tables()
    login = LoginWindow(on_success=launch_dashboard)
    login.mainloop()


if __name__ == "__main__":
    main()
