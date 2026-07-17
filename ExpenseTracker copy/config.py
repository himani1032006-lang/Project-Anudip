"""
config.py
---------
Stores database connection settings for the Expense Tracker application.

NOTE: For a real project, avoid hardcoding passwords in source code.
Here we keep it simple (beginner-friendly) but you can switch to
environment variables later using os.getenv().
"""

DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "expense_tracker",
    "user": "jitendrakumarlal",
    "password": ""
}

# Default admin credentials (used only to seed the admins table the first
# time the program runs, if no admin exists yet).
DEFAULT_ADMIN = {
    "username": "admin",
    "password": "admin123"
}
