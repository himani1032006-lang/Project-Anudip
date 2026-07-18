# ============================================
# transaction.py — Transaction CRUD Operations
# ============================================
# Is file mein Transaction class hai jo income/expense
# add, view, search, update, delete karta hai.

from utils import validate_amount, get_category_choice, display_transactions


class Transaction:
    """
    Transaction class — Transactions ka CRUD (Create, Read, Update, Delete)
    handle karta hai.
    """

    def __init__(self, db):
        """
        Constructor — Database object receive karta hai.
        """
        self.db = db

    def add_transaction(self, user_id, transaction_type):
        """
        Naya transaction add karta hai (Income ya Expense).
        User se category, amount, aur description leta hai.
        """
        print(f"\n💵 Add {transaction_type}")
        print("-" * 30)

        # ---- Category select karwao ----
        category = get_category_choice(transaction_type)

        # ---- Amount input ----
        amount_str = input("Enter amount: ₹")
        amount = validate_amount(amount_str)
        if amount is None:
            return

        # ---- Description input (optional) ----
        description = input("Enter description (optional): ").strip()
        if not description:
            description = f"{transaction_type} - {category}"

        # ---- Database mein insert karo ----
        try:
            self.db.cursor.execute("""
                INSERT INTO transactions 
                (user_id, transaction_type, category, amount, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, transaction_type, category, amount, description))

            print(f"\n✅ {transaction_type} of ₹{amount} added successfully!")

        except Exception as e:
            print(f"❌ Failed to add transaction: {e}")

    def view_transactions(self, user_id):
        """
        Ek user ke saare transactions dikhata hai.
        ORDER BY date DESC — latest pehle dikhe.
        """
        try:
            self.db.cursor.execute("""
                SELECT transaction_id, transaction_type, category, 
                       amount, description, transaction_date
                FROM transactions 
                WHERE user_id = %s 
                ORDER BY transaction_date DESC, transaction_id DESC
            """, (user_id,))

            transactions = self.db.cursor.fetchall()
            print(f"\n📋 Your Transactions:")
            display_transactions(transactions)

        except Exception as e:
            print(f"❌ Failed to fetch transactions: {e}")

    def search_transaction(self, user_id):
        """
        Transactions search karta hai category ya description se.
        LIKE operator use karta hai — partial match bhi milega.
        """
        print("\n🔍 Search Transaction")
        print("-" * 30)
        keyword = input("Enter search keyword (category/description): ").strip()

        if not keyword:
            print("❌ Please enter a keyword to search!")
            return

        try:
            # LIKE operator se partial matching
            # % keyword ke aage peeche lagaya — kahin bhi match hoga
            self.db.cursor.execute("""
                SELECT transaction_id, transaction_type, category,
                       amount, description, transaction_date
                FROM transactions
                WHERE user_id = %s 
                  AND (category ILIKE %s OR description ILIKE %s)
                ORDER BY transaction_date DESC
            """, (user_id, f"%{keyword}%", f"%{keyword}%"))

            transactions = self.db.cursor.fetchall()
            print(f"\n🔍 Search Results for '{keyword}':")
            display_transactions(transactions)

        except Exception as e:
            print(f"❌ Search failed: {e}")

    def update_transaction(self, user_id):
        """
        Existing transaction update karta hai.
        Pehle user apna transaction select karta hai,
        phir naye values deta hai.
        """
        # Pehle saare transactions dikhao
        self.view_transactions(user_id)

        print("\n✏️ Update Transaction")
        print("-" * 30)
        txn_id = input("Enter Transaction ID to update: ").strip()

        if not txn_id.isdigit():
            print("❌ Invalid Transaction ID!")
            return

        try:
            # Pehle check karo ki ye transaction is user ka hai ya nahi
            self.db.cursor.execute("""
                SELECT transaction_id, transaction_type, category, 
                       amount, description
                FROM transactions 
                WHERE transaction_id = %s AND user_id = %s
            """, (txn_id, user_id))

            txn = self.db.cursor.fetchone()

            if not txn:
                print("❌ Transaction not found or doesn't belong to you!")
                return

            # Current values dikhao
            print(f"\nCurrent Type: {txn[1]}")
            print(f"Current Category: {txn[2]}")
            print(f"Current Amount: ₹{txn[3]}")
            print(f"Current Description: {txn[4]}")

            # ---- Naye values lo (Enter = skip = purana value) ----
            print("\n(Press Enter to keep current value)")

            # Transaction type update
            print(f"\nTransaction Type [{txn[1]}]:")
            print("  1. Income")
            print("  2. Expense")
            type_choice = input("Enter choice (or press Enter to skip): ").strip()

            if type_choice == "1":
                new_type = "Income"
            elif type_choice == "2":
                new_type = "Expense"
            else:
                new_type = txn[1]  # Purana value rakho

            # Category update
            new_category = get_category_choice(new_type)

            # Amount update
            amount_input = input(f"New amount [₹{txn[3]}]: ").strip()
            if amount_input:
                new_amount = validate_amount(amount_input)
                if new_amount is None:
                    return
            else:
                new_amount = txn[3]

            # Description update
            new_desc = input(f"New description [{txn[4]}]: ").strip()
            if not new_desc:
                new_desc = txn[4]

            # ---- Database update karo ----
            self.db.cursor.execute("""
                UPDATE transactions 
                SET transaction_type = %s, category = %s, 
                    amount = %s, description = %s
                WHERE transaction_id = %s AND user_id = %s
            """, (new_type, new_category, new_amount, new_desc, txn_id, user_id))

            print("\n✅ Transaction updated successfully!")

        except Exception as e:
            print(f"❌ Update failed: {e}")

    def delete_transaction(self, user_id):
        """
        Transaction delete karta hai ID se.
        Sirf apna transaction delete kar sakta hai user.
        """
        # Pehle transactions dikhao
        self.view_transactions(user_id)

        print("\n🗑️ Delete Transaction")
        print("-" * 30)
        txn_id = input("Enter Transaction ID to delete: ").strip()

        if not txn_id.isdigit():
            print("❌ Invalid Transaction ID!")
            return

        try:
            # Check karo ki transaction exist karta hai aur is user ka hai
            self.db.cursor.execute("""
                SELECT transaction_id FROM transactions 
                WHERE transaction_id = %s AND user_id = %s
            """, (txn_id, user_id))

            if not self.db.cursor.fetchone():
                print("❌ Transaction not found or doesn't belong to you!")
                return

            # Confirmation lo
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Delete cancelled.")
                return

            # Delete karo
            self.db.cursor.execute(
                "DELETE FROM transactions WHERE transaction_id = %s AND user_id = %s",
                (txn_id, user_id)
            )
            print("\n✅ Transaction deleted successfully!")

        except Exception as e:
            print(f"❌ Delete failed: {e}")

    def delete_transaction_admin(self, txn_id):
        """
        Admin ke liye — kisi bhi transaction ko delete kar sakta hai.
        """
        try:
            # Check karo ki transaction exist karta hai
            self.db.cursor.execute(
                "SELECT transaction_id FROM transactions WHERE transaction_id = %s",
                (txn_id,)
            )

            if not self.db.cursor.fetchone():
                print("❌ Transaction not found!")
                return

            # Delete karo
            self.db.cursor.execute(
                "DELETE FROM transactions WHERE transaction_id = %s",
                (txn_id,)
            )
            print("\n✅ Transaction deleted by admin!")

        except Exception as e:
            print(f"❌ Delete failed: {e}")
