
from datetime import datetime, timedelta, timezone

import jwt

from pwdlib import PasswordHash

from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from config import settings
from apps.database import get_db
from models import User


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

ALGORITHM = "HS256"


# --------------------------------
# PASSWORD HASHING
# --------------------------------

def hash_password(password: str) -> str:

    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed: str
) -> bool:

    return password_hash.verify(
        password,
        hashed
    )


# --------------------------------
# JWT TOKEN GENERATION
# --------------------------------

def create_access_token(user: User) -> str:

    now = datetime.now(timezone.utc)

    payload = {

        "sub": str(user.id),

        "company_id": user.company_id,

        "role": user.role,

        "iat": now,

        "exp": now + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# --------------------------------
# GET CURRENT USER
# --------------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload.get("sub", "0"))

    except (
        jwt.InvalidTokenError,
        ValueError,
        TypeError
    ):

        raise unauthorized

    user = db.query(User).filter(
        User.id == user_id,
        User.is_active.is_(True)
    ).first()

    if not user or not user.company or not user.company.is_active:

        raise unauthorized

    return user


# --------------------------------
# COMPANY ADMIN AUTHORIZATION
# --------------------------------

def require_company_admin(
    user: User = Depends(get_current_user)
):

    if user.role not in (
        "company_admin",
        "platform_admin"
    ):

        raise HTTPException(
            status_code=403,
            detail="Administrator permission required"
        )

    return user
