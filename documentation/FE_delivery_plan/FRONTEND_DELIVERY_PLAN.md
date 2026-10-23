# Weekly Wonder — Frontend Delivery Plan

**Status:** Draft baseline for the MVP  
**Owner:** Product/Engineering Lead  
**Frontend stack:** React, TypeScript, Vite, Tailwind CSS, shadcn/ui-style components  
**Target backend:** FastAPI REST API + Server-Sent Events (SSE) for run progress  
**AI orchestration:** LangGraph behind the backend boundary; MCP/tools are backend concerns

## 1. Purpose and scope

Build a reliable web workspace for creators and researchers to configure research requests, monitor research runs, inspect sources and evidence, review findings, and export a source-backed research brief.

The current dashboard is a UI prototype with sample data. A successful Vite build proves that the source compiles and bundles; it does not prove product behaviour, accessibility, API integration, security, or AI workflow correctness.

### MVP user journey

1. User opens the research dashboard.
2. User creates a research request (topic/question, date window, language, intended format, depth, exclusions).
3. UI validates the request and submits it to the backend.
4. UI shows the created run and its lifecycle status.
5. UI receives progress updates and handles reconnects or stale state.
6. User opens a run to inspect sources, claims/findings, evidence, and warnings.
7. User reviews/edits the brief and exports or copies it.
8. User can retry failed work or request a revised run, with clear cost/status feedback.

### Explicitly out of scope for the first frontend slice

- Running an LLM or LangGraph directly in the browser.
- Storing API keys or provider secrets in frontend code.
- Publishing to YouTube automatically.
- A complex real-time collaboration system.
- Building every settings, billing, team-admin, and analytics page before validating the core research journey.

## 2. Team structure and responsibilities

A small team can combine roles, but each responsibility must have a named owner. For a 5–7 person delivery team:

| Role | Primary accountability | Concrete outputs |
|---|---|---|
| Product Manager (PM) | User problem, scope, priority, acceptance criteria | Product brief, personas, MVP scope, prioritized backlog, release acceptance |
| Solution Architect / Tech Lead | End-to-end boundaries, key technical decisions, quality attributes, cross-team alignment | Context/container diagrams, ADRs, API/event contracts, risk register, technical review |
| UX/UI Designer | User flows, information architecture, interaction and visual design | User flows, wireframes, design tokens, component states, responsive/accessibility annotations |
| Frontend Engineer(s) | Implement accessible, tested UI and frontend architecture | React features, state management, API client, tests, frontend docs |
| Backend Engineer | API, auth, persistence, run lifecycle and event delivery | FastAPI endpoints, Pydantic schemas, database model, SSE events, OpenAPI contract |
| AI/ML Engineer | Research graph, tools, evidence processing, evaluation and guardrails | LangGraph workflow, source/evidence schemas, graph state, evaluations, failure behaviour |
| QA / Test Engineer | Independent validation, test strategy and release confidence | Test plan, functional/regression results, defect reports, release sign-off evidence |
| DevOps / Platform Engineer (part-time early) | Environments, CI/CD, secrets, observability and deployment | CI pipeline, environment config, hosting, logs/metrics, rollback procedure |
| Security/Privacy reviewer (part-time) | Threat modelling, data handling, authorization and prompt-injection controls | Security review, privacy requirements, abuse cases, remediation tracking |

### If the team is small

- 3 people: (1) Product + UX, (2) Solution Architect + Frontend, (3) Backend + AI integration; borrow QA/security/DevOps support as needed.
- 5 people: PM/UX can be one person; Architect/Tech Lead; Frontend; Backend; AI Engineer. QA is shared but must still have explicit test ownership.
- Do not make the AI Engineer the owner of frontend API contracts by default. The Architect/Tech Lead coordinates the contract, with Frontend and Backend jointly reviewing it.

## 3. Role-level task breakdown

### Product Manager
- Define primary persona and top user job.
- Specify request inputs and report outputs in user language.
- Rank MVP versus later features.
- Write user stories with testable acceptance criteria.
- Resolve product decisions: retry behaviour, cancellation, report editing, export formats, usage/cost disclosure.
- Run demos and accept/reject delivered stories.

### Solution Architect / Tech Lead
- Define system context and boundaries: browser UI, API, database, workflow engine, search/source providers.
- Establish frontend/backend ownership and versioned API contracts.
- Define run lifecycle and error taxonomy with Backend + AI.
- Decide how the UI gets progress (recommend SSE first for one-way progress).
- Set quality attributes: security, reliability, accessibility, performance, maintainability, observability.
- Maintain Architecture Decision Records (ADRs), risks, dependency map and non-functional requirements.
- Review design for secrets, authorization, untrusted source content, retries and duplicate submissions.
- Facilitate design/code reviews; avoid becoming a bottleneck for routine implementation.

