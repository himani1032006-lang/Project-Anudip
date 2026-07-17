"""
user.py
-------
Handles the logged-in user's dashboard actions: adding income/expenses,
viewing, searching, updating, deleting transactions, and viewing balance.

Responsibility: User-facing menu logic. The actual SQL work is
delegated to the Transaction class (composition).
"""

from transaction import Transaction
from utils import get_valid_amount, get_valid_category, print_transaction_row, print_header


class User:
    """Represents the currently logged-in user and their menu actions."""

    def __init__(self, db, user_id):
        self.db = db
        self.user_id = user_id
        self.transaction = Transaction(db)

    def add_income(self):
        print_header("Add Income")
        category = get_valid_category("Income")
        amount = get_valid_amount()
        description = input("Enter a short description (optional): ").strip()
        self.transaction.add_transaction(self.user_id, "Income", category, amount, description)

    def add_expense(self):
        print_header("Add Expense")
        category = get_valid_category("Expense")
        amount = get_valid_amount()
        description = input("Enter a short description (optional): ").strip()
        self.transaction.add_transaction(self.user_id, "Expense", category, amount, description)

    def view_transactions(self):
        print_header("All Transactions")
        rows = self.transaction.get_all_transactions(self.user_id)

        if not rows:
            print("No transactions found.")
            return

        for row in rows:
            print_transaction_row(row)

    def search_transaction(self):
        print_header("Search Transaction")
        keyword = input("Enter a category or keyword to search: ").strip()

        if not keyword:
            print("Search keyword cannot be empty.")
            return

        rows = self.transaction.search_transactions(self.user_id, keyword)

        if not rows:
            print("No matching transactions found.")
            return

        for row in rows:
            print_transaction_row(row)

    def update_transaction(self):
        print_header("Update Transaction")
        transaction_id = input("Enter the Transaction ID to update: ").strip()

        if not transaction_id.isdigit():
            print("Invalid Transaction ID.")
            return

        existing = self.transaction.get_transaction_by_id(int(transaction_id), self.user_id)
        if not existing:
            print("Transaction not found or does not belong to you.")
            return

        transaction_type = existing[1]  # Income or Expense - kept unchanged
        print(f"Updating a {transaction_type} transaction.")

        category = get_valid_category(transaction_type)
        amount = get_valid_amount()
        description = input("Enter a new description (optional): ").strip()

        self.transaction.update_transaction(
            int(transaction_id), self.user_id, category, amount, description
        )

    def delete_transaction(self):
        print_header("Delete Transaction")
        transaction_id = input("Enter the Transaction ID to delete: ").strip()

        if not transaction_id.isdigit():
            print("Invalid Transaction ID.")
            return

        confirm = input("Are you sure you want to delete this transaction? (y/n): ").strip().lower()
        if confirm != "y":
            print("Delete cancelled.")
            return

        self.transaction.delete_transaction(int(transaction_id), self.user_id)

    def view_balance(self):
        print_header("Your Balance Summary")
        total_income, total_expense, balance = self.transaction.get_balance(self.user_id)

        print(f"Total Income   : {total_income:.2f}")
        print(f"Total Expense  : {total_expense:.2f}")
        print(f"Current Balance: {balance:.2f}")
