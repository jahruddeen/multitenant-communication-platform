from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict
)


# --------------------------------
# COMPANY REGISTRATION
# --------------------------------

class CompanyRegister(BaseModel):

    company_name: str = Field(
        min_length=2,
        max_length=150
    )

    email: EmailStr

    full_name: str = Field(
        min_length=2,
        max_length=150
    )

    password: str = Field(
        min_length=10,
        max_length=128
    )


# --------------------------------
# USER RESPONSE
# --------------------------------

class UserOut(BaseModel):

    id: int
    company_id: int
    email: EmailStr
    full_name: str
    role: str

    model_config = ConfigDict(
        from_attributes=True
    )


# --------------------------------
# JWT TOKEN
# --------------------------------

class Token(BaseModel):

    access_token: str

    token_type: str = "bearer"


# --------------------------------
# CONTACT CREATE
# --------------------------------

class ContactCreate(BaseModel):

    phone: str = Field(
        pattern=r"^\+?[1-9]\d{7,14}$"
    )

    name: str = Field(
        default="",
        max_length=150
    )

    sms_consent: bool = False

    voice_consent: bool = False


# --------------------------------
# CONTACT UPDATE
# --------------------------------

class ContactUpdate(BaseModel):

    name: Optional[str] = None

    sms_consent: Optional[bool] = None

    voice_consent: Optional[bool] = None

    opted_out: Optional[bool] = None


# --------------------------------
# CONTACT RESPONSE
# --------------------------------

class ContactOut(BaseModel):

    id: int
    company_id: int
    phone: str
    name: str

    sms_consent: bool
    voice_consent: bool
    opted_out: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# --------------------------------
# SMS REQUEST
# --------------------------------

class SMSRequest(BaseModel):

    contact_id: int

    message: str = Field(
        min_length=1,
        max_length=1000
    )


# --------------------------------
# VOICE CALL REQUEST
# --------------------------------

class CallRequest(BaseModel):

    contact_id: int


# --------------------------------
# NOTIFICATION RESPONSE
# --------------------------------

class NotificationOut(BaseModel):

    id: int

    contact_id: int

    channel: str

    status: str

    attempt: int

    message: Optional[str] = None

    error: Optional[str] = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )