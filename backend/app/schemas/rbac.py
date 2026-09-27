from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PermissionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1)
    resource: str = Field(..., min_length=1)
    action: str = Field(..., min_length=1)
    description: Optional[str] = None


class RoleCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    password_hash: Optional[str] = None
    is_active: bool = True
