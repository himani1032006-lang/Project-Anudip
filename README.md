# Project-Anudip
# Expense Tracker (CLI + PostgreSQL)

A beginner-friendly, command-line Expense Tracker built with Python (OOP)
and PostgreSQL. No web frameworks or GUIs — pure CLI.

## Features

**Users can:**
- Register and log in
- Add income and expenses
- View, search, update, and delete their transactions
- View total income, total expenses, and current balance

**Admins can:**
- Log in with admin credentials
- View all registered users
- View all transactions across users
- Delete any transaction
- Generate a system-wide report (totals, category breakdowns)

## Tech Stack

- Python 3.x
- PostgreSQL
- psycopg2 (raw SQL, no ORM)

## Project Structure

```
ExpenseTracker/
├── config.py        # DB connection settings
├── database.py       # Database class: connection + table creation
├── auth.py            # Authentication class: register/login
├── user.py            # User class: user dashboard logic
├── admin.py           # Admin class: admin dashboard logic
├── transaction.py      # Transaction class: all transaction SQL
├── reports.py          # Reports class: aggregated reports
├── utils.py            # Shared helper/validation functions
├── main.py             # CLI entry point (run this file)
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Install PostgreSQL
Make sure PostgreSQL is installed and running on your machine.

### 2. Create the database
```sql
CREATE DATABASE expense_tracker;
```

### 3. Configure connection settings
Copy the example config file and fill in your own credentials:

```bash
cp config.example.py config.py
```

Then open `config.py` and update `DB_CONFIG` with your PostgreSQL username,
password, host, and port. `config.py` is listed in `.gitignore`, so your
real password will never be pushed to GitHub.

```python
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "expense_tracker",
    "user": "postgres",
    "password": "your_password_here"
}
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the application
```bash
python main.py
```

The required tables (`users`, `admins`, `transactions`) are created
automatically the first time you run the app. A default admin account
is also created automatically:

```
username: admin
password: admin123
```

You can change these defaults in `config.py` before first run, or
update the `admins` table directly afterward.

## Menu Overview

**Main Menu**
```
1. Register
2. User Login
3. Admin Login
4. Exit
```

**User Dashboard**
```
1. Add Income
2. Add Expense
3. View Transactions
4. Search Transaction
5. Update Transaction
6. Delete Transaction
7. View Balance
8. Logout
```

**Admin Dashboard**
```
1. View Users
2. View Transactions
3. Delete Transaction
4. Generate Reports
5. Logout
```

## Notes

- Passwords are stored in plain text for simplicity (no hashing), as
  this is intended as a learning project. Do not use this approach in
  a production application.
- All SQL queries use parameterized statements (`%s` placeholders) to
  prevent SQL injection.
- Each class has a single, clear responsibility (Database, Authentication,
  User, Admin, Transaction, Reports), which keeps the code modular and
  easy to extend.
