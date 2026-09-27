from backend.app.models.permission import Permission
from backend.app.models.role import Role
from backend.app.models.user import User
from backend.app.services.rbac_service import RBACService


def test_user_has_permission_from_role_assignment() -> None:
    role = Role(name="Developer", description="Developer access")
    permission = Permission(
        name="github.issue.create",
        resource="github_issue",
        action="create",
        description="Create GitHub issues",
    )
    role.permissions.append(permission)

    user = User(email="dev@example.com", name="Developer User", is_active=True)
    user.roles.append(role)

    assert RBACService.user_has_permission(user, "github.issue.create") is True
    assert RBACService.user_has_permission(user, "github.issue.read") is False


def test_role_has_permission_lookup() -> None:
    role = Role(name="Manager", description="Manager access")
    permission = Permission(
        name="jira.issue.create",
        resource="jira_issue",
        action="create",
        description="Create Jira issues",
    )
    role.permissions.append(permission)

    assert RBACService.role_has_permission(role, "jira.issue.create") is True
    assert RBACService.role_has_permission(role, "database.admin") is False


def test_user_can_have_multiple_roles_and_permissions() -> None:
    developer_role = Role(name="Developer")
    manager_role = Role(name="Manager")
    github_permission = Permission(
        name="github.issue.read",
        resource="github_issue",
        action="read",
        description="Read GitHub issues",
    )
    jira_permission = Permission(
        name="jira.issue.create",
        resource="jira_issue",
        action="create",
        description="Create Jira issues",
    )

    developer_role.permissions.append(github_permission)
    manager_role.permissions.append(jira_permission)

    user = User(email="ops@example.com", name="Ops User", is_active=True)
    user.roles.extend([developer_role, manager_role])

    assert RBACService.user_has_permission(user, "github.issue.read") is True
    assert RBACService.user_has_permission(user, "jira.issue.create") is True
    assert RBACService.user_has_permission(user, "deployment.approve") is False
