# ============================================
# utils.py — Helper Functions & Validation
# ============================================
# Is file mein input validation aur menu display
# ke liye helper functions hain.

import os
import re


# ---- Category Lists ----
# Income aur Expense ke categories yahan define hain

INCOME_CATEGORIES = ["Salary", "Freelancing", "Business", "Other"]
EXPENSE_CATEGORIES = ["Food", "Shopping", "Bills", "Travel", "Entertainment", "Other"]


def clear_screen():
    """Terminal screen clear karta hai."""
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """User se Enter press karwata hai — taki output padh sake."""
    input("\n⏎ Press Enter to continue...")


def validate_email(email):
    """
    Email format check karta hai.
    Simple regex use kar rahe hain — basic validation ke liye kaafi hai.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        print("❌ Invalid email format!")
        return False


def validate_phone(phone):
    """Phone number validate karta hai — sirf 10 digits allowed."""
    if phone.isdigit() and len(phone) == 10:
        return True
    else:
        print("❌ Phone number must be exactly 10 digits!")
        return False


def validate_password(password):
    """Password length check — minimum 4 characters."""
    if len(password) >= 4:
        return True
    else:
        print("❌ Password must be at least 4 characters!")
        return False


def validate_amount(amount_str):
    """
    Amount validate karta hai — positive number hona chahiye.
    Returns float value if valid, None if invalid.
    """
    try:
        amount = float(amount_str)
        if amount > 0:
            return amount
        else:
            print("❌ Amount must be greater than 0!")
            return None
    except ValueError:
        print("❌ Invalid amount! Please enter a number.")
        return None


def validate_name(name):
    """Name empty nahi hona chahiye."""
    if len(name.strip()) >= 2:
        return True
    else:
        print("❌ Name must be at least 2 characters!")
        return False


def get_category_choice(transaction_type):
    """
    Transaction type ke hisaab se category choose karwata hai.
    Income ke liye Income categories, Expense ke liye Expense categories.
    """
    if transaction_type == "Income":
        categories = INCOME_CATEGORIES
    else:
        categories = EXPENSE_CATEGORIES

    print(f"\n📂 Select {transaction_type} Category:")
    print("-" * 30)

    # Har category ko number ke saath display karo
    for i, category in enumerate(categories, 1):
        print(f"  {i}. {category}")

    while True:
        choice = input("\nEnter choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]
        else:
            print("❌ Invalid choice! Try again.")


def display_transactions(transactions):
    """
    Transactions ko table format mein display karta hai.
    Agar koi transaction nahi hai to message dikhata hai.
    """
    if not transactions:
        print("\n📭 No transactions found!")
        return

    # Table header
    print("\n" + "=" * 95)
    print(f"{'ID':<6} {'Type':<10} {'Category':<15} {'Amount':<12} {'Description':<25} {'Date':<12}")
    print("=" * 95)

    # Har transaction print karo
    for txn in transactions:
        print(f"{txn[0]:<6} {txn[1]:<10} {txn[2]:<15} ₹{txn[3]:<11} {txn[4]:<25} {txn[5]}")

    print("=" * 95)
    print(f"Total Transactions: {len(transactions)}")


def show_main_menu():
    """Main menu display karta hai."""
    print("\n" + "=" * 40)
    print("   💰 EXPENSE TRACKER SYSTEM 💰")
    print("=" * 40)
    print("  1. Register")
    print("  2. User Login")
    print("  3. Admin Login")
    print("  4. Exit")
    print("=" * 40)


def show_user_menu(name):
    """User dashboard menu display karta hai."""
    print("\n" + "=" * 40)
    print(f"   👤 Welcome, {name}!")
    print("=" * 40)
    print("  1. Add Income")
    print("  2. Add Expense")
    print("  3. View Transactions")
    print("  4. Search Transaction")
    print("  5. Update Transaction")
    print("  6. Delete Transaction")
    print("  7. View Balance")
    print("  8. Logout")
    print("=" * 40)


def show_admin_menu():
    """Admin dashboard menu display karta hai."""
    print("\n" + "=" * 40)
    print("   🔑 ADMIN DASHBOARD")
    print("=" * 40)
    print("  1. View All Users")
    print("  2. View All Transactions")
    print("  3. Delete Transaction")
    print("  4. Generate Reports")
    print("  5. Logout")
    print("=" * 40)
