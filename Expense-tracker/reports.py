# ============================================
# reports.py — Reports Generation Module
# ============================================
# Is file mein Reports class hai jo admin ke liye
# summary reports generate karta hai.

class Reports:
    """
    Reports class — Income, Expense aur Balance ke
    reports generate karta hai.
    """

    def __init__(self, db):
        """Constructor — Database object receive karta hai."""
        self.db = db

    def total_income(self):
        """Saare users ka total income nikalta hai."""
        try:
            self.db.cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE transaction_type = 'Income'
            """)
            return self.db.cursor.fetchone()[0]
        except Exception as e:
            print(f"❌ Error: {e}")
            return 0

    def total_expense(self):
        """Saare users ka total expense nikalta hai."""
        try:
            self.db.cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE transaction_type = 'Expense'
            """)
            return self.db.cursor.fetchone()[0]
        except Exception as e:
            print(f"❌ Error: {e}")
            return 0

    def current_balance(self):
        """Total Income - Total Expense = Current Balance"""
        income = self.total_income()
        expense = self.total_expense()
        return income - expense

    def expense_by_category(self):
        """
        Category wise expense dikhata hai.
        GROUP BY use karta hai category pe.
        """
        try:
            self.db.cursor.execute("""
                SELECT category, SUM(amount) as total
                FROM transactions
                WHERE transaction_type = 'Expense'
                GROUP BY category
                ORDER BY total DESC
            """)
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"❌ Error: {e}")
            return []

    def income_by_category(self):
        """
        Category wise income dikhata hai.
        GROUP BY use karta hai category pe.
        """
        try:
            self.db.cursor.execute("""
                SELECT category, SUM(amount) as total
                FROM transactions
                WHERE transaction_type = 'Income'
                GROUP BY category
                ORDER BY total DESC
            """)
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"❌ Error: {e}")
            return []

    def total_transactions(self):
        """Total number of transactions count karta hai."""
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) FROM transactions"
            )
            return self.db.cursor.fetchone()[0]
        except Exception as e:
            print(f"❌ Error: {e}")
            return 0

    def generate_report(self):
        """
        Complete report generate karta hai.
        Saari summary ek jagah dikhata hai.
        """
        income = self.total_income()
        expense = self.total_expense()
        balance = income - expense
        total_txn = self.total_transactions()

        print("\n" + "=" * 50)
        print("   📊 EXPENSE TRACKER — FULL REPORT")
        print("=" * 50)

        # ---- Overall Summary ----
        print("\n📌 Overall Summary:")
        print(f"  📈 Total Income:        ₹{income}")
        print(f"  📉 Total Expense:       ₹{expense}")
        print(f"  💵 Current Balance:     ₹{balance}")
        print(f"  📋 Total Transactions:  {total_txn}")

        # ---- Income by Category ----
        income_cat = self.income_by_category()
        print("\n📌 Income by Category:")
        print("-" * 35)
        if income_cat:
            for cat, amount in income_cat:
                print(f"  {cat:<20} ₹{amount}")
        else:
            print("  No income records found.")

        # ---- Expense by Category ----
        expense_cat = self.expense_by_category()
        print("\n📌 Expense by Category:")
        print("-" * 35)
        if expense_cat:
            for cat, amount in expense_cat:
                print(f"  {cat:<20} ₹{amount}")
        else:
            print("  No expense records found.")

        print("\n" + "=" * 50)
        print("   Report generated successfully! ✅")
        print("=" * 50)
