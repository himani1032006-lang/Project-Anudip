"""
main.py
-------
Entry point of the Expense Tracker CLI application.
Displays the main menu and routes the user to the correct
dashboard (User or Admin) after successful login.

Run with: python main.py
"""

from database import Database
from auth import Authentication
from user import User
from admin import Admin


def user_dashboard(db, user_id):
    """Show the menu for a logged-in user and handle their choices."""
    current_user = User(db, user_id)

    while True:
        print("\n----- User Dashboard -----")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Search Transaction")
        print("5. Update Transaction")
        print("6. Delete Transaction")
        print("7. View Balance")
        print("8. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            current_user.add_income()
        elif choice == "2":
            current_user.add_expense()
        elif choice == "3":
            current_user.view_transactions()
        elif choice == "4":
            current_user.search_transaction()
        elif choice == "5":
            current_user.update_transaction()
        elif choice == "6":
            current_user.delete_transaction()
        elif choice == "7":
            current_user.view_balance()
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def admin_dashboard(db, admin_id):
    """Show the menu for a logged-in admin and handle their choices."""
    current_admin = Admin(db, admin_id)

    while True:
        print("\n----- Admin Dashboard -----")
        print("1. View Users")
        print("2. View Transactions")
        print("3. Delete Transaction")
        print("4. Generate Reports")
        print("5. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            current_admin.view_users()
        elif choice == "2":
            current_admin.view_all_transactions()
        elif choice == "3":
            current_admin.delete_transaction()
        elif choice == "4":
            current_admin.generate_reports()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    """Main program loop: shows the main menu until the user exits."""
    db = Database()
    db.create_tables()
    auth = Authentication(db)

    try:
        while True:
            print("\n===== Expense Tracker =====")
            print("1. Register")
            print("2. User Login")
            print("3. Admin Login")
            print("4. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                auth.register_user()
            elif choice == "2":
                user_id = auth.login_user()
                if user_id:
                    user_dashboard(db, user_id)
            elif choice == "3":
                admin_id = auth.login_admin()
                if admin_id:
                    admin_dashboard(db, admin_id)
            elif choice == "4":
                print("Thank you for using Expense Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    finally:
        # Always close the database connection, even if an error occurs.
        db.close()


if __name__ == "__main__":
    main()
