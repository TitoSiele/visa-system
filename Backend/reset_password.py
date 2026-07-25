from database import SessionLocal
import models, crud

db = SessionLocal()

email = "titussiele5@gmail.com"
new_password = "1234"  # set whatever you want, remember it

user = db.query(models.User).filter(models.User.email == email).first()

if user:
    user.hashed_password = crud.pwd_context.hash(new_password)
    db.commit()
    print(f"Password for {email} reset to: {new_password}")
else:
    print("No user found with that email")

db.close()