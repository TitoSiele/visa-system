from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

# Security: Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        country_of_origin=user.country_of_origin,
        date_of_birth=user.date_of_birth,
        passport_number=user.passport_number,
        phone_number=user.phone_number,
        address=user.address,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_application(db: Session, application: schemas.ApplicationCreate, user_id: int):
    db_app = models.Application(**application.dict(), user_id=user_id)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def get_applications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Application).offset(skip).limit(limit).all()


def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()


def set_document_verified(db: Session, document_id: int, verified: bool):
    doc = get_document(db, document_id)
    if not doc:
        return None
    doc.verified = verified
    db.commit()
    db.refresh(doc)
    return doc


def get_all_applications(db: Session, status: str | None = None):
    query = db.query(models.Application)
    if status:
        query = query.filter(models.Application.status == status)
    return query.all()


def update_application_status(db: Session, app_id: int, new_status: str):
    application = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not application:
        return None
    application.status = new_status
    db.commit()
    db.refresh(application)
    return application


def create_payment(db: Session, application_id: int, amount: int, phone_number: str, checkout_request_id: str | None = None):
    payment = models.Payment(
        application_id=application_id,
        amount=amount,
        phone_number=phone_number,
        checkout_request_id=checkout_request_id,
        status="Pending",
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment_by_checkout_id(db: Session, checkout_request_id: str):
    return db.query(models.Payment).filter(
        models.Payment.checkout_request_id == checkout_request_id
    ).first()


def update_payment_status(db: Session, payment_id: int, status: str, mpesa_receipt_number: str | None = None):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        return None
    payment.status = status
    if mpesa_receipt_number:
        payment.mpesa_receipt_number = mpesa_receipt_number
    db.commit()
    db.refresh(payment)
    return payment