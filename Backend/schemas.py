from pydantic import EmailStr, BaseModel, field_validator
from typing import List, Optional
from datetime import datetime


# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    country_of_origin: Optional[str] = None
    date_of_birth: Optional[str] = None
    passport_number: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None


class UserCreate(UserBase):
    password: str  # Only used when creating a user

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --- Application Schemas ---
class ApplicationBase(BaseModel):
    visa_type_id: int


class ApplicationCreate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: int
    user_id: int
    status: str
    submitted_at: datetime

    class Config:
        from_attributes = True


class ApplicationStatusUpdate(BaseModel):
    status: str  # "Approved", "Rejected", "More Info", "Pending"


class ApplicationAdminOut(BaseModel):
    id: int
    user_id: int
    applicant_name: str
    applicant_email: str
    visa_type_name: str
    status: str
    submitted_at: Optional[datetime]


# --- Visa Type Schemas ---
class VisaType(BaseModel):
    id: int
    name: str
    required_documents: List[str]

    class Config:
        from_attributes = True


# --- Document Schemas ---
class DocumentVerify(BaseModel):
    verified: bool


class DocumentOut(BaseModel):
    id: int
    application_id: int
    document_type: str
    file_path: str
    verified: bool

    class Config:
        from_attributes = True


# --- Payment Schemas ---
class PaymentInitiate(BaseModel):
    application_id: int
    amount: int
    phone_number: str  # e.g. 0712345678


class PaymentOut(BaseModel):
    id: int
    application_id: int
    amount: int
    status: str
    checkout_request_id: Optional[str] = None

    class Config:
        from_attributes = True