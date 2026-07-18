# ============================================
# user.py — User Dashboard Module
# ============================================
# Is file mein User class hai jo logged-in user
# ke dashboard aur operations handle karta hai.

from transaction import Transaction
from utils import show_user_menu, pause


class User:
    """
    User class — User ka dashboard aur operations manage karta hai.
    """

    def __init__(self, db, user_id, name):
        """
        Constructor — User ki details aur Transaction object store karta hai.
        """
        self.db = db
        self.user_id = user_id
        self.name = name
        # Transaction object banao — CRUD operations ke liye
        self.transaction = Transaction(db)

    def add_income(self):
        """Income add karta hai — Transaction class ko call karta hai."""
        self.transaction.add_transaction(self.user_id, "Income")

    def add_expense(self):
        """Expense add karta hai — Transaction class ko call karta hai."""
        self.transaction.add_transaction(self.user_id, "Expense")

    def view_transactions(self):
        """User ke saare transactions dikhata hai."""
        self.transaction.view_transactions(self.user_id)

    def search_transaction(self):
        """Transaction search karta hai keyword se."""
        self.transaction.search_transaction(self.user_id)

    def update_transaction(self):
        """Transaction update karta hai."""
        self.transaction.update_transaction(self.user_id)

    def delete_transaction(self):
        """Transaction delete karta hai."""
        self.transaction.delete_transaction(self.user_id)

    def view_balance(self):
        """
        User ka balance dikhata hai.
        Total Income - Total Expense = Remaining Balance
        """
        try:
            # ---- Total Income nikalo ----
            self.db.cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = %s AND transaction_type = 'Income'
            """, (self.user_id,))
            total_income = self.db.cursor.fetchone()[0]

            # ---- Total Expense nikalo ----
            self.db.cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = %s AND transaction_type = 'Expense'
            """, (self.user_id,))
            total_expense = self.db.cursor.fetchone()[0]

            # ---- Balance calculate karo ----
            balance = total_income - total_expense

            # ---- Display karo ----
            print("\n" + "=" * 40)
            print("   💰 YOUR BALANCE SUMMARY")
            print("=" * 40)
            print(f"  📈 Total Income:   ₹{total_income}")
            print(f"  📉 Total Expense:  ₹{total_expense}")
            print(f"  💵 Balance:        ₹{balance}")
            print("=" * 40)

            if balance < 0:
                print("  ⚠️ Warning: You have overspent!")

        except Exception as e:
            print(f"❌ Failed to fetch balance: {e}")

    def user_dashboard(self):
        """
        User dashboard — Menu loop chalata hai.
        Jab tak user logout nahi karta, menu dikhata rahega.
        """
        while True:
            show_user_menu(self.name)
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_income()
            elif choice == "2":
                self.add_expense()
            elif choice == "3":
                self.view_transactions()
            elif choice == "4":
                self.search_transaction()
            elif choice == "5":
                self.update_transaction()
            elif choice == "6":
                self.delete_transaction()
            elif choice == "7":
                self.view_balance()
            elif choice == "8":
                print(f"\n👋 Goodbye, {self.name}! Logged out.")
                break
            else:
                print("❌ Invalid choice! Please try again.")

            pause()
