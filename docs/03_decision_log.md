# Decision Log

## Decision Template

### Decision ID

### Date

### Decision

### Reason

### Alternatives Considered

### Expected Impact

## Decisions

### Decision ID

#001

### Date

2026-06-13

### Decision

Do not start with RAG.

### Reason

Current user pain is not knowledge retrieval. The first pain is daily business recording and structured data collection.

### Alternatives Considered

Build an AI knowledge base for salon operations first.

### Expected Impact

The MVP stays close to the user's daily workflow and starts collecting useful structured data.

### Decision ID

#002

### Date

2026-06-13

### Decision

Start with text input before voice input.

### Reason

Text input is easier to build and test. Voice input can be added later with Whisper.

### Alternatives Considered

Start directly with voice input.

### Expected Impact

The first version can be shipped and tested faster while keeping the voice-first direction open.

### Decision ID

#003

### Date

2026-06-13

### Decision

Use SQLite first.

### Reason

The MVP is for one salon first. A local-first database is enough.

### Alternatives Considered

Use Postgres, a hosted database, or a full SaaS backend from day one.

### Expected Impact

The system remains simple, cheap, and easy to operate during validation.

### Decision ID

#004

### Date

2026-06-13

### Decision

Do not build authentication, payment, or multi-tenant SaaS yet.

### Reason

The current goal is to validate one real user and one real workflow.

### Alternatives Considered

Build a full SaaS product foundation immediately.

### Expected Impact

Development stays focused on proving whether the core workflow is useful.

