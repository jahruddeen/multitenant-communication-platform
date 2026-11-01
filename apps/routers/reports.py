
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth import get_current_user

from app.database import get_db

from app.models import NotificationLog, User

from app.schemas import NotificationOut


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# NOTIFICATION HISTORY

@router.get(
    "/notifications",
    response_model=list[NotificationOut]
)
def notification_report(
    limit: int = 100,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    limit = max(1, min(limit, 500))

    logs = db.query(NotificationLog).filter(
        NotificationLog.company_id == user.company_id
    ).order_by(
        NotificationLog.created_at.desc()
    ).limit(limit).all()

    return logs


# SMS AND CALL SUMMARY

@router.get("/summary")
def summary(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    rows = db.query(
        NotificationLog.channel,
        NotificationLog.status
    ).filter(
        NotificationLog.company_id == user.company_id
    ).all()

    result = {
        "SMS": {},
        "VOICE": {}
    }

    for channel, status in rows:

        result.setdefault(channel, {})

        result[channel][status] = (
            result[channel].get(status, 0) + 1
        )

    return result
