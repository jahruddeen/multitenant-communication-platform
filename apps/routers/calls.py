
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.auth import get_current_user

from app.database import get_db

from app.models import Contact, User

from app.schemas import CallRequest, NotificationOut

from app.services.scheduler import request_retry


router = APIRouter(
    prefix="/calls",
    tags=["Voice Calls"]
)


# START VOICE CALL

@router.post(
    "/start",
    response_model=NotificationOut
)
def start_call(
    data: CallRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        result = request_retry(
            db,
            user.company_id,
            data.contact_id
        )

        return result

    except ValueError as exc:

        message = str(exc)

        code = (
            404
            if message == "Contact not found"
            else 429
        )

        raise HTTPException(
            code,
            message
        )

    except PermissionError as exc:

        raise HTTPException(
            403,
            str(exc)
        )

    except RuntimeError as exc:

        raise HTTPException(
            503,
            str(exc)
        )


# OPT OUT CONTACT

@router.post("/{contact_id}/opt-out")
def opt_out(
    contact_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    contact = db.query(Contact).filter_by(
        id=contact_id,
        company_id=user.company_id
    ).first()

    if not contact:

        raise HTTPException(
            404,
            "Contact not found"
        )

    contact.opted_out = True

    contact.sms_consent = False

    contact.voice_consent = False

    db.commit()

    return {
        "status": "opted_out",
        "contact_id": contact.id
    }
