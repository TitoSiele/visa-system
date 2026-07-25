from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="applicant")  # applicant, officer, admin

    # --- Personal details ---
    country_of_origin = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)   # stored as "YYYY-MM-DD"
    passport_number = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)

    applications = relationship("Application", back_populates="owner")


class VisaType(Base):
    __tablename__ = "visa_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # e.g., 'Student Visa'
    description = Column(String)
    required_documents = Column(JSON)  # e.g., ["Passport", "Bank Statement"]


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    visa_type_id = Column(Integer, ForeignKey("visa_types.id"))
    status = Column(String, default="Submitted")  # Pending, Approved, Rejected, More Info
    submitted_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    owner = relationship("User", back_populates="applications")
    documents = relationship("Document", back_populates="application")
    visa_type = relationship("VisaType")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    file_path = Column(String, nullable=False)  # Storage location
    document_type = Column(String)  # e.g., 'Passport'
    verified = Column(Boolean, default=False)

    application = relationship("Application", back_populates="documents")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    amount = Column(Integer, nullable=False)  # KES, whole numbers only for M-Pesa
    phone_number = Column(String, nullable=False)
    status = Column(String, default="Pending")  # Pending, Completed, Failed
    checkout_request_id = Column(String, nullable=True, index=True)
    mpesa_receipt_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    application = relationship("Application")