from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.core.database import Base
from backend.app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from backend.app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

engine = create_engine("sqlite:///./enterprise_ai.db")
Base.metadata.create_all(bind=engine)


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    is_active: bool


def get_db() -> Session:
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    existing_user = db.query(User).filter(User.email == str(payload.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user = User(
        email=str(payload.email),
        name=payload.name,
        password_hash=hash_password(payload.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "is_active": user.is_active,
    }


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    user = db.query(User).filter(User.email == str(payload.email)).first()
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id), extra_claims={"email": user.email, "name": user.name})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_current_user(authorization: str | None = Header(default=None, alias="Authorization"), db: Session = Depends(get_db)) -> dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {"id": user.id, "email": user.email, "name": user.name, "is_active": user.is_active}


@router.post("/logout")
def logout(authorization: str | None = Header(default=None, alias="Authorization")) -> dict[str, str]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = authorization.split(" ", 1)[1]
    try:
        decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    return {"message": "Logged out successfully"}
