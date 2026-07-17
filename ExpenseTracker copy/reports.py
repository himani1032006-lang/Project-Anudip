"""
reports.py
----------
Generates simple summary reports across all users:
total income, total expense, balance, category breakdowns,
and total transaction count.

Responsibility: Reporting/aggregation queries only.
"""

import psycopg2
from utils import print_header


class Reports:
    """Generates system-wide reports for the admin."""

    def __init__(self, db):
        self.db = db

    def total_income(self):
        try:
            self.db.cursor.execute(
                """SELECT COALESCE(SUM(amount), 0) FROM transactions
                   WHERE transaction_type = 'Income';"""
            )
            return self.db.cursor.fetchone()[0]
        except psycopg2.Error as error:
            print(f"Error calculating total income: {error}")
            return 0

    def total_expense(self):
        try:
            self.db.cursor.execute(
                """SELECT COALESCE(SUM(amount), 0) FROM transactions
                   WHERE transaction_type = 'Expense';"""
            )
            return self.db.cursor.fetchone()[0]
        except psycopg2.Error as error:
            print(f"Error calculating total expense: {error}")
            return 0

    def total_transactions(self):
        try:
            self.db.cursor.execute("SELECT COUNT(*) FROM transactions;")
            return self.db.cursor.fetchone()[0]
        except psycopg2.Error as error:
            print(f"Error counting transactions: {error}")
            return 0

    def expense_by_category(self):
        try:
            self.db.cursor.execute(
                """SELECT category, SUM(amount) FROM transactions
                   WHERE transaction_type = 'Expense'
                   GROUP BY category
                   ORDER BY SUM(amount) DESC;"""
            )
            return self.db.cursor.fetchall()
        except psycopg2.Error as error:
            print(f"Error fetching expense by category: {error}")
            return []

    def income_by_category(self):
        try:
            self.db.cursor.execute(
                """SELECT category, SUM(amount) FROM transactions
                   WHERE transaction_type = 'Income'
                   GROUP BY category
                   ORDER BY SUM(amount) DESC;"""
            )
            return self.db.cursor.fetchall()
        except psycopg2.Error as error:
            print(f"Error fetching income by category: {error}")
            return []

    def generate_full_report(self):
        """Print a complete summary report to the console."""
        print_header("System Report")

        income = self.total_income()
        expense = self.total_expense()
        balance = income - expense
        count = self.total_transactions()

        print(f"Total Income        : {income:.2f}")
        print(f"Total Expense       : {expense:.2f}")
        print(f"Current Balance     : {balance:.2f}")
        print(f"Total Transactions  : {count}")

        print("\n-- Income by Category --")
        income_rows = self.income_by_category()
        if income_rows:
            for category, amount in income_rows:
                print(f"{category:15}: {amount:.2f}")
        else:
            print("No income records found.")

        print("\n-- Expense by Category --")
        expense_rows = self.expense_by_category()
        if expense_rows:
            for category, amount in expense_rows:
                print(f"{category:15}: {amount:.2f}")
        else:
            print("No expense records found.")
