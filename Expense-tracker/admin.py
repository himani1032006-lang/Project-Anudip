# ============================================
# admin.py — Admin Dashboard Module
# ============================================
# Is file mein Admin class hai jo admin ke
# dashboard aur operations handle karta hai.

from transaction import Transaction
from reports import Reports
from utils import show_admin_menu, display_transactions, pause


class Admin:
    """
    Admin class — Admin dashboard aur operations manage karta hai.
    Admin saare users dekh sakta hai, transactions dekh/delete kar sakta hai,
    aur reports generate kar sakta hai.
    """

    def __init__(self, db):
        """
        Constructor — Database object, Transaction object,
        aur Reports object store karta hai.
        """
        self.db = db
        self.transaction = Transaction(db)
        self.reports = Reports(db)

    def view_all_users(self):
        """
        Saare registered users dikhata hai.
        INNER JOIN se har user ke transaction count bhi dikhata hai.
        """
        try:
            # LEFT JOIN isliye use kiya — taki bina transaction wale users bhi dikhe
            self.db.cursor.execute("""
                SELECT u.user_id, u.name, u.email, u.phone,
                       COUNT(t.transaction_id) as total_transactions
                FROM users u
                LEFT JOIN transactions t ON u.user_id = t.user_id
                GROUP BY u.user_id, u.name, u.email, u.phone
                ORDER BY u.user_id
            """)
            users = self.db.cursor.fetchall()

            if not users:
                print("\n📭 No users registered yet!")
                return

            # Table format mein display karo
            print("\n" + "=" * 75)
            print(f"{'ID':<6} {'Name':<20} {'Email':<25} {'Phone':<15} {'Transactions':<12}")
            print("=" * 75)

            for user in users:
                print(f"{user[0]:<6} {user[1]:<20} {user[2]:<25} {user[3]:<15} {user[4]:<12}")

            print("=" * 75)
            print(f"Total Users: {len(users)}")

        except Exception as e:
            print(f"❌ Failed to fetch users: {e}")

    def view_all_transactions(self):
        """
        Saare users ke transactions dikhata hai.
        INNER JOIN se user ka naam bhi dikhata hai.
        """
        try:
            self.db.cursor.execute("""
                SELECT t.transaction_id, t.transaction_type, t.category,
                       t.amount, t.description, t.transaction_date, u.name
                FROM transactions t
                INNER JOIN users u ON t.user_id = u.user_id
                ORDER BY t.transaction_date DESC, t.transaction_id DESC
            """)
            transactions = self.db.cursor.fetchall()

            if not transactions:
                print("\n📭 No transactions found!")
                return

            # Table format — admin ko user name bhi dikhega
            print("\n" + "=" * 110)
            print(f"{'ID':<6} {'User':<15} {'Type':<10} {'Category':<15} {'Amount':<12} {'Description':<25} {'Date':<12}")
            print("=" * 110)

            for txn in transactions:
                print(f"{txn[0]:<6} {txn[6]:<15} {txn[1]:<10} {txn[2]:<15} ₹{txn[3]:<11} {txn[4]:<25} {txn[5]}")

            print("=" * 110)
            print(f"Total Transactions: {len(transactions)}")

        except Exception as e:
            print(f"❌ Failed to fetch transactions: {e}")

    def delete_transaction(self):
        """
        Admin kisi bhi transaction ko delete kar sakta hai.
        Pehle saare transactions dikhata hai, phir ID maangta hai.
        """
        # Pehle saare transactions dikhao
        self.view_all_transactions()

        print("\n🗑️ Delete Transaction (Admin)")
        print("-" * 30)
        txn_id = input("Enter Transaction ID to delete: ").strip()

        if not txn_id.isdigit():
            print("❌ Invalid Transaction ID!")
            return

        # Confirmation lo
        confirm = input("Are you sure? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Delete cancelled.")
            return

        # Transaction class ka admin delete method call karo
        self.transaction.delete_transaction_admin(int(txn_id))

    def generate_reports(self):
        """Reports class ka generate_report method call karta hai."""
        self.reports.generate_report()

    def admin_dashboard(self):
        """
        Admin dashboard — Menu loop chalata hai.
        Jab tak admin logout nahi karta, menu dikhata rahega.
        """
        while True:
            show_admin_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.view_all_users()
            elif choice == "2":
                self.view_all_transactions()
            elif choice == "3":
                self.delete_transaction()
            elif choice == "4":
                self.generate_reports()
            elif choice == "5":
                print("\n👋 Admin logged out.")
                break
            else:
                print("❌ Invalid choice! Please try again.")

            pause()