### UX/UI Designer
- Map the core flow and information hierarchy.
- Design dashboard, create-run form, run details, source/evidence view, report review, error/empty/loading states.
- Define responsive behaviour and keyboard/focus states.
- Specify reusable patterns and design tokens.
- Test the flow with representative users before polishing secondary screens.

### Frontend Engineer
- Set up route/layout/component boundaries and typed domain models.
- Implement form validation and accessible interaction states.
- Build API client and loading/error/retry behaviour.
- Implement run list, run details, progress stream, sources, evidence and report review.
- Keep backend/AI implementation details out of UI components.
- Write unit/component/integration tests and document local setup and decisions.
- Monitor bundle size, runtime errors and accessibility.

### Backend Engineer
- Agree request/response/event contracts before parallel implementation.
- Implement authentication/authorization, input validation, run persistence and ownership checks.
- Provide list/detail/create/cancel/retry/report endpoints as agreed for MVP.
- Implement SSE event stream with run IDs, event IDs/reconnect semantics, heartbeat and terminal states.
- Expose OpenAPI documentation and realistic fixtures.
- Ensure duplicate submissions and retries are handled intentionally (idempotency where appropriate).

### AI/ML Engineer
- Define typed workflow input/output independent of the UI.
- Implement research planning, source discovery, evidence extraction, verification/gap analysis and brief generation.
- Return structured evidence and source metadata, not only free-form text.
- Handle partial results, tool failures, timeouts, and uncertainty explicitly.
- Evaluate citation support, source quality, hallucination risk and prompt-injection resilience.
- Emit meaningful lifecycle/progress events through the backend contract.

### QA / Test Engineer
- Translate acceptance criteria into test cases.
- Validate browser, viewport, keyboard, accessibility and failure scenarios.
- Test create/list/detail/progress/retry/cancel/export end-to-end when APIs are available.
- Verify that citations resolve to the right source and that incomplete evidence is labelled.
- Track regressions and maintain a release checklist.

### DevOps / Platform Engineer
- Provide dev/staging/prod configuration and deployment pipeline.
- Keep secrets server-side; configure CORS, HTTPS, environment variables and secure headers.
- Add frontend error reporting and backend correlation/run IDs.
- Define health checks, logs, rollback and build artifact retention.

## 4. Frontend work breakdown structure (WBS)

Priority key: **P0** required for a credible MVP; **P1** valuable next; **P2** later.

### FE-0 — Discovery and design baseline (P0)
- Confirm persona, top journey, request fields, report shape and MVP exclusions.
- Map user flow and navigation.
- Create page/state inventory.
- Define responsive breakpoints and keyboard interaction expectations.
- Agree frontend/backend vocabulary and lifecycle statuses.
- **Acceptance:** PM, UX, Frontend, Backend, AI and Architect agree on the core journey and terminology.

### FE-1 — Application foundation (P0)
- Verify project scripts, TypeScript strictness and path alias behaviour.
- Establish feature/folder conventions, route strategy and layout shell.
- Centralize design tokens, typography, spacing, colours and reusable components.
- Add environment variable convention (`VITE_API_BASE_URL` only for public API origin; never secrets).
- Add error boundary and global error/empty/loading patterns.
- Configure formatting/linting and CI build check.
- **Acceptance:** clean install, development server, production build and CI build succeed from documented instructions.

### FE-2 — Dashboard overview (P0)
- Research run list with pagination strategy (client or server; choose with API design).
- Search and status filters with defined semantics.
- Summary metrics only when their meaning and source are defined.
- Empty state, loading skeleton, API error state and retry.
- Run row links to run details.
- **Acceptance:** all values come from typed data; no hard-coded production metrics; filter/search behaviour is tested.

### FE-3 — Create research request (P0)
- Define `ResearchRequest` fields with PM/AI.
- Form validation, helpful inline messages, keyboard support and submission state.
- Prevent accidental duplicate submissions while a request is in flight.
- Show server validation errors and recoverable failures.
- Navigate to or display the newly created run.
- **Acceptance:** valid input produces one run; invalid input explains how to fix it; server failure preserves user input.

### FE-4 — Run lifecycle and progress (P0)
- Define canonical statuses and legal transitions with Backend + AI.
- Run detail header with status, timestamps, duration and available actions.
- SSE client for progress; reconnect/backoff and stale-state recovery.
- Handle queued/running/needs-review/completed/failed/cancelled states as agreed.
- Show meaningful stages, not fake percentage progress if no reliable percentage exists.
- **Acceptance:** refresh/reconnect does not lose the current run; terminal states stop progress listening; failures are understandable.

