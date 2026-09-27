from __future__ import annotations

from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class ApprovalRequest(Base):
    """Approval workflow record for sensitive or high-risk actions."""

    __tablename__ = "approval_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    resource: Mapped[str | None] = mapped_column(String(255), nullable=True)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="MEDIUM")
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="PENDING")
    requested_at: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: __import__("datetime").datetime.utcnow())
    reviewed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), nullable=True)

    requester: Mapped["User"] = relationship(foreign_keys=[user_id], back_populates="approval_requests")
    reviewer: Mapped["User | None"] = relationship(foreign_keys=[reviewed_by], back_populates="approved_requests")

    def __repr__(self) -> str:
        return f"ApprovalRequest(id={self.id}, action={self.action}, status={self.status})"
