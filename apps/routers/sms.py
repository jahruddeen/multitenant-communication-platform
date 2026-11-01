
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.auth import get_current_user

from app.database import get_db

from app.models import Contact, NotificationLog, User

from app.schemas import SMSRequest, NotificationOut

from app.services.sms_service import send_sms


router = APIRouter(
    prefix="/sms",
    tags=["SMS"]
)


@router.post(
    "/send",
    response_model=NotificationOut
)
def send(
    data: SMSRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    contact = db.query(Contact).filter_by(
        id=data.contact_id,
        company_id=user.company_id
    ).first()

    if not contact:

        raise HTTPException(
            404,
            "Contact not found"
        )

    if not contact.sms_consent or contact.opted_out:

        raise HTTPException(
            403,
            "SMS consent is required"
        )

    try:

        result = send_sms(
            contact.phone,
            data.message
        )

        log = NotificationLog(

            company_id=user.company_id,

            contact_id=contact.id,

            channel="SMS",

            status=result["status"],

            provider_message_id=result.get(
                "provider_message_id"
            ),

            message=data.message
        )

        db.add(log)

        db.commit()

        db.refresh(log)

        return log

    except RuntimeError as exc:

        raise HTTPException(
            503,
            str(exc)
        )
