# API Design Overview

## Planned backend API surface

The backend will provide the following route groups in future phases:

- `auth` — register, login, logout, identity lookup
- `users` — user management and role mapping
- `roles` — role definition and assignment
- `permissions` — permission management
- `chat` — agent conversation requests
- `tools` — available tool discovery and metadata
- `approvals` — approval request / decision workflow
- `audit` — audit log queries

## Authentication endpoints

Planned endpoints:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/logout`

## Authorization approach

Protected endpoints should require authenticated identity and deterministic permission checks via middleware or dependency injection.

## Tool discovery contract

The system should expose only tools allowed for the current user. The tool metadata will include fields such as:

- tool_name
- server
- description
- required_permission
- risk_level
- requires_approval

## Execution contract

Any tool invocation must include:

- user identity
- target tool
- required permission check
- approval status when applicable
- audit log entry for the action result

## Phase 1 API state

This phase defines the API structure and contracts conceptually. The concrete route implementations and authorization middleware will be created in the corresponding later phases.
