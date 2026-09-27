# Security Model

## Core security principle

The system must enforce authorization outside the LLM. The model can propose an action, but backend policy decides whether it is allowed to run.

## Security layers

### 1. Authentication
- establishes identity
- validates user session or token
- separates user identity from permissions

### 2. RBAC
- maps users to roles
- maps roles to permissions
- evaluates allowed actions via deterministic logic

### 3. Permission-aware tool discovery
- filters tool registry based on the current user's permissions
- prevents unauthorized tools from being exposed to the agent

### 4. Execution-time authorization
- re-checks permission before each actual MCP invocation
- rejects unauthorized or manipulated tool requests

### 5. Human approval
- high-risk actions require out-of-band authorization
- approval is enforced before sensitive execution

### 6. Audit logging
- records login, authorization, denial, approval, and system events
- excludes secrets, tokens, and credentials

## Threat model focus

The design specifically addresses:

- prompt injection
- unauthorized tool calling
- privilege escalation
- token misuse
- broken access control
- tool abuse
- secret leakage
- malicious tool arguments

## Security design constraints

- no direct trust of frontend-provided claims
- no reliance on the LLM for authorization decisions
- no hard-coded credentials in source control
- no secret values in logs or example payloads
- no unchecked SQL execution in initial system design
- approvals handled outside the LLM workflow

## Phase 1 security baseline

This phase defines the architecture and documents the required controls, but does not yet implement runtime enforcement. The backend foundation for enforcement will be created in later phases.
