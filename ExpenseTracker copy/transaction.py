"""
transaction.py
---------------
Handles all database operations related to transactions:
add, view, search, update, delete.

Responsibility: Transaction data access only. Both User and Admin
classes use this class instead of writing SQL themselves, which keeps
the SQL logic in one place (modular programming).
"""

import psycopg2


class Transaction:
    """Represents transaction-related database operations."""

    def __init__(self, db):
        self.db = db

    def add_transaction(self, user_id, transaction_type, category, amount, description):
        """Insert a new income or expense transaction for a user."""
        try:
            self.db.cursor.execute(
                """INSERT INTO transactions
                   (user_id, transaction_type, category, amount, description)
                   VALUES (%s, %s, %s, %s, %s);""",
                (user_id, transaction_type, category, amount, description)
            )
            self.db.connection.commit()
            print(f"{transaction_type} added successfully.")

        except psycopg2.Error as error:
            self.db.connection.rollback()
            print(f"Error adding transaction: {error}")

    def get_all_transactions(self, user_id):
        """Return all transactions for a specific user, newest first."""
        try:
            self.db.cursor.execute(
                """SELECT transaction_id, transaction_type, category,
                          amount, description, transaction_date
                   FROM transactions
                   WHERE user_id = %s
                   ORDER BY transaction_date DESC, transaction_id DESC;""",
                (user_id,)
            )
            return self.db.cursor.fetchall()

        except psycopg2.Error as error:
            print(f"Error fetching transactions: {error}")
            return []

    def search_transactions(self, user_id, keyword):
        """Search a user's transactions by category or description keyword."""
        try:
            like_pattern = f"%{keyword}%"
            self.db.cursor.execute(
                """SELECT transaction_id, transaction_type, category,
                          amount, description, transaction_date
                   FROM transactions
                   WHERE user_id = %s
                     AND (category ILIKE %s OR description ILIKE %s)
                   ORDER BY transaction_date DESC;""",
                (user_id, like_pattern, like_pattern)
            )
            return self.db.cursor.fetchall()

        except psycopg2.Error as error:
            print(f"Error searching transactions: {error}")
            return []

    def get_transaction_by_id(self, transaction_id, user_id=None):
        """Fetch a single transaction by ID.
        If user_id is given, restrict the lookup to that user (ownership check).
        """
        try:
            if user_id is not None:
                self.db.cursor.execute(
                    """SELECT transaction_id, transaction_type, category,
                              amount, description, transaction_date
                       FROM transactions
                       WHERE transaction_id = %s AND user_id = %s;""",
                    (transaction_id, user_id)
                )
            else:
                self.db.cursor.execute(
                    """SELECT transaction_id, transaction_type, category,
                              amount, description, transaction_date
                       FROM transactions
                       WHERE transaction_id = %s;""",
                    (transaction_id,)
                )
            return self.db.cursor.fetchone()

        except psycopg2.Error as error:
            print(f"Error fetching transaction: {error}")
            return None

    def update_transaction(self, transaction_id, user_id, category, amount, description):
        """Update category, amount, and description of a transaction owned by user_id."""
        try:
            self.db.cursor.execute(
                """UPDATE transactions
                   SET category = %s, amount = %s, description = %s
                   WHERE transaction_id = %s AND user_id = %s;""",
                (category, amount, description, transaction_id, user_id)
            )
            self.db.connection.commit()

            if self.db.cursor.rowcount == 0:
                print("No matching transaction found to update.")
            else:
                print("Transaction updated successfully.")

        except psycopg2.Error as error:
            self.db.connection.rollback()
            print(f"Error updating transaction: {error}")

    def delete_transaction(self, transaction_id, user_id=None):
        """Delete a transaction. If user_id is given, only that user's
        transaction can be deleted (used by User class). If user_id is
        None, any transaction can be deleted (used by Admin class).
        """
        try:
            if user_id is not None:
                self.db.cursor.execute(
                    "DELETE FROM transactions WHERE transaction_id = %s AND user_id = %s;",
                    (transaction_id, user_id)
                )
            else:
                self.db.cursor.execute(
                    "DELETE FROM transactions WHERE transaction_id = %s;",
                    (transaction_id,)
                )
            self.db.connection.commit()

            if self.db.cursor.rowcount == 0:
                print("No matching transaction found to delete.")
            else:
                print("Transaction deleted successfully.")

        except psycopg2.Error as error:
            self.db.connection.rollback()
            print(f"Error deleting transaction: {error}")

    def get_balance(self, user_id):
        """Return (total_income, total_expense, balance) for a user."""
        try:
            self.db.cursor.execute(
                """SELECT
                       COALESCE(SUM(amount) FILTER (WHERE transaction_type = 'Income'), 0),
                       COALESCE(SUM(amount) FILTER (WHERE transaction_type = 'Expense'), 0)
                   FROM transactions
                   WHERE user_id = %s;""",
                (user_id,)
            )
            total_income, total_expense = self.db.cursor.fetchone()
            balance = total_income - total_expense
            return total_income, total_expense, balance

        except psycopg2.Error as error:
            print(f"Error calculating balance: {error}")
            return 0, 0, 0

    def get_all_transactions_admin(self):
        """Return all transactions across all users, joined with user name."""
        try:
            self.db.cursor.execute(
                """SELECT t.transaction_id, u.name, t.transaction_type,
                          t.category, t.amount, t.description, t.transaction_date
                   FROM transactions t
                   INNER JOIN users u ON t.user_id = u.user_id
                   ORDER BY t.transaction_date DESC, t.transaction_id DESC;"""
            )
            return self.db.cursor.fetchall()

        except psycopg2.Error as error:
            print(f"Error fetching all transactions: {error}")
            return []
