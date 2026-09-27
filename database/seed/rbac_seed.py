"""Seed data for the Phase 3 PostgreSQL RBAC model.

This is intentionally simple and deterministic. It creates the baseline roles and
permission set required by the project design without introducing later-phase
business logic.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.core.database import Base
from backend.app.models.permission import Permission
from backend.app.models.role import Role
from backend.app.models.user import User


def seed_rbac(engine) -> None:
    """Create baseline RBAC records if they are not already present."""
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        employee_role = session.query(Role).filter_by(name="Employee").first()
        if employee_role is None:
            employee_role = Role(name="Employee", description="Standard employee role")
            session.add(employee_role)

        developer_role = session.query(Role).filter_by(name="Developer").first()
        if developer_role is None:
            developer_role = Role(name="Developer", description="Developer role")
            session.add(developer_role)

        manager_role = session.query(Role).filter_by(name="Manager").first()
        if manager_role is None:
            manager_role = Role(name="Manager", description="Manager role")
            session.add(manager_role)

        admin_role = session.query(Role).filter_by(name="Admin").first()
        if admin_role is None:
            admin_role = Role(name="Admin", description="Administrative role")
            session.add(admin_role)

        session.flush()

        permissions = {
            "github.issue.read": Permission(
                name="github.issue.read",
                resource="github_issue",
                action="read",
                description="Read GitHub issues",
            ),
            "github.issue.create": Permission(
                name="github.issue.create",
                resource="github_issue",
                action="create",
                description="Create GitHub issues",
            ),
            "jira.issue.read": Permission(
                name="jira.issue.read",
                resource="jira_issue",
                action="read",
                description="Read Jira issues",
            ),
            "jira.issue.create": Permission(
                name="jira.issue.create",
                resource="jira_issue",
                action="create",
                description="Create Jira issues",
            ),
            "deployment.status.read": Permission(
                name="deployment.status.read",
                resource="deployment",
                action="status.read",
                description="Read deployment status",
            ),
            "deployment.approve": Permission(
                name="deployment.approve",
                resource="deployment",
                action="approve",
                description="Approve direct deployment actions",
            ),
            "database.admin": Permission(
                name="database.admin",
                resource="database",
                action="admin",
                description="Administrative database access",
            ),
        }

        for permission in permissions.values():
            existing_permission = session.query(Permission).filter_by(name=permission.name).first()
            if existing_permission is None:
                session.add(permission)

        session.flush()

        permission_lookup = {
            perm.name: perm for perm in session.query(Permission).all()
        }

        employee_role.permissions = [permission_lookup["github.issue.read"], permission_lookup["jira.issue.read"]]
        developer_role.permissions = [
            permission_lookup["github.issue.read"],
            permission_lookup["github.issue.create"],
            permission_lookup["jira.issue.read"],
            permission_lookup["jira.issue.create"],
            permission_lookup["deployment.status.read"],
        ]
        manager_role.permissions = [
            permission_lookup["github.issue.read"],
            permission_lookup["jira.issue.read"],
            permission_lookup["jira.issue.create"],
            permission_lookup["deployment.status.read"],
            permission_lookup["deployment.approve"],
        ]
        admin_role.permissions = list(permission_lookup.values())

        admin_user = session.query(User).filter_by(email="admin@example.com").first()
        if admin_user is None:
            admin_user = User(
                email="admin@example.com",
                name="System Administrator",
                is_active=True,
                password_hash="seeded",
            )
            session.add(admin_user)
            admin_user.roles.append(admin_role)

        session.commit()
