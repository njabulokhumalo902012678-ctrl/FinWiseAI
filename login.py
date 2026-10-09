"""
login.py
Login and registration screens for FinWise AI.
Passwords are stored as SHA-256 hashes (never plaintext).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import re

from database import get_connection


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def is_valid_email(email: str) -> bool:
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None


class LoginWindow(tk.Tk):
    """First screen shown when the application starts."""

    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success  # callback(user_id, fullname)

        self.title("FinWise AI - Login")
        self.geometry("400x420")
        self.resizable(False, False)
        self.configure(bg="#0f172a")

        self._build_login_ui()

    # ---------- UI ----------
    def _build_login_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(
            self, text="FinWise AI", font=("Segoe UI", 22, "bold"),
            bg="#0f172a", fg="#38bdf8"
        ).pack(pady=(30, 0))
        tk.Label(
            self, text="Track your money. Understand your spending.",
            font=("Segoe UI", 10), bg="#0f172a", fg="#94a3b8"
        ).pack(pady=(0, 20))

        form = tk.Frame(self, bg="#0f172a")
        form.pack(pady=10)

        tk.Label(form, text="Email", bg="#0f172a", fg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(form, width=30)
        self.email_entry.grid(row=1, column=0, pady=5)

        tk.Label(form, text="Password", bg="#0f172a", fg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(form, width=30, show="*")
        self.password_entry.grid(row=3, column=0, pady=5)

        ttk.Button(self, text="Login", command=self._handle_login).pack(pady=(20, 5), ipadx=20)
        ttk.Button(self, text="Create an Account", command=self._build_register_ui).pack(pady=5)

        self.bind("<Return>", lambda e: self._handle_login())

    def _build_register_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(
            self, text="Create Account", font=("Segoe UI", 18, "bold"),
            bg="#0f172a", fg="#38bdf8"
        ).pack(pady=(30, 20))

        form = tk.Frame(self, bg="#0f172a")
        form.pack(pady=5)

        tk.Label(form, text="Full Name", bg="#0f172a", fg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.reg_name = ttk.Entry(form, width=30)
        self.reg_name.grid(row=1, column=0, pady=5)

        tk.Label(form, text="Email", bg="#0f172a", fg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.reg_email = ttk.Entry(form, width=30)
        self.reg_email.grid(row=3, column=0, pady=5)

        tk.Label(form, text="Password", bg="#0f172a", fg="white").grid(row=4, column=0, sticky="w", pady=5)
        self.reg_password = ttk.Entry(form, width=30, show="*")
        self.reg_password.grid(row=5, column=0, pady=5)

        tk.Label(form, text="Confirm Password", bg="#0f172a", fg="white").grid(row=6, column=0, sticky="w", pady=5)
        self.reg_confirm = ttk.Entry(form, width=30, show="*")
        self.reg_confirm.grid(row=7, column=0, pady=5)

        ttk.Button(self, text="Register", command=self._handle_register).pack(pady=(20, 5), ipadx=20)
        ttk.Button(self, text="Back to Login", command=self._build_login_ui).pack(pady=5)

    # ---------- Logic ----------
    def _handle_login(self):
        email = self.email_entry.get().strip().lower()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, fullname, password FROM users WHERE email = ?", (email,))
        row = cur.fetchone()
        conn.close()

        if row is None or row[2] != hash_password(password):
            messagebox.showerror("Login Failed", "Invalid email or password.")
            return

        user_id, fullname = row[0], row[1]
        self.destroy()
        self.on_success(user_id, fullname)

    def _handle_register(self):
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip().lower()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()

        if not name or not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return
        if not is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters.")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
                (name, email, hash_password(password)),
            )
            conn.commit()
        except Exception:
            messagebox.showerror("Error", "An account with this email already exists.")
            conn.close()
            return
        conn.close()

        messagebox.showinfo("Success", "Account created successfully. Please log in.")
        self._build_login_ui()
