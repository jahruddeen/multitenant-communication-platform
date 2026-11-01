
import csv
import io

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

from sqlalchemy.orm import Session

from app.auth import get_current_user

from app.database import get_db

from app.models import Contact, ConsentEvent, User

from app.schemas import (
    ContactCreate,
    ContactUpdate,
    ContactOut
)


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


# CREATE CONTACT

@router.post(
    "",
    response_model=ContactOut,
    status_code=201
)
def create_contact(
    data: ContactCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing = db.query(Contact).filter_by(
        company_id=user.company_id,
        phone=data.phone
    ).first()

    if existing:

        raise HTTPException(
            409,
            "Contact already exists"
        )

    contact = Contact(
        company_id=user.company_id,
        **data.model_dump()
    )

    db.add(contact)

    db.flush()

    if data.sms_consent:

        db.add(ConsentEvent(
            company_id=user.company_id,
            contact_id=contact.id,
            channel="SMS",
            action="GRANTED"
        ))

    if data.voice_consent:

        db.add(ConsentEvent(
            company_id=user.company_id,
            contact_id=contact.id,
            channel="VOICE",
            action="GRANTED"
        ))

    db.commit()

    db.refresh(contact)

    return contact


# GET CONTACTS

@router.get(
    "",
    response_model=list[ContactOut]
)
def list_contacts(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(Contact).filter(
        Contact.company_id == user.company_id
    ).order_by(
        Contact.id.desc()
    ).all()


# UPDATE CONTACT

@router.patch(
    "/{contact_id}",
    response_model=ContactOut
)
def update_contact(
    contact_id: int,
    data: ContactUpdate,
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

    changes = data.model_dump(
        exclude_unset=True
    )

    for key, value in changes.items():

        setattr(contact, key, value)

    db.commit()

    db.refresh(contact)

    return contact


# DELETE CONTACT

@router.delete(
    "/{contact_id}",
    status_code=204
)
def delete_contact(
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

    db.delete(contact)

    db.commit()


# CSV UPLOAD

@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            400,
            "Please upload CSV file"
        )

    raw = await file.read()

    if len(raw) > 2_000_000:

        raise HTTPException(
            413,
            "CSV file exceeds 2 MB"
        )

    try:

        reader = csv.DictReader(
            io.StringIO(
                raw.decode("utf-8-sig")
            )
        )

        required = {
            "phone",
            "name",
            "sms_consent",
            "voice_consent"
        }

        if not reader.fieldnames or not required.issubset(
            set(reader.fieldnames)
        ):

            raise ValueError(
                "Required headers: phone,name,sms_consent,voice_consent"
            )

        created = 0

        for row in reader:

            phone = (row.get("phone") or "").strip()

            if (
                not phone.startswith("+")
                or not phone[1:].isdigit()
                or not (8 <= len(phone[1:]) <= 15)
            ):
                continue

            existing = db.query(Contact).filter_by(
                company_id=user.company_id,
                phone=phone
            ).first()

            if existing:
                continue

            sms_ok = (
                row.get("sms_consent", "").strip().lower()
                == "true"
            )

            voice_ok = (
                row.get("voice_consent", "").strip().lower()
                == "true"
            )

            contact = Contact(
                company_id=user.company_id,
                phone=phone,
                name=(row.get("name") or "")[:150],
                sms_consent=sms_ok,
                voice_consent=voice_ok
            )

            db.add(contact)

            created += 1

        db.commit()

        return {
            "created": created,
            "message": "CSV processed successfully"
        }

    except (
        UnicodeDecodeError,
        csv.Error,
        ValueError
    ) as exc:

        db.rollback()

        raise HTTPException(
            400,
            str(exc)
        )
