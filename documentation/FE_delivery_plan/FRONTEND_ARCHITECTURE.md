# Weekly Wonder — Frontend Architecture Baseline

**Status:** Initial proposal; review before treating as final.

## 1. Context and boundary

The frontend is a browser application for creating and monitoring research runs and reviewing source-backed briefs. It is not an AI runtime. FastAPI owns authentication, authorization, validation, persistence, run lifecycle and communication with the LangGraph workflow. The AI workflow owns planning, source gathering, analysis, verification and structured report generation.

```text
Browser
  React pages/components
       | typed API client (HTTPS/JSON)
       v
  FastAPI API --------------------> PostgreSQL
       |                                stores runs, sources, evidence, reports
       | starts/queries workflow
       v
  LangGraph workflow ---> search/retrieval tools and MCP integrations
       |
       +---- lifecycle/progress events ----> FastAPI SSE endpoint ----> Browser
```

This is a logical diagram, not a deployment topology. Actual queues, workers, database schema and MCP server placement remain backend/platform decisions.

## 2. Frontend responsibilities

- Present research request forms and client-side usability validation.
- Call backend APIs and display authoritative server state.
- Render run status, progress, sources, evidence and reports.
- Handle network errors, loading/empty/partial results, reconnects and user recovery.
- Support accessible, responsive interaction and human review.
- Capture safe diagnostic information and correlation IDs where available.

## 3. Frontend does not own

- Provider credentials or secret management.
- Authorization decisions or tenant isolation.
- LLM prompts as a security boundary.
- LangGraph node orchestration, retries or model-provider calls.
- Source trust decisions solely through styling; trust/verification metadata must come from backend/AI logic.
- Persistent run state as the authoritative record.

## 4. Data flow

1. Form collects a `ResearchRequest` and validates user-facing constraints.
2. API client sends a command to create the run.
3. Backend returns a canonical `ResearchRun` snapshot and ID.
4. UI navigates to run detail and fetches the current snapshot.
5. UI subscribes to SSE events; event payloads update visible progress.
6. On reconnect, the UI resumes using event IDs where supported and refetches the snapshot to reconcile state.
7. On completion, UI fetches the structured report and source/evidence records.
8. UI presents provenance and lets the user review/export according to product rules.

## 5. State ownership

- **Server state:** runs, reports, sources, evidence, user permissions and run lifecycle. Backend is authoritative.
- **Local UI state:** modal open/closed, current filter, current search input, selected tab, transient form draft.
- **Form state:** current input values, client validation errors, server validation errors, submit pending state.
- **Stream state:** connection status, last event ID and latest safe progress message. It must not replace the canonical run snapshot.

Use a server-state library only when complexity justifies it. Start with a small typed API client and local React state if the app remains small; add TanStack Query or equivalent when cache invalidation, pagination, deduplication and polling needs become significant.

## 6. Status and error semantics

Agree canonical status values with Backend and AI. UI labels may be friendlier, but must map from stable API enum values. Unknown future statuses should render a safe fallback rather than crash.

Each request path should handle:
- pending/loading;
- success;
- empty result;
- validation error;
- unauthenticated/unauthorized response;
- rate limit or quota response if applicable;
- network timeout/disconnection;
- server error with correlation ID;
- partial result;
- terminal run failure/cancellation.

Do not show raw stack traces or internal provider errors to end users.

## 7. API client conventions

- One base URL from validated public environment configuration.
- Typed request/response payloads and centralized error parsing.
- Explicit timeout and cancellation behaviour where appropriate.
- Include request/correlation IDs when backend supports them.
- No secrets in frontend environment variables.
- Use ISO 8601 strings for timestamps; format only at the UI boundary.
- Keep API DTOs compatible with OpenAPI and validate contract changes in CI where practical.

## 8. SSE conventions to agree before production

- Stable event envelope and event names.
- Monotonic or otherwise well-defined event IDs.
- `Last-Event-ID`/replay policy and duplicate handling.
- Heartbeat and idle timeout behaviour.
- Reconnect backoff, maximum retry behaviour and snapshot reconciliation.
- Terminal event semantics for completed, failed and cancelled runs.
- Safe user-facing messages without internal stack traces or secrets.
- Authentication strategy compatible with browser EventSource constraints.

## 9. Security and privacy

- Browser bundle is public; anything compiled into it must be considered visible.
- Enforce authorization server-side for every run/report/source access.
- Render source text as text, not arbitrary HTML. Sanitize any rich content that truly must be rendered.
- Treat retrieved documents and prompt-injection content as untrusted.
- Use safe external link attributes and a restrictive content security policy appropriate to deployment.
- Avoid logging full prompts, reports or source excerpts unless explicitly approved and protected.
- Define retention and deletion requirements before collecting user or customer research data.

## 10. Quality attributes and initial targets

Targets below should be confirmed against the product's expected traffic and deployment environment.

- Reliability: failed network requests produce recoverable UI, not silent failure.
- Accessibility: keyboard operation, visible focus, labels, semantic headings and announced status changes.
- Performance: dashboard shell renders quickly; long lists are paginated; large report content does not block navigation.
- Maintainability: feature-oriented code, typed boundaries, automated checks and current docs.
- Observability: frontend error plus request/run ID can be correlated with server logs without exposing sensitive content.

## 11. Decisions still open

- Router choice and final route map.
- Form validation library and schema source.
- Server-state/cache library.
- Authentication mechanism and token/cookie strategy.
- Exact run status lifecycle and event schema.
- Report editing/versioning requirements.
- Export formats and file-generation location.
- Telemetry provider and data-retention policy.
