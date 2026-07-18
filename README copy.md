# 💰 Expense Tracker System

A **Command Line Interface (CLI)** based Expense Tracker built using **Python (OOP)** and **PostgreSQL**.

This project helps users track their income and expenses with features like adding transactions, viewing balance, searching, updating, and deleting records. Admins can manage users and generate reports.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.x | Programming Language |
| PostgreSQL | Relational Database |
| psycopg2 | PostgreSQL adapter for Python |

---

## 📁 Project Structure

```
Expense-tracker/
├── config.py          # Database connection settings
├── database.py        # Database class — connection & table creation
├── auth.py            # Authentication — Register & Login
├── user.py            # User dashboard & operations
├── admin.py           # Admin dashboard & operations
├── transaction.py     # Transaction CRUD operations
├── reports.py         # Report generation
├── utils.py           # Helper functions & input validation
├── main.py            # Entry point — Main menu
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## ✨ Features

### 👤 User Features
- Register & Login
- Add Income / Expense
- View all transactions
- Search transactions by keyword
- Update existing transactions
- Delete transactions
- View balance summary (Income - Expense)

### 🔑 Admin Features
- Admin Login
- View all registered users
- View all transactions (with user names)
- Delete any transaction
- Generate detailed reports

### 📊 Reports
- Total Income & Expense
- Current Balance
- Income by Category
- Expense by Category
- Total Transaction Count

---

## 🐍 Python Concepts Used

- Classes & Objects
- Constructors (`__init__`)
- Encapsulation
- Methods
- Exception Handling (`try-except`)
- Modular Programming
- Functions, Loops, Conditionals

---

## 🗃️ Database Schema

### Users Table
| Column | Type | Constraints |
|--------|------|-------------|
| user_id | SERIAL | PRIMARY KEY |
| name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(100) | UNIQUE, NOT NULL |
| phone | VARCHAR(15) | NOT NULL |
| password | VARCHAR(50) | NOT NULL |

### Admins Table
| Column | Type | Constraints |
|--------|------|-------------|
| admin_id | SERIAL | PRIMARY KEY |
| username | VARCHAR(50) | UNIQUE, NOT NULL |
| password | VARCHAR(50) | NOT NULL |

### Transactions Table
| Column | Type | Constraints |
|--------|------|-------------|
| transaction_id | SERIAL | PRIMARY KEY |
| user_id | INTEGER | FOREIGN KEY → users |
| transaction_type | VARCHAR(10) | CHECK (Income/Expense) |
| category | VARCHAR(50) | NOT NULL |
| amount | NUMERIC(10,2) | CHECK (> 0) |
| description | VARCHAR(200) | — |
| transaction_date | DATE | DEFAULT CURRENT_DATE |

---

## 🚀 How to Run

### Prerequisites
- Python 3.x installed
- PostgreSQL installed and running
- `pip` package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/Expense-tracker.git
cd Expense-tracker
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Create PostgreSQL Database
Open your PostgreSQL terminal (psql) and run:
```sql
CREATE DATABASE expense_tracker;
```

### Step 4: Update Config (if needed)
Open `config.py` and update your PostgreSQL credentials:
```python
DB_NAME = "expense_tracker"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
```

### Step 5: Run the Application
```bash
python main.py
```

---

## 📸 Menu Screenshots

### Main Menu
```
========================================
   💰 EXPENSE TRACKER SYSTEM 💰
========================================
  1. Register
  2. User Login
  3. Admin Login
  4. Exit
========================================
```

### User Dashboard
```
========================================
   👤 Welcome, Jitendra!
========================================
  1. Add Income
  2. Add Expense
  3. View Transactions
  4. Search Transaction
  5. Update Transaction
  6. Delete Transaction
  7. View Balance
  8. Logout
========================================
```

### Admin Dashboard
```
========================================
   🔑 ADMIN DASHBOARD
========================================
  1. View All Users
  2. View All Transactions
  3. Delete Transaction
  4. Generate Reports
  5. Logout
========================================
```

---

## 👨‍💻 Default Admin Credentials

| Username | Password |
|----------|----------|
| admin | admin123 |

---

## 📝 SQL Operations Used

`CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `WHERE`, `ORDER BY`, `GROUP BY`, `COUNT`, `SUM`, `LIMIT`, `INNER JOIN`, `LEFT JOIN`, `ILIKE`

---

## 🤝 Contributing

This is a learning project. Feel free to fork and improve!

---

## 📄 License

This project is open source and available for educational purposes.

---

**Made with ❤️ by Jitendra Kumar Lal**
