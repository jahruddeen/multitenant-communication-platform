
from fastapi import APIRouter, Depends, HTTPException

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from apps.database import get_db

from models import Company, User

from schemas import (
    CompanyRegister,
    Token,
    UserOut
)

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    require_company_admin
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# COMPANY REGISTRATION

@router.post(
    "/register",
    response_model=UserOut,
    status_code=201
)
def register(
    data: CompanyRegister,
    db: Session = Depends(get_db)
):

    email = data.email.lower()

    existing = db.query(Company).filter(
        Company.email == email
    ).first()

    if existing:

        raise HTTPException(
            status_code=409,
            detail="Company already registered"
        )

    company = Company(
        name=data.company_name,
        email=email
    )

    db.add(company)

    db.flush()

    user = User(

        company_id=company.id,

        email=email,

        full_name=data.full_name,

        password_hash=hash_password(
            data.password
        ),

        role="company_admin"
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


# USER LOGIN

@router.post(
    "/login",
    response_model=Token
)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form.username.lower()
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active or not user.company.is_active:

        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    token = create_access_token(user)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# CURRENT USER

@router.get(
    "/me",
    response_model=UserOut
)
def get_profile(
    user: User = Depends(get_current_user)
):

    return user
