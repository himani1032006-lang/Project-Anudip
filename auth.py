# ============================================
# auth.py — Authentication Module
# ============================================
# Is file mein Authentication class hai jo user
# registration, user login, aur admin login handle karta hai.

from utils import validate_email, validate_phone, validate_password, validate_name


class Authentication:
    """
    Authentication class — Register aur Login ka kaam karta hai.
    """

    def __init__(self, db):
        """
        Constructor — Database object receive karta hai.
        Isse hum database queries run kar paayenge.
        """
        self.db = db

    def register_user(self):
        """
        Naya user register karta hai.
        Name, email, phone, password leke database mein save karta hai.
        """
        print("\n" + "=" * 40)
        print("   📝 USER REGISTRATION")
        print("=" * 40)

        # ---- Name Input ----
        name = input("Enter your name: ").strip()
        if not validate_name(name):
            return

        # ---- Email Input ----
        email = input("Enter your email: ").strip().lower()
        if not validate_email(email):
            return

        # ---- Phone Input ----
        phone = input("Enter your phone (10 digits): ").strip()
        if not validate_phone(phone):
            return

        # ---- Password Input ----
        password = input("Enter password (min 4 chars): ").strip()
        if not validate_password(password):
            return

        # ---- Database mein insert karo ----
        try:
            # Pehle check karo ki email already exist karti hai ya nahi
            self.db.cursor.execute(
                "SELECT email FROM users WHERE email = %s", (email,)
            )
            if self.db.cursor.fetchone():
                print("❌ This email is already registered!")
                return

            # User insert karo
            self.db.cursor.execute(
                "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
                (name, email, phone, password)
            )
            print(f"\n✅ Registration successful! Welcome, {name}!")

        except Exception as e:
            print(f"❌ Registration failed: {e}")

    def login_user(self):
        """
        User login karta hai email aur password se.
        Successful login pe (user_id, name) return karta hai.
        Failed login pe None return karta hai.
        """
        print("\n" + "=" * 40)
        print("   🔐 USER LOGIN")
        print("=" * 40)

        email = input("Enter your email: ").strip().lower()
        password = input("Enter your password: ").strip()

        try:
            # Email aur password dono match karo
            self.db.cursor.execute(
                "SELECT user_id, name FROM users WHERE email = %s AND password = %s",
                (email, password)
            )
            user = self.db.cursor.fetchone()

            if user:
                print(f"\n✅ Login successful! Welcome back, {user[1]}!")
                # (user_id, name) return karo
                return user
            else:
                print("❌ Invalid email or password!")
                return None

        except Exception as e:
            print(f"❌ Login failed: {e}")
            return None

    def login_admin(self):
        """
        Admin login karta hai username aur password se.
        Successful login pe True return karta hai.
        Failed login pe False return karta hai.
        """
        print("\n" + "=" * 40)
        print("   🔑 ADMIN LOGIN")
        print("=" * 40)

        username = input("Enter admin username: ").strip()
        password = input("Enter admin password: ").strip()

        try:
            # Admin credentials check karo
            self.db.cursor.execute(
                "SELECT admin_id FROM admins WHERE username = %s AND password = %s",
                (username, password)
            )
            admin = self.db.cursor.fetchone()

            if admin:
                print("\n✅ Admin login successful!")
                return True
            else:
                print("❌ Invalid admin credentials!")
                return False

        except Exception as e:
            print(f"❌ Admin login failed: {e}")
            return False
