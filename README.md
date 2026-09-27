# Enterprise AI Operations & Access Control Agent

This repository is being implemented in phases according to the implementation plan in `implementation.txt`.

## Phase 1 status

The project foundation has been established with:

- a monorepo structure for backend, frontend, MCP servers, docs, and database assets
- a requirements and architecture definition
- a security model that separates authentication, RBAC, tool authorization, and approval controls
- an initial API contract outline for the backend

## Repository layout

- `backend/` — FastAPI backend application
- `frontend/` — React + TypeScript UI
- `mcp-servers/` — MCP server implementations
- `database/` — database migrations and seed data
- `docs/` — project documentation
- `tests/` — higher-level tests

## Current phase

This repository is at Phase 1: system definition and architecture groundwork.

## Security principles

- Authentication and authorization are separate concerns.
- RBAC is enforced server-side, not by the LLM.
- Tool discovery is permission-aware.
- Execution-time authorization is required for every tool invocation.
- Sensitive actions require explicit human approval.
- Audit logs capture security-relevant events without logging secrets.

## Next steps

Continue with Phase 2 only after Phase 1 is reviewed and approved in this workspace.
