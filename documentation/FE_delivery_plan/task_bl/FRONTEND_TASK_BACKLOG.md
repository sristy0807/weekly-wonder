# Weekly Wonder — Initial Frontend Backlog

Use this as an initial planning backlog. Estimates are intentionally omitted until the team clarifies requirements and capacity.

| ID | Priority | Work item | Owner(s) | Dependency | Done when |
|---|---|---|---|---|---|
| FE-001 | P0 | Confirm MVP journey, request inputs and report sections | PM, UX, Architect, AI | None | Signed-off user flow and acceptance criteria |
| FE-002 | P0 | Agree run status lifecycle and event vocabulary | Architect, Backend, AI, Frontend | FE-001 | State transition table and event contract reviewed |
| FE-003 | P0 | Establish routing and feature-oriented folder structure | Frontend | FE-001 | Dashboard and detail routes work; structure documented |
| FE-004 | P0 | Create typed domain models and fixtures | Frontend, Backend | FE-002 | Models/fixtures represent success, partial and failure cases |
| FE-005 | P0 | Add central API client and error normalization | Frontend | FE-004, API contract | Base URL, JSON parsing, errors and request IDs handled centrally |
| FE-006 | P0 | Implement dashboard list with loading/empty/error states | Frontend, UX | FE-004 | List renders API/fixture data and states are tested |
| FE-007 | P0 | Implement research request form | Frontend, UX, AI | FE-001, FE-004 | Validation, pending state and server errors work |
| FE-008 | P0 | Integrate create/list/detail endpoints | Frontend, Backend | FE-005, API contract | Create one run and view canonical run state |
| FE-009 | P0 | Implement run detail and lifecycle rendering | Frontend | FE-002, FE-008 | Known and unknown statuses render safely |
| FE-010 | P0 | Implement SSE progress and reconnect recovery | Frontend, Backend | FE-002, FE-009 | Refresh/reconnect reconciles with server snapshot |
| FE-011 | P0 | Implement sources/evidence panel | Frontend, AI, Backend, UX | Evidence schema | Findings link to source records; missing citations are visible |
| FE-012 | P0 | Implement report view and basic export/copy | Frontend, PM, UX | Report schema | Export matches rendered structured report |
| FE-013 | P0 | Add component and integration tests | Frontend, QA | FE-006–FE-012 | Core behaviours run in CI |
| FE-014 | P0 | Accessibility and responsive QA | UX, Frontend, QA | Core screens | Keyboard pass and viewport checks recorded |
| FE-015 | P0 | Add frontend error monitoring and correlation | Frontend, DevOps | API request ID design | Errors diagnosable without leaking sensitive data |
| FE-016 | P0 | Production smoke test and release docs | QA, DevOps, Frontend | FE-013–FE-015 | Staging checklist passes; rollback documented |
| FE-017 | P1 | Retry/cancel UI and API integration | Frontend, Backend, AI, PM | Lifecycle semantics | Supported actions show confirmation and clear outcomes |
| FE-018 | P1 | Saved templates and advanced filters | PM, UX, Frontend, Backend | MVP feedback | Feature meets prioritized user need |
| FE-019 | P2 | Team sharing, billing/usage and admin settings | PM, Architect, Backend, Frontend | Product validation | Scope and permission model approved |

## Suggested release gates

- **Gate A — Prototype:** responsive dashboard and local interactions; no production data claims.
- **Gate B — Connected UI:** real API create/list/detail; robust loading and error states.
- **Gate C — Agentic vertical slice:** one research request runs through LangGraph and returns a structured report with provenance.
- **Gate D — Commercial MVP:** authorization, operational observability, evaluation, accessibility, security review, support/runbook and customer feedback loop.
