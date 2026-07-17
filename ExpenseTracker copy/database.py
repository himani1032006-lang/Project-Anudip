"""
database.py
-----------
Handles the PostgreSQL connection and table creation.

Responsibility: Everything related to connecting to the database
and setting up the schema lives here. Other classes (User, Admin,
Transaction, Reports, Authentication) receive a Database object and
use its connection/cursor to run queries.
"""

import psycopg2
from config import DB_CONFIG, DEFAULT_ADMIN


class Database:
    """Manages the PostgreSQL connection and initial table setup."""

    def __init__(self):
        # self.connection and self.cursor are "protected" via naming
        # convention (encapsulation) - other classes should not touch
        # them directly; they should go through Database's methods.
        self.connection = None
        self.cursor = None
        self._connect()

    def _connect(self):
        """Create a connection to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            print("Connected to the database successfully.")
        except psycopg2.Error as error:
            print(f"Error connecting to the database: {error}")
            raise SystemExit("Cannot continue without a database connection.")

    def create_tables(self):
        """Create all required tables if they do not already exist."""
        try:
            # ---------- Users table ----------
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(15) NOT NULL,
                    password VARCHAR(100) NOT NULL
                );
            """)

            # ---------- Admins table ----------
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    admin_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL
                );
            """)

            # ---------- Transactions table ----------
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(user_id)
                        ON DELETE CASCADE,
                    transaction_type VARCHAR(10) NOT NULL
                        CHECK (transaction_type IN ('Income', 'Expense')),
                    category VARCHAR(50) NOT NULL,
                    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
                    description VARCHAR(255),
                    transaction_date DATE NOT NULL DEFAULT CURRENT_DATE
                );
            """)

            self.connection.commit()
            print("Tables are ready.")

            self._seed_default_admin()

        except psycopg2.Error as error:
            self.connection.rollback()
            print(f"Error creating tables: {error}")

    def _seed_default_admin(self):
        """Insert a default admin account if the admins table is empty."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM admins;")
            count = self.cursor.fetchone()[0]

            if count == 0:
                self.cursor.execute(
                    "INSERT INTO admins (username, password) VALUES (%s, %s);",
                    (DEFAULT_ADMIN["username"], DEFAULT_ADMIN["password"])
                )
                self.connection.commit()
                print(
                    f"Default admin created -> "
                    f"username: {DEFAULT_ADMIN['username']}, "
                    f"password: {DEFAULT_ADMIN['password']}"
                )
        except psycopg2.Error as error:
            self.connection.rollback()
            print(f"Error seeding default admin: {error}")

    def close(self):
        """Close the cursor and connection cleanly."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")
