
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import (
    get_current_user,
    require_company_admin
)

from apps.database import get_db
from models import Company, User


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# COMPANY PROFILE

@router.get("/me")
def company_profile(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    company = db.query(Company).filter(
        Company.id == user.company_id
    ).first()

    return {
        "id": company.id,
        "name": company.name,
        "email": company.email,
        "is_active": company.is_active,
        "created_at": company.created_at
    }


# COMPANY USERS

@router.get("/me/users")
def company_users(
    user: User = Depends(require_company_admin),
    db: Session = Depends(get_db)
):

    users = db.query(User).filter(
        User.company_id == user.company_id
    ).all()

    return [

        {
            "id": item.id,
            "email": item.email,
            "full_name": item.full_name,
            "role": item.role
        }

        for item in users
    ]
