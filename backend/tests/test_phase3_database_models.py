from backend.app.models.approval_request import ApprovalRequest
from backend.app.models.audit_log import AuditLog
from backend.app.models.permission import Permission
from backend.app.models.role import Role
from backend.app.models.tool_registry import ToolRegistry
from backend.app.models.user import User


def test_rbac_models_are_defined() -> None:
    user = User(email="example@example.com", name="Example User", is_active=True)
    role = Role(name="Developer", description="Developer access")
    permission = Permission(
        name="github.issue.create",
        resource="github_issue",
        action="create",
        description="Create GitHub issues",
    )

    user.roles.append(role)
    role.permissions.append(permission)

    assert user.email == "example@example.com"
    assert user.roles[0].name == "Developer"
    assert role.permissions[0].name == "github.issue.create"


def test_audit_and_approval_models_are_created() -> None:
    user = User(email="audit@example.com", name="Audit User", is_active=True)
    audit_log = AuditLog(
        user=user,
        role="Developer",
        action="github.issue.create",
        tool="create_github_issue",
        resource="repo-demo",
        decision="ALLOWED",
        reason="Permission granted",
        request_id="req-123",
    )
    approval = ApprovalRequest(
        user_id=1,
        action="deployment.rollback",
        resource="payments-api",
        risk_level="CRITICAL",
        reason="Severe deployment issue",
        status="PENDING",
    )

    assert audit_log.decision == "ALLOWED"
    assert approval.action == "deployment.rollback"
    assert approval.risk_level == "CRITICAL"


def test_tool_registry_metadata_tracks_permission_and_risk() -> None:
    tool = ToolRegistry(
        tool_name="create_github_issue",
        server_name="github",
        description="Create a GitHub issue",
        required_permission="github.issue.create",
        risk_level="LOW",
        requires_approval=False,
    )

    assert tool.required_permission == "github.issue.create"
    assert tool.risk_level == "LOW"
    assert tool.requires_approval is False
