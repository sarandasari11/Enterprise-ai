from __future__ import annotations

from backend.app.models.role import Role
from backend.app.models.user import User


class RBACService:
    """Centralized permission evaluation for the RBAC layer."""

    @staticmethod
    def role_has_permission(role: Role, permission_name: str) -> bool:
        if role is None:
            return False
        return any(permission.name == permission_name for permission in role.permissions)

    @staticmethod
    def user_has_permission(user: User, permission_name: str) -> bool:
        if user is None:
            return False
        for role in user.roles:
            if RBACService.role_has_permission(role, permission_name):
                return True
        return False
