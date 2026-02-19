# src/user/signup.py
# DTO compiled from:     dna/user/signup.dna
# Service compiled from: spec/user/signup.spec
import re

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import exists
from sqlalchemy.orm import Session

from ..database import get_db
from .entity import User


# ── DTO: dna/user/signup.dna ────────────────────────────────────────────────
class SignupInput(BaseModel):
    # username : $T.Username !  (@len(3,30) @pattern([a-zA-Z0-9_]+))
    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    # email : $T.Email !  (@format(email))
    email: EmailStr
    # password : $T.Password !  (@len(8,72) @pattern((?=.*[a-z])(?=.*[A-Z])(?=.*\d)))
    password: str = Field(..., min_length=8, max_length=72)
    # password_confirm : Str !
    password_confirm: str
    # full_name : $T.FullName  (@len(1,100), optional)
    full_name: str | None = Field(default=None, max_length=100)

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not re.search(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)", v):
            raise ValueError("password must contain lowercase, uppercase, and digit")
        return v


# ── Service: spec/user/signup.spec ──────────────────────────────────────────
def signup(input: SignupInput, db: Session) -> None:
    # ? > db.exists(User, email == input.email)
    #   !=>! Err(EmailAlreadyExists)
    if db.query(exists().where(User.email == input.email)).scalar():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="EmailAlreadyExists"
        )

    # ? > db.exists(User, username == input.username)
    #   !=>! Err(UsernameAlreadyExists)
    if db.query(exists().where(User.username == input.username)).scalar():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="UsernameAlreadyExists"
        )

    # ? input.password != input.password_confirm
    #   !=>! Err(PasswordMismatch)
    if input.password != input.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="PasswordMismatch"
        )

    # hashed_pw <- > hash.bcrypt(input.password, $SecurityPolicy.password_hash @cost(12))
    hashed_pw = bcrypt.hashpw(
        input.password.encode(), bcrypt.gensalt(rounds=12)
    ).decode()

    # > db.create(User, username, email, hashed_password, full_name)
    user = User(
        username=input.username,
        email=input.email,
        hashed_password=hashed_pw,
        full_name=input.full_name,
    )
    db.add(user)
    db.commit()

    # => Ok  (returns None; router wraps as {"result": "Ok"})


# ── Router ───────────────────────────────────────────────────────────────────
router = APIRouter()


@router.post("/signup", status_code=status.HTTP_200_OK)
def signup_route(input: SignupInput, db: Session = Depends(get_db)) -> dict:
    signup(input, db)
    return {"result": "Ok"}
