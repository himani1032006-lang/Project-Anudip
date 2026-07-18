# ============================================
# main.py — Main Entry Point
# ============================================
# Ye file program ka starting point hai.
# Yahan se Main Menu chalti hai aur user ko
# Register, Login, ya Admin Login ka option milta hai.

from database import Database
from auth import Authentication
from user import User
from admin import Admin
from utils import show_main_menu, pause, clear_screen


def main():
    """
    Main function — Program yahan se start hota hai.
    Database connect karta hai, tables banata hai,
    aur Main Menu loop chalata hai.
    """

    # ---- Database Setup ----
    # Database object banao — connection establish hoga
    db = Database()
    # Tables create karo agar pehle se nahi hain
    db.create_tables()

    # ---- Authentication object banao ----
    auth = Authentication(db)

    print("\n🎉 Welcome to Expense Tracker System!")

    # ---- Main Menu Loop ----
    while True:
        show_main_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # ---- User Registration ----
            auth.register_user()
            pause()

        elif choice == "2":
            # ---- User Login ----
            user_data = auth.login_user()

            if user_data:
                # Login successful — User dashboard pe jao
                # user_data = (user_id, name)
                user = User(db, user_data[0], user_data[1])
                user.user_dashboard()

        elif choice == "3":
            # ---- Admin Login ----
            is_admin = auth.login_admin()

            if is_admin:
                # Admin login successful — Admin dashboard pe jao
                admin = Admin(db)
                admin.admin_dashboard()

        elif choice == "4":
            # ---- Exit ----
            print("\n👋 Thank you for using Expense Tracker!")
            print("   Made with ❤️ by Jitendra Kumar Lal")
            db.close_connection()
            break

        else:
            print("❌ Invalid choice! Please try again.")
            pause()


# ---- Program Start ----
# Ye check karta hai ki file directly run ho rahi hai
# ya kisi aur file ne import kari hai
if __name__ == "__main__":
    main()
    
