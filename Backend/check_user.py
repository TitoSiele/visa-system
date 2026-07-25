from database import SessionLocal
import models

db = SessionLocal()

passport = "A1356789"
user = db.query(models.User).filter(models.User.passport_number == passport).first()

if user:
    print("Found user:")
    print("Name:", user.full_name)
    print("Email:", user.email)
    print("Country:", user.country_of_origin)
    print("DOB:", user.date_of_birth)
    print("Passport:", user.passport_number)
    print("Phone:", user.phone_number)
    print("Address:", user.address)
else:
    print("No user found with that passport number")

db.close()