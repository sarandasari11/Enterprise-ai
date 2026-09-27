from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base

if TYPE_CHECKING:
    from backend.app.models.approval_request import ApprovalRequest
    from backend.app.models.audit_log import AuditLog
    from backend.app.models.role import Role

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class User(Base):
    """Application user entity for identity and role assignment."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[str | None] = mapped_column(String(50), nullable=True)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="user")
    approval_requests: Mapped[list["ApprovalRequest"]] = relationship(
        foreign_keys="ApprovalRequest.user_id",
        back_populates="requester",
    )
    approved_requests: Mapped[list["ApprovalRequest"]] = relationship(
        foreign_keys="ApprovalRequest.reviewed_by",
        back_populates="reviewer",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email})"