### FE-5 — Sources and evidence (P0)
- Source list with title, publisher/domain, URL, published/retrieved time and source type where available.
- Evidence/findings linked to source IDs and relevant excerpts.
- Clearly distinguish source fact, model inference, unresolved claim and contradictory evidence.
- External links open safely; handle missing metadata and inaccessible sources.
- **Acceptance:** every evidence-backed claim can be traced to one or more source records; missing citations are visible, not fabricated.

### FE-6 — Research brief review (P0)
- Structured report view: executive summary, key findings, why it matters, caveats, competing views and references.
- Copy/export action (MVP can start with Markdown download/copy if agreed).
- Human review/editing rules and unsaved-change handling.
- **Acceptance:** the brief remains readable, sources are accessible and export content matches the displayed report.

### FE-7 — Error, retry and cancellation (P0/P1)
- Standard error model and user-safe messages.
- Retry/re-run behaviour and cost implications.
- Cancel only if backend supports cancellation semantics.
- Preserve useful state after network interruption.
- **Acceptance:** every user action has a defined success, failure and recovery outcome.

### FE-8 — Accessibility, responsive behaviour and polish (P0)
- Keyboard-only navigation, visible focus, labels and semantic landmarks.
- Contrast, reduced motion and screen-reader status announcements.
- Test narrow screens and zoom.
- Avoid colour as the only status indicator.
- **Acceptance:** no blocking accessibility issues in the core journey; manual keyboard pass completed.

### FE-9 — Test and observability baseline (P0)
- Unit tests for pure logic and schema mapping.
- Component tests for form, filtering, status rendering and errors.
- API contract tests against fixtures or a test server.
- End-to-end smoke test for the core journey.
- Capture frontend runtime errors and correlate with request/run IDs without logging sensitive content.
- **Acceptance:** tests run in CI; release has reproducible evidence for core acceptance criteria.

### FE-10 — P1/P2 enhancements
- User preferences and saved research templates.
- Advanced filters, sorting and saved views.
- Report editor with version history.
- Team sharing/permissions, billing/usage, notification preferences.
- Internationalization and multiple report languages.
- Offline support only if a real product requirement exists.

## 5. Recommended frontend structure

Keep the code feature-oriented, not one giant `App.tsx` file. A reasonable target structure as the app grows:

```text
src/
  app/                 # app bootstrap, routes, providers, global error boundary
  components/ui/       # reusable primitive UI components
  components/shared/   # app-wide patterns: loading, empty, error, status badge
  features/
    research-runs/
      api.ts            # feature API calls
      types.ts          # frontend domain types
      components/       # run list, filters, status, progress
      pages/            # overview and run detail
    research-request/
      schema.ts         # request validation schema
      components/       # request form
    research-report/
      components/       # brief, evidence, citations, export
  lib/
    api-client.ts       # base URL, JSON/error handling, request IDs
    env.ts              # validated public environment configuration
    utils.ts
  test/                 # test setup and shared fixtures
  types/                # only truly cross-feature types
```

Do not create every folder before it is needed. Refactor incrementally when a feature boundary becomes real. Avoid coupling components to LangGraph node names or internal graph state.

## 6. Frontend domain model (initial proposal)

The names and values must be agreed with Backend + AI and then reflected in OpenAPI/types. These are illustrative, not a final contract.

```ts
type ResearchRunStatus =
  | 'queued'
  | 'running'
  | 'needs_review'
  | 'completed'
  | 'failed'
  | 'cancelled'

type ResearchRequest = {
  question: string
  topic?: string
  dateFrom?: string
  dateTo?: string
  outputLanguage: string
  intendedFormat: 'youtube_script' | 'research_brief'
  depth: 'quick' | 'standard' | 'deep'
  exclusions?: string[]
}

type ResearchRun = {
  id: string
  title: string
  status: ResearchRunStatus
  createdAt: string
  updatedAt: string
  progressStage?: string
  errorCode?: string
}
```

Use ISO 8601 timestamps and document timezone interpretation. Do not use UI labels such as `"Today, 10:42 AM"` as API values. Format timestamps in the UI.

## 7. API and event contract responsibilities

The exact contract is an Architect-led, Frontend/Backend/AI-reviewed deliverable. Suggested initial surface:

