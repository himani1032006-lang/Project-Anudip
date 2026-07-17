"""
auth.py
-------
Handles user registration, user login, and admin login.

Responsibility: Authentication only. It does not know anything about
transactions or reports - it just verifies identity and returns the
logged-in user's/admin's ID (or None if login fails).
"""

import psycopg2
from utils import is_valid_email, is_valid_phone, is_valid_password


class Authentication:
    """Handles registration and login for both users and admins."""

    def __init__(self, db):
        # db is a Database object (composition, not inheritance).
        self.db = db

    def register_user(self):
        """Register a new user after validating input and email uniqueness."""
        print_header = "\n--- User Registration ---"
        print(print_header)

        name = input("Enter your name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return

        email = input("Enter your email: ").strip()
        if not is_valid_email(email):
            print("Invalid email format.")
            return

        phone = input("Enter your phone number: ").strip()
        if not is_valid_phone(phone):
            print("Invalid phone number. Use digits only (7-15 digits).")
            return

        password = input("Enter a password (min 4 characters, no spaces): ").strip()
        if not is_valid_password(password):
            print("Password does not meet requirements.")
            return

        try:
            # Check email uniqueness before inserting.
            self.db.cursor.execute(
                "SELECT user_id FROM users WHERE email = %s;", (email,)
            )
            if self.db.cursor.fetchone():
                print("An account with this email already exists.")
                return

            self.db.cursor.execute(
                """INSERT INTO users (name, email, phone, password)
                   VALUES (%s, %s, %s, %s);""",
                (name, email, phone, password)
            )
            self.db.connection.commit()
            print("Registration successful! You can now log in.")

        except psycopg2.Error as error:
            self.db.connection.rollback()
            print(f"Error during registration: {error}")

    def login_user(self):
        """Log in a user with email and password. Returns user_id or None."""
        print("\n--- User Login ---")
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()

        try:
            self.db.cursor.execute(
                """SELECT user_id, name FROM users
                   WHERE email = %s AND password = %s;""",
                (email, password)
            )
            result = self.db.cursor.fetchone()

            if result:
                user_id, name = result
                print(f"Welcome back, {name}!")
                return user_id
            else:
                print("Invalid email or password.")
                return None

        except psycopg2.Error as error:
            print(f"Error during login: {error}")
            return None

    def login_admin(self):
        """Log in an admin with username and password. Returns admin_id or None."""
        print("\n--- Admin Login ---")
        username = input("Enter admin username: ").strip()
        password = input("Enter admin password: ").strip()

        try:
            self.db.cursor.execute(
                """SELECT admin_id FROM admins
                   WHERE username = %s AND password = %s;""",
                (username, password)
            )
            result = self.db.cursor.fetchone()

            if result:
                print("Admin login successful!")
                return result[0]
            else:
                print("Invalid admin credentials.")
                return None

        except psycopg2.Error as error:
            print(f"Error during admin login: {error}")
            return None
