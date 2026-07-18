# ============================================
# database.py — Database Connection & Setup
# ============================================
# Is file mein Database class hai jo PostgreSQL se
# connection banata hai aur tables create karta hai.

import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class Database:
    """
    Database class — PostgreSQL se connect karta hai
    aur zaroori tables banata hai.
    """

    def __init__(self):
        """Constructor — Database se connection establish karta hai."""
        try:
            self.connection = psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            # autocommit ON — har query turant save hogi
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print("✅ Database se connection successful!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            exit()

    def create_tables(self):
        """Zaroori tables banata hai agar pehle se nahi hain."""
        try:
            # ---- Users Table ----
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(15) NOT NULL,
                    password VARCHAR(50) NOT NULL
                )
            """)

            # ---- Admins Table ----
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    admin_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(50) NOT NULL
                )
            """)

            # ---- Transactions Table ----
            # user_id FOREIGN KEY hai — users table se linked
            # CHECK constraint se sirf 'Income' ya 'Expense' allowed hai
            # amount > 0 hona chahiye
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(user_id),
                    transaction_type VARCHAR(10) NOT NULL 
                        CHECK (transaction_type IN ('Income', 'Expense')),
                    category VARCHAR(50) NOT NULL,
                    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
                    description VARCHAR(200),
                    transaction_date DATE DEFAULT CURRENT_DATE NOT NULL
                )
            """)

            # ---- Default Admin Insert ----
            # Pehle check karo ki admin already hai ya nahi
            self.cursor.execute(
                "SELECT * FROM admins WHERE username = %s", ("admin",)
            )
            if self.cursor.fetchone() is None:
                self.cursor.execute(
                    "INSERT INTO admins (username, password) VALUES (%s, %s)",
                    ("admin", "admin123")
                )
                print("👤 Default admin created (username: admin, password: admin123)")

            print("✅ All tables are ready!")

        except Exception as e:
            print(f"❌ Table creation failed: {e}")

    def close_connection(self):
        """Database connection close karta hai."""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("🔒 Database connection closed.")
