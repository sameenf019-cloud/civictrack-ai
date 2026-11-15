import getpass

from app.database import SessionLocal
from app.models import User, UserRole
from app.security import hash_password


def main():
    role_name = input("Role (admin/officer): ").strip().lower()
    if role_name not in ("admin", "officer"):
        print("Role must be admin or officer.")
        return

    full_name = input("Full name: ").strip()
    email = input("Email: ").strip().lower()
    password = getpass.getpass("Password (min 8 chars, hidden): ")
    if len(full_name) < 2 or "@" not in email or len(password) < 8:
        print("Invalid input. Nothing was saved.")
        return

    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == email).first():
            print("This email already exists. Nothing was saved.")
            return
        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            role=UserRole(role_name),
        )
        db.add(user)
        db.commit()
        print(f"Created {role_name}: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()