"""
expenses.py
Window for adding a new expense record.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database import get_connection, EXPENSE_CATEGORIES


def open_expense_window(parent, user_id, refresh_callback):
    win = tk.Toplevel(parent)
    win.title("Add Expense")
    win.geometry("340x380")
    win.resizable(False, False)
    win.configure(bg="#0f172a")
    win.grab_set()

    tk.Label(win, text="Add Expense", font=("Segoe UI", 14, "bold"),
             bg="#0f172a", fg="#ef4444").pack(pady=15)

    form = tk.Frame(win, bg="#0f172a")
    form.pack(pady=5)

    tk.Label(form, text="Category", bg="#0f172a", fg="white").grid(row=0, column=0, sticky="w", pady=5)
    category_box = ttk.Combobox(form, values=EXPENSE_CATEGORIES, width=26, state="readonly")
    category_box.current(0)
    category_box.grid(row=1, column=0, pady=5)

    tk.Label(form, text="Description", bg="#0f172a", fg="white").grid(row=2, column=0, sticky="w", pady=5)
    desc_entry = ttk.Entry(form, width=28)
    desc_entry.grid(row=3, column=0, pady=5)

    tk.Label(form, text="Amount", bg="#0f172a", fg="white").grid(row=4, column=0, sticky="w", pady=5)
    amount_entry = ttk.Entry(form, width=28)
    amount_entry.grid(row=5, column=0, pady=5)

    tk.Label(form, text="Date (YYYY-MM-DD)", bg="#0f172a", fg="white").grid(row=6, column=0, sticky="w", pady=5)
    date_entry = ttk.Entry(form, width=28)
    date_entry.insert(0, date.today().isoformat())
    date_entry.grid(row=7, column=0, pady=5)

    def save():
        category = category_box.get()
        description = desc_entry.get().strip()
        amount_str = amount_entry.get().strip()
        date_str = date_entry.get().strip()

        if not category or not amount_str or not date_str:
            messagebox.showerror("Error", "Category, amount and date are required.", parent=win)
            return
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Amount must be a positive number.", parent=win)
            return
        try:
            date.fromisoformat(date_str)
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format.", parent=win)
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO expenses (user_id, category, description, amount, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, category, description, amount, date_str),
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Expense recorded.", parent=win)
        refresh_callback()
        win.destroy()

    ttk.Button(win, text="Save Expense", command=save).pack(pady=20, ipadx=15)
