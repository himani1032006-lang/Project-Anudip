"""
admin.py
--------
Handles the logged-in admin's dashboard actions: viewing users,
viewing all transactions, deleting any transaction, and generating reports.

Responsibility: Admin-facing menu logic. Delegates data access to
Transaction and Reports classes (composition).
"""

import psycopg2
from transaction import Transaction
from reports import Reports
from utils import print_header


class Admin:
    """Represents the currently logged-in admin and their menu actions."""

    def __init__(self, db, admin_id):
        self.db = db
        self.admin_id = admin_id
        self.transaction = Transaction(db)
        self.reports = Reports(db)

    def view_users(self):
        print_header("All Registered Users")
        try:
            self.db.cursor.execute(
                """SELECT user_id, name, email, phone
                   FROM users
                   ORDER BY user_id;"""
            )
            users = self.db.cursor.fetchall()

            if not users:
                print("No users found.")
                return

            for user_id, name, email, phone in users:
                print(f"ID: {user_id} | Name: {name} | Email: {email} | Phone: {phone}")

        except psycopg2.Error as error:
            print(f"Error fetching users: {error}")

    def view_all_transactions(self):
        print_header("All Transactions (All Users)")
        rows = self.transaction.get_all_transactions_admin()

        if not rows:
            print("No transactions found.")
            return

        for (transaction_id, user_name, transaction_type,
             category, amount, description, transaction_date) in rows:
            print(
                f"ID: {transaction_id} | User: {user_name} | {transaction_type:7} | "
                f"{category:12} | Amount: {amount:10.2f} | Date: {transaction_date} | "
                f"Note: {description if description else '-'}"
            )

    def delete_transaction(self):
        print_header("Delete Transaction (Admin)")
        transaction_id = input("Enter the Transaction ID to delete: ").strip()

        if not transaction_id.isdigit():
            print("Invalid Transaction ID.")
            return

        confirm = input("Are you sure you want to delete this transaction? (y/n): ").strip().lower()
        if confirm != "y":
            print("Delete cancelled.")
            return

        # Admin can delete any user's transaction, so user_id is not passed.
        self.transaction.delete_transaction(int(transaction_id))

    def generate_reports(self):
        self.reports.generate_full_report()
