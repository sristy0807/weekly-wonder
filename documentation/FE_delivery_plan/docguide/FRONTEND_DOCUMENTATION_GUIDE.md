# Weekly Wonder — Frontend Documentation Guide

This guide defines which documentation the team should maintain, who owns it, and when it must change.

## Documentation index

| Document | Purpose | Owner | Update trigger |
|---|---|---|---|
| `README.md` | Quick start, prerequisites, commands, environment setup | Frontend Lead | Setup or scripts change |
| `docs/FRONTEND_DELIVERY_PLAN.md` | Team roles, work breakdown, dependencies, acceptance gates | Solution Architect / Tech Lead | Scope, staffing, delivery sequence changes |
| `docs/FRONTEND_ARCHITECTURE.md` | Frontend boundaries, code structure, data flow, state/error strategy | Frontend Lead + Architect | Significant structure or integration decisions change |
| `docs/adr/` | Short records of important decisions and alternatives | Decision owner, coordinated by Architect | A consequential technical decision is made |
| `docs/API_CONTRACT.md` or generated OpenAPI link | Request/response schemas, errors, auth and versioning | Backend Lead; reviewed by Frontend | API contract changes |
| `docs/RESEARCH_RUN_EVENTS.md` | SSE event names, payloads, ordering, reconnect and terminal states | Backend + Frontend + AI | Event stream changes |
| `docs/UX_STATES.md` | Loading, empty, error, disabled, permission and responsive states | UX + Frontend | UI flow/state changes |
| `docs/TESTING.md` | Test levels, commands, fixtures, coverage expectations | QA + Frontend | Test strategy or tooling changes |
| `docs/SECURITY_AND_PRIVACY.md` | Browser trust boundary, secrets, untrusted source content, telemetry | Architect + Security | Threat model or data handling changes |
| `docs/RELEASE_RUNBOOK.md` | Build/deploy/rollback/smoke checks | DevOps + Frontend | Release process changes |

Do not duplicate the complete OpenAPI schema in prose. Link to the authoritative generated contract and document frontend-specific interpretation and examples where needed.

## Frontend architecture principles

1. UI components render domain data; they do not know about LangGraph nodes, model vendors, or MCP server internals.
2. All API calls go through a small typed API client rather than being scattered across components.
3. API response DTOs and frontend view models should be separated only where there is a real mapping need. Avoid unnecessary duplicate type layers.
4. Server state (runs, reports, sources) is distinct from transient UI state (open modal, current filter, unsaved form input).
5. Run detail refresh/snapshot is the source of truth; SSE is an update channel, not the only copy of state.
6. Loading, empty, error, permission-denied, partial-result and terminal states are first-class UI states.
7. Source excerpts and generated text are untrusted data. Do not render arbitrary HTML from sources.
8. No API secrets in `VITE_*` variables; Vite variables are bundled into browser-accessible code.
9. Document a decision when it affects multiple features, future migration cost, security, reliability or team workflow.
10. Update docs in the same pull request as the implementation that changes them.

## Architecture Decision Record (ADR) template

Create `docs/adr/0001-example.md` for each accepted significant decision:

```md
# ADR-0001: <short decision title>

- Status: Proposed | Accepted | Superseded
- Date: YYYY-MM-DD
- Decision owners: <roles>

## Context
What problem or constraint requires a decision?

## Options considered
- Option A — benefits and drawbacks
- Option B — benefits and drawbacks

## Decision
What did we choose?

## Consequences
Trade-offs, operational impact, and what becomes easier/harder.

## Follow-up
Actions, owners and due dates, if any.
```

## Suggested initial ADRs

- ADR-0001: Use React + TypeScript + Vite for the web client.
- ADR-0002: Keep AI orchestration behind FastAPI; do not call LLM providers directly from the browser.
- ADR-0003: Use REST for commands/snapshots and SSE for one-way run progress in the MVP.
- ADR-0004: Use a typed canonical research-run lifecycle independent of LangGraph's internal state.
- ADR-0005: Define source/evidence provenance as first-class domain data.

These are suggestions. Record an ADR only after the team reviews and accepts the decision; do not treat a suggestion as an already-approved decision.

## Pull request documentation checklist

- [ ] Does the change alter setup, scripts, environment variables or build behaviour?
- [ ] Does it change API fields, event payloads, statuses or error semantics?
- [ ] Does it add a user flow or a new loading/error/empty state?
- [ ] Does it change authentication, source rendering, telemetry or data retention?
- [ ] Does it introduce a decision that affects more than one feature/team?
- [ ] Are test instructions and screenshots/recordings needed for reviewer confidence?

If all answers are no, no documentation change may be needed. Documentation should be maintained, not produced ceremonially.
