# Domain-Driven Design Assessment — metadata-service

A pragmatic DDD review of the extraction-records domain: what the model gets
right, where it leaks, and what to do about it. Not a refactor mandate — the
model is already close to the ideal; the fixes below are small and additive.

## Ubiquitous language

| Term | Meaning (one definition) | Used consistently |
|---|---|---|
| Record | One extraction result (envelope + data), identified by client-supplied id | ✅ code, schema, API, portal |
| Envelope | The fixed metadata wrapper: source/audit/pipeline/record/business | ✅ |
| Status | `raw → edited → verified` lifecycle | ✅ single `constants.py` source |
| Dataset | First-class publishable artifact promoted from a Record | ✅ |
| Actor | Who made the call: `user:<name>` / `key:<key>` / `system:<who>` | ✅ |

**Verdict: strong.** The vocabulary is stable and consistently used.

## Bounded contexts

```
┌────────────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│  Extraction        │     │  Verification         │     │  Publishing      │
│  (pipelines POST   │────▶│  (portal edits,       │────▶│  (datasets,      │
│   records; raw     │     │   status raw→verified)│     │   public browse) │
│   status)          │     │                      │     │                  │
└────────────────────┘     └──────────────────────┘     └──────────────────┘
```

Each context owns a phase of the Record lifecycle. They integrate through the
`Record` aggregate (shared kernel) and domain events (webhooks, audit log).

## Aggregate: Record

```
Record (aggregate root, id = client-supplied id)
├── envelope
│   ├── source      (VO: filename, model, page, extracted_at)
│   ├── audit       (VO: created/edited by+at, edit_count, status)
│   ├── pipeline    (VO: run_id, batch_id, version)
│   ├── record      (VO: validation status + warnings)
│   └── business    (VO: date, tags, domain, is_duplicate, coverage)
└── data            (free-form extraction payload — the only domain-dependent part)
```

**What's right:**
- Aggregate root owns its audit history — edits go through `patch_record`,
  which bumps `edit_count` and appends an immutable `AuditEvent` row
- Status lifecycle is an **invariant enforced inside the aggregate
  boundary** (`_build_envelope`/`patch_record` validate transitions)
- Cross-aggregate references are by id (`record_id` on Dataset, not a child)
- Value objects are treated immutably (envelope is rebuilt, not mutated)

**What leaks (small):**

| Leak | Where | Fix |
|---|---|---|
| Domain work in routers | `records.py` builds/merges envelopes, decides status transitions | Extract envelope-building into a domain service (`domain/record_factory.py`) — routers should validate + call it |
| Envelope → columns duplication | `crud.to_out` re-derives columns from envelope JSON | Accept as a read-model projection (documented), or compute once in the factory |
| `capture-ocr` builds a Record by hand in the router | `admin.py` | Route through the same factory |
| Promotion logic is a service but lives in `promote.py` at app root | — | Fine as-is (small); move to `domain/` when it grows |

## Domain events

- `AuditEvent` (per-record immutable history) — the event log ✅
- `AuditEventGlobal` (cross-entity) — the audit trail ✅
- Webhooks fired on `create/update/delete` — the outbox-ish side effect ✅
- **Gap:** events are written inside the same transaction (good), but there is
  no explicit domain-event object (`RecordVerified(id, at)`); the webhook
  payload is shaped ad-hoc. If more consumers appear, introduce typed events.

## Repositories

- `crud.py` acts as the persistence layer (filters, sort, to_out) — pragmatic
  and sufficient at this size ✅
- No repository interface/protocol — fine until there's a second storage
  backend or tests need a fake. SQLite tests already reuse the same engine.

## Recommendations (additive, in priority order)

1. **Extract `build_envelope`/`_apply_envelope` into `domain/record_factory.py`**
   — one place for envelope rules; `records.py` and `admin.py` both call it
2. **Typed domain event objects** (`RecordCreated`, `RecordVerified`) feeding
   both audit rows and webhooks — replaces ad-hoc `{"event": action, ...}`
3. **Document the read-model**: `crud.to_out` columns are a projection of the
   envelope, not a second source of truth (add a comment + test asserting
   they stay in sync)
4. Leave `data` free-form — the "domain-agnostic envelope" IS the product
   decision (per README); don't schema-ify it

## Verdict

The model is a **healthy aggregate-centric design** with consistent language
and correct invariant placement. The three fixes above are hygiene, not
surgery. Skip any of them if the domain stops growing.
