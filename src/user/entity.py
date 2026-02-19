# src/user/entity.py
# Compiled from: dna/user/entity.dna
# User <: $BaseEntity  ($BaseEntity from dna/root.dna)
import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


# $Enum.Role : [admin, user, guest]  <- "user"
class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


# $Enum.Status : [active, inactive, banned]  <- "active"
class StatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    banned = "banned"


class User(Base):
    __tablename__ = "users"

    # $BaseEntity: id UUID ! required @auto
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    # $BaseEntity: created_at DateTime ! @auto
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # $BaseEntity: updated_at DateTime ! @auto
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # username : $T.Username ! @unique  (@len(3,30) @pattern([a-zA-Z0-9_]+))
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    # email : $T.Email ! @unique  (@format(email))
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    # hashed_password : Str ! @hashed @internal
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # full_name : $T.FullName  (@len(1,100), optional)
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # role : $Enum.Role  <- "user"
    role: Mapped[RoleEnum] = mapped_column(
        SAEnum(RoleEnum), default=RoleEnum.user, nullable=False
    )
    # status : $Enum.Status  <- "active"
    status: Mapped[StatusEnum] = mapped_column(
        SAEnum(StatusEnum), default=StatusEnum.active, nullable=False
    )
