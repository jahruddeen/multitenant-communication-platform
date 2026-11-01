
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
    Index
)

from sqlalchemy.orm import relationship

from apps.database import Base


def utcnow():
    return datetime.now(timezone.utc)


# --------------------------------
# COMPANY TABLE
# --------------------------------

class Company(Base):

    __tablename__ = "companies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=utcnow
    )

    users = relationship(
        "User",
        back_populates="company"
    )

    contacts = relationship(
        "Contact",
        back_populates="company"
    )


# --------------------------------
# USER TABLE
# --------------------------------

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True
    )

    email = Column(
        String(255),
        nullable=False,
        index=True
    )

    full_name = Column(
        String(150),
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(30),
        default="company_admin"
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        default=utcnow
    )

    company = relationship(
        "Company",
        back_populates="users"
    )

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "email",
            name="uq_user_company_email"
        ),
    )


# --------------------------------
# CONTACT TABLE
# --------------------------------

class Contact(Base):

    __tablename__ = "contacts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True
    )

    phone = Column(
        String(20),
        nullable=False
    )

    name = Column(
        String(150),
        default=""
    )

    sms_consent = Column(
        Boolean,
        default=False
    )

    voice_consent = Column(
        Boolean,
        default=False
    )

    opted_out = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=utcnow
    )

    company = relationship(
        "Company",
        back_populates="contacts"
    )

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "phone",
            name="uq_contact_company_phone"
        ),
    )


# --------------------------------
# CONSENT HISTORY TABLE
# --------------------------------

class ConsentEvent(Base):

    __tablename__ = "consent_events"

    id = Column(
        Integer,
        primary_key=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=False
    )

    channel = Column(
        String(20),
        nullable=False
    )

    action = Column(
        String(30),
        nullable=False
    )

    source = Column(
        String(150),
        default="admin_entry"
    )

    recorded_at = Column(
        DateTime(timezone=True),
        default=utcnow
    )


# --------------------------------
# NOTIFICATION LOG TABLE
# --------------------------------

class NotificationLog(Base):

    __tablename__ = "notification_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True
    )

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=False,
        index=True
    )

    channel = Column(
        String(20),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False
    )

    provider_message_id = Column(
        String(150),
        nullable=True
    )

    attempt = Column(
        Integer,
        default=1
    )

    message = Column(
        Text,
        nullable=True
    )

    error = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        default=utcnow
    )


Index(
    "ix_logs_company_created",
    NotificationLog.company_id,
    NotificationLog.created_at
)
