from getpass import getpass

from backend.auth import hash_password
from backend.database import get_connection


ADMIN_EMAIL = "Kanoohanan@gmail.com"


def create_admin():
    password = getpass("Enter admin password: ")
    confirm_password = getpass("Confirm admin password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    if len(password) < 8:
        print("Password must be at least 8 characters.")
        return

    password_hash, salt = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

    existing = cursor.execute(
        "SELECT id FROM admin_users WHERE email = ?",
        (ADMIN_EMAIL,)
    ).fetchone()

    if existing:
        print("Admin account already exists.")
        connection.close()
        return

    cursor.execute(
        """
        INSERT INTO admin_users (email, password_hash, salt)
        VALUES (?, ?, ?)
        """,
        (ADMIN_EMAIL, password_hash, salt)
    )

    connection.commit()
    connection.close()

    print("Admin account created successfully.")


if __name__ == "__main__":
    create_admin()