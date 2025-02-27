from hh2e_external_data_model.db_connector import SessionLocal
from hh2e_external_data_model.models import User


def main() -> None:
    db = SessionLocal()

    # Create user
    new_user = User(name="John Doe", email="imran@example.com")
    db.add(new_user)
    db.commit()

    # Query users
    users = db.query(User).all()
    print(f"Users in DB: {users}")


if __name__ == "__main__":
    main()
