from database import SessionLocal
import models

db = SessionLocal()
users = db.query(models.User).all()

if not users:
    print("No users found in the database at all.")
else:
    for u in users:
        print(f"Email: {u.email} | Role: {u.role} | Name: {u.full_name}")

db.close()