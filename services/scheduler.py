
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.config import settings

from app.models import Contact, NotificationLog

from app.services.voice_service import make_call


def request_retry(
    db: Session,
    company_id: int,
    contact_id: int
):

    contact = db.query(Contact).filter_by(
        id=contact_id,
        company_id=company_id
    ).first()

    if not contact:

        raise ValueError("Contact not found")

    if not contact.voice_consent or contact.opted_out:

        raise PermissionError(
            "Voice consent is required"
        )

    logs = db.query(NotificationLog).filter_by(
        company_id=company_id,
        contact_id=contact_id,
        channel="VOICE"
    ).order_by(
        NotificationLog.created_at.desc()
    ).all()

    if len(logs) >= settings.MAX_CALL_ATTEMPTS:

        raise ValueError(
            "Maximum voice attempts reached"
        )

    if logs:

        last_time = logs[0].created_at

        if last_time.tzinfo is None:

            last_time = last_time.replace(
                tzinfo=timezone.utc
            )

        allowed_at = last_time + timedelta(
            minutes=settings.CALL_RETRY_COOLDOWN_MINUTES
        )

        if datetime.now(timezone.utc) < allowed_at:

            raise ValueError(
                "Retry cooldown is active"
            )

    result = make_call(contact.phone)

    log = NotificationLog(

        company_id=company_id,

        contact_id=contact_id,

        channel="VOICE",

        status=result["status"],

        provider_message_id=result.get(
            "provider_message_id"
        ),

        attempt=len(logs) + 1
    )

    db.add(log)

    db.commit()

    db.refresh(log)

    return log