- `POST /api/research-runs` — validate and create a run; return run ID and initial status.
- `GET /api/research-runs` — list the current user's runs with filters/pagination.
- `GET /api/research-runs/{run_id}` — canonical current run state.
- `GET /api/research-runs/{run_id}/events` — SSE lifecycle/progress stream.
- `GET /api/research-runs/{run_id}/report` — structured brief when available.
- `POST /api/research-runs/{run_id}/retry` — retry semantics if approved for MVP.
- `POST /api/research-runs/{run_id}/cancel` — only if cancellation is truly supported.

Define event envelope before implementation. Minimum fields to consider: `event_id`, `run_id`, `type`, `occurred_at`, `stage`, safe user-facing `message`, and optional structured payload. Document reconnection (`Last-Event-ID`), duplicate delivery, ordering, heartbeat and terminal events.

Use the FastAPI-generated OpenAPI schema as the contract source where practical. Avoid maintaining conflicting hand-written API types in multiple places; generate types or validate shared fixtures in CI.

## 8. Cross-cutting requirements

- **Security:** secrets stay server-side; enforce authorization per run; render source text as untrusted content; never execute source HTML; safe external links; avoid unsafe HTML rendering.
- **Privacy:** decide retention, deletion, telemetry and whether user research requests may contain confidential information.
- **Reliability:** request timeouts, retries only where safe, duplicate submission protection, SSE reconnect and refresh recovery.
- **Cost transparency:** communicate when a run is expensive or a retry starts new work if cost is relevant to users.
- **Performance:** lazy-load large report/detail views if needed; paginate long run/source lists; track bundle size.
- **Accessibility:** semantic HTML, keyboard access, focus management, accessible form errors and status announcements.
- **Observability:** correlate frontend errors and API requests with request/run IDs; do not log secrets or unnecessary research content.
- **AI trust:** provenance for claims, uncertainty labels, visible source links and explicit human approval before consequential publishing.

## 9. Definition of Ready (before a story starts)

- User/problem and desired outcome are clear.
- Acceptance criteria and failure states are written.
- Design or interaction notes exist for non-trivial UI.
- Required API fields/events and ownership are agreed, or a clearly labelled mock contract exists.
- Loading, empty, error and permission states are considered.
- Dependencies and test approach are known.

## 10. Definition of Done (for each frontend story)

- Meets acceptance criteria and design intent.
- TypeScript build and lint checks pass.
- Appropriate unit/component/API tests pass.
- Loading, empty, error and responsive states are handled.
- Keyboard and accessible labels/focus are checked for the changed flow.
- No secrets or sensitive data are exposed in browser code/logs.
- Documentation is updated when behaviour, contract, setup or architecture changes.
- Product/QA review completed for the user-visible outcome.

## 11. Delivery sequence and dependencies

1. **Align:** product brief, user flow, glossary, run status lifecycle.
2. **Contract-first:** request/response/event schemas and mock fixtures.
3. **Frontend foundation:** typed models, API client, error patterns, routes/layout.
4. **Core UI:** run list and create-request form against fixtures.
5. **Backend vertical slice:** create run → persist → list/detail → report placeholder.
6. **Progress:** SSE contract and reconnect behaviour.
7. **AI integration:** LangGraph emits structured status, evidence and report data through backend.
8. **Trust/review:** evidence/source review and human approval.
9. **Quality gate:** end-to-end, accessibility, security, performance and staging validation.
10. **Release:** deploy, monitor, collect feedback, prioritize next iteration.

The key is to deliver vertical slices end-to-end rather than completing all frontend screens in isolation and discovering late that the backend data model cannot support them.

## 12. Risks and open decisions

| Decision/risk | Owner(s) | Required outcome |
|---|---|---|
| Who is the first paying user and what job are they buying? | PM + Architect | One target persona and measurable MVP outcome |
| Exact request fields and report structure | PM + AI + UX | Versioned product/domain schema |
| Canonical run statuses and transitions | Architect + Backend + AI | State transition table and event contract |
| SSE reconnect/refresh behaviour | Backend + Frontend | Event IDs, snapshot endpoint, reconnect policy |
| Authentication and tenant boundaries | Architect + Backend + Security | Threat-reviewed authorization design |
| Source/citation quality and prompt injection | AI + Security + Product | Evaluation criteria and safe display rules |
| Report editing/versioning and export | PM + UX + Frontend | MVP decision and acceptance criteria |
| Data retention/deletion and telemetry | Product + Security + Backend | Documented privacy policy and operational rules |

## 13. Current prototype status

- Dashboard shell and sample research runs: implemented.
- Search/filter and demo create-run interaction: prototype behaviour; verify in browser.
- Production API, auth, database persistence, SSE, LangGraph, MCP, real citations: not yet integrated.
- `npm run build`: the developer has confirmed it succeeds locally.

Treat the current UI as a clickable prototype, not as a completed commercial frontend.
