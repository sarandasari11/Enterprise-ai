# Architecture

## System overview

The system is designed as a secure enterprise AI platform with the following boundary layers:

1. Frontend user interface
2. FastAPI backend
3. Authentication and token validation
4. RBAC and permission enforcement
5. LangGraph-based agent orchestration
6. Permission-aware MCP client
7. External MCP servers for GitHub, Jira, and database operations
8. Audit and approval subsystems

## Architectural flow

```text
User
  ↓
React UI
  ↓
FastAPI API
  ↓
Auth + JWT validation
  ↓
RBAC permission lookup
  ↓
Permission-aware tool discovery
  ↓
LangGraph agent
  ↓
Execution-time authorization
  ↓
MCP tool call
  ↓
External system
```

## Physical monorepo structure

```text
enterprise-ai-agent/
├── backend/
├── frontend/
├── mcp-servers/
├── database/
├── docs/
├── tests/
├── docker-compose.yml
├── .env.example
├── README.md
└── implementation.txt
```

## Separation of concerns

### Authentication
The identity layer answers: "Who is this user?"

### Authorization
The RBAC layer answers: "What is this user allowed to do?"

### Agent orchestration
The LangGraph layer answers: "Which allowed workflow should the system follow?"

### MCP integration
The MCP layer answers: "What external tool interface is available?"

### Approval control
The approval system answers: "Does this action require a human decision before execution?"

### Audit
The audit layer records all meaningful events without exposing secrets.

## Security architecture

The core rule is:

> The LLM may decide what action it wants to perform, but it must never decide whether it is authorized to perform that action.

Therefore, authorization is enforced by deterministic policy logic before any tool is invoked. MCP tool metadata and RBAC rules stay distinct. Tool filtering and tool execution authorization are separate enforcement points.

## Phase 1 architecture scope

Phase 1 defines the project foundation only. Future phases will add:

- RBAC persistence and database model
- authentication service and token validation
- backend routes and middleware
- MCP tool registry and execution logic
- LangGraph state and node execution
- approval workflow and audit logging implementation
- frontend dashboards and Docker deployment

## Future implementation alignment

The design aligns with the phased plan in `implementation.txt` and intentionally leaves later phases for their respective implementation steps.
