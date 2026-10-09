"""
dashboard.py
Main application window shown after login. Ties together income, expenses,
analysis, AI prediction, recommendations, and reports.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from analysis import get_totals, get_category_breakdown, get_monthly_expenses, get_monthly_income
from income import open_income_window
from expenses import open_expense_window
from prediction import predict_next_month_expense
from recommendations import generate_recommendations
from reports import save_report


class Dashboard(tk.Tk):
    def __init__(self, user_id, fullname):
        super().__init__()
        self.user_id = user_id
        self.fullname = fullname

        self.title(f"FinWise AI - Dashboard ({fullname})")
        self.geometry("1000x650")
        self.configure(bg="#0f172a")

        self._build_layout()
        self.refresh()

    # ---------- Layout ----------
    def _build_layout(self):
        header = tk.Frame(self, bg="#0f172a")
        header.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(header, text=f"Welcome, {self.fullname}", font=("Segoe UI", 18, "bold"),
                 bg="#0f172a", fg="#38bdf8").pack(side="left")

        ttk.Button(header, text="+ Add Income", command=self._add_income).pack(side="right", padx=5)
        ttk.Button(header, text="+ Add Expense", command=self._add_expense).pack(side="right", padx=5)
        ttk.Button(header, text="Export Report", command=self._export_report).pack(side="right", padx=5)

        # Stat cards
        self.stats_frame = tk.Frame(self, bg="#0f172a")
        self.stats_frame.pack(fill="x", padx=20, pady=10)

        self.income_card = self._make_stat_card(self.stats_frame, "Total Income", "#22c55e")
        self.expense_card = self._make_stat_card(self.stats_frame, "Total Expenses", "#ef4444")
        self.balance_card = self._make_stat_card(self.stats_frame, "Balance", "#38bdf8")
        self.top_category_card = self._make_stat_card(self.stats_frame, "Top Category", "#f59e0b")

        # Body: charts on the left, AI panel on the right
        body = tk.Frame(self, bg="#0f172a")
        body.pack(fill="both", expand=True, padx=20, pady=10)

        self.chart_frame = tk.Frame(body, bg="#0f172a")
        self.chart_frame.pack(side="left", fill="both", expand=True)

        ai_panel = tk.Frame(body, bg="#111827", width=320)
        ai_panel.pack(side="right", fill="y", padx=(15, 0))
        ai_panel.pack_propagate(False)

        tk.Label(ai_panel, text="🤖 AI Prediction", font=("Segoe UI", 13, "bold"),
                 bg="#111827", fg="#38bdf8").pack(anchor="w", padx=15, pady=(15, 5))
        self.prediction_label = tk.Label(ai_panel, text="", wraplength=290, justify="left",
                                          bg="#111827", fg="white", font=("Segoe UI", 10))
        self.prediction_label.pack(anchor="w", padx=15, pady=(0, 15))

        tk.Label(ai_panel, text="💡 Recommendations", font=("Segoe UI", 13, "bold"),
                 bg="#111827", fg="#38bdf8").pack(anchor="w", padx=15, pady=(5, 5))
        self.recommendations_label = tk.Label(ai_panel, text="", wraplength=290, justify="left",
                                               bg="#111827", fg="white", font=("Segoe UI", 10))
        self.recommendations_label.pack(anchor="w", padx=15, pady=(0, 15))

    def _make_stat_card(self, parent, title, color):
        card = tk.Frame(parent, bg="#1e293b", width=220, height=80)
        card.pack(side="left", padx=8, fill="x", expand=True)
        card.pack_propagate(False)
        tk.Label(card, text=title, bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(10, 0))
        value_label = tk.Label(card, text="0.00", bg="#1e293b", fg=color, font=("Segoe UI", 16, "bold"))
        value_label.pack(anchor="w", padx=12)
        return value_label

    # ---------- Actions ----------
    def _add_income(self):
        open_income_window(self, self.user_id, self.refresh)

    def _add_expense(self):
        open_expense_window(self, self.user_id, self.refresh)

    def _export_report(self):
        path, _ = save_report(self.user_id, self.fullname)
        messagebox.showinfo("Report Saved", f"Report saved to:\n{path}")

    # ---------- Data refresh ----------
    def refresh(self):
        total_income, total_expenses, balance = get_totals(self.user_id)
        self.income_card.config(text=f"{total_income:,.2f}")
        self.expense_card.config(text=f"{total_expenses:,.2f}")
        self.balance_card.config(text=f"{balance:,.2f}")

        breakdown = get_category_breakdown(self.user_id)
        if breakdown.empty:
            self.top_category_card.config(text="N/A")
        else:
            self.top_category_card.config(text=breakdown.index[0])

        self._draw_charts()
        self._update_prediction()
        self._update_recommendations()

    def _draw_charts(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(6.2, 6), dpi=90, facecolor="#0f172a")

        # Pie chart: spending by category
        ax1 = fig.add_subplot(211)
        breakdown = get_category_breakdown(self.user_id)
        ax1.set_facecolor("#0f172a")
        if breakdown.empty:
            ax1.text(0.5, 0.5, "No expenses yet", ha="center", va="center", color="white")
            ax1.axis("off")
        else:
            ax1.pie(breakdown.values, labels=breakdown.index, autopct="%1.0f%%",
                    textprops={"color": "white", "fontsize": 8})
        ax1.set_title("Spending by Category", color="white", fontsize=10)

        # Bar chart: monthly income vs expenses
        ax2 = fig.add_subplot(212)
        ax2.set_facecolor("#0f172a")
        monthly_income = get_monthly_income(self.user_id)
        monthly_expenses = get_monthly_expenses(self.user_id)
        months = sorted(set(list(monthly_income.index) + list(monthly_expenses.index)))

        if not months:
            ax2.text(0.5, 0.5, "No monthly data yet", ha="center", va="center", color="white")
            ax2.axis("off")
        else:
            income_vals = [monthly_income.get(m, 0) for m in months]
            expense_vals = [monthly_expenses.get(m, 0) for m in months]
            x = range(len(months))
            width = 0.35
            ax2.bar([i - width / 2 for i in x], income_vals, width, label="Income", color="#22c55e")
            ax2.bar([i + width / 2 for i in x], expense_vals, width, label="Expenses", color="#ef4444")
            ax2.set_xticks(list(x))
            ax2.set_xticklabels(months, rotation=30, ha="right", color="white", fontsize=8)
            ax2.tick_params(colors="white")
            ax2.legend(facecolor="#0f172a", labelcolor="white", fontsize=8)
        ax2.set_title("Monthly Income vs Expenses", color="white", fontsize=10)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _update_prediction(self):
        prediction, monthly = predict_next_month_expense(self.user_id)
        if prediction is None:
            text = "Not enough monthly data yet. Add expenses across at least 2 different months to unlock predictions."
        else:
            text = (
                f"Based on your spending trend, estimated expenses for next month: "
                f"{prediction:,.2f}\n\n(Model: Linear Regression on {len(monthly)} months of data)"
            )
        self.prediction_label.config(text=text)

    def _update_recommendations(self):
        tips = generate_recommendations(self.user_id)
        self.recommendations_label.config(text="\n\n".join(tips))
