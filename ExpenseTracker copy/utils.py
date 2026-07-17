"""
utils.py
--------
Small reusable helper functions used across the project:
input validation, formatted printing, etc.

Keeping these in one place avoids repeating the same validation
code in auth.py, user.py, admin.py, etc.
"""

import re

INCOME_CATEGORIES = ["Salary", "Freelancing", "Business", "Other"]
EXPENSE_CATEGORIES = ["Food", "Shopping", "Bills", "Travel", "Entertainment", "Other"]


def is_valid_email(email):
    """Very simple email format check."""
    pattern = r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """Phone number must be digits only, 7-15 characters long."""
    return phone.isdigit() and 7 <= len(phone) <= 15


def is_valid_password(password):
    """Basic password rule: at least 4 characters, no spaces."""
    return len(password) >= 4 and " " not in password


def get_valid_amount():
    """Ask the user for a positive amount and validate it."""
    while True:
        value = input("Enter amount: ").strip()
        try:
            amount = float(value)
            if amount <= 0:
                print("Amount must be greater than 0. Try again.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number.")


def get_valid_category(transaction_type):
    """Show category options based on transaction type and validate choice."""
    categories = INCOME_CATEGORIES if transaction_type == "Income" else EXPENSE_CATEGORIES

    print("Choose a category:")
    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    while True:
        choice = input("Enter category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]
        print("Invalid choice. Try again.")


def print_transaction_row(row):
    """Print a single transaction row in a readable format.
    Expected row order:
    transaction_id, transaction_type, category, amount, description, transaction_date
    """
    transaction_id, transaction_type, category, amount, description, transaction_date = row
    print(
        f"ID: {transaction_id} | {transaction_type:7} | {category:12} | "
        f"Amount: {amount:10.2f} | Date: {transaction_date} | "
        f"Note: {description if description else '-'}"
    )


def print_header(title):
    """Print a simple section header for readability in the CLI."""
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)
