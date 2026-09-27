from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class ToolRegistry(Base):
    """Registry metadata for MCP tools and their authorization policy."""

    __tablename__ = "tool_registry"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tool_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    server_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    required_permission: Mapped[str] = mapped_column(String(255), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="LOW")
    requires_approval: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self) -> str:
        return f"ToolRegistry(id={self.id}, tool_name={self.tool_name})"
