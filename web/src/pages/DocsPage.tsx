const endpoints = [
  {
    method: "POST",
    path: "/api-meta/api/v1/records",
    desc: "Ingest a record (open — no key needed). Client-supplied id is idempotent. Duplicates: ?on_duplicate=error|skip|replace.",
    body: `{
  "id": "optional-client-id",
  "schema_version": "1.0",
  "type": "invoice",
  "source": { "document_id": "doc_1", "filename": "scan.pdf", "page": 1,
              "extracted_at": "2026-08-04T07:00:00Z", "model": "surya-vllm-v2",
              "source_system": "khmer-parser-ui" },
  "pipeline": { "run_id": "run_1", "batch_id": "batch_1", "version": "1.2.0" },
  "business": { "date": "2026-08-01", "tags": ["import"], "domain": "logistics" },
  "data": { "order_no": "INV-2201", "amount": 1500 }
}`,
  },
  {
    method: "POST",
    path: "/api-meta/api/v1/records/batch",
    desc: "Ingest up to 500 records in one call. Per-item isolation: one bad item never rolls back the others. ?on_duplicate applies to every item.",
    body: `{ "items": [ { ...record... }, { ...record... } ] }`,
  },
  {
    method: "POST",
    path: "/api-meta/api/v1/auth/login",
    desc: "Sign in. Send one of the configured keys as password → returns the token for X-API-Key.",
    body: `{ "password": "<your-team-key>" }`,
  },
  {
    method: "GET",
    path: "/api-meta/api/v1/records?type=&domain=&status=&tag=&business_from=&business_to=&created_from=&created_to=&edited_from=&edited_to=&q=&page=1&page_size=50&sort=created_at:desc",
    desc: "List records with filters, pagination and sorting. Open — no credentials needed.",
  },
  { method: "GET", path: "/api-meta/api/v1/records/{id}", desc: "Fetch one record (full envelope + data). Open." },
  {
    method: "GET",
    path: "/api-meta/api/v1/records/{id}/trace",
    desc: "Full lineage + immutable audit chain — provenance, pipeline job id, every edit with actor/timestamp, promoted dataset. Open.",
  },
  {
    method: "PATCH",
    path: "/api-meta/api/v1/records/{id}",
    desc: "Edit data / business / status. Auto-updates audit: edited_at, edited_by, edit_count++, status→edited. Send X-Edited-By: user:<name>.",
    body: `{ "data": { "order_no": "INV-9999" }, "status": "verified" }`,
  },
  { method: "DELETE", path: "/api-meta/api/v1/records/{id}", desc: "Delete a record (audit entry is kept)." },
  {
    method: "GET",
    path: "/api-meta/api/v1/export?format=csv|json|jsonl|parquet",
    desc: "Export filtered records. CSV flattened for spreadsheets (UTF-8 BOM); JSONL and Parquet stream for pipelines/analysts. Filters include created_from/to + edited_from/to for incremental sync. Open.",
  },
  { method: "GET", path: "/api-meta/api/v1/stats", desc: "Aggregates: totals by status / type / domain, per-day. Open." },
  { method: "GET", path: "/api-meta/api/v1/meta", desc: "Distinct types and domains (for filter dropdowns). Open." },
  { method: "GET", path: "/api-meta/api/v1/webhooks", desc: "Admin: register event-driven hooks (create/update/delete). Public http(s) targets only." },
  { method: "GET", path: "/api-meta/api/v1/datasets/{id}/file", desc: "Raw download of a published dataset's embedded file. Public." },
  { method: "GET", path: "/health", desc: "Liveness + DB check (open)." },
];

const methodTone: Record<string, string> = {
  GET: "bg-accent/10 text-accent",
  POST: "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400",
  PATCH: "bg-amber-500/15 text-amber-600 dark:text-amber-400",
  DELETE: "bg-red-500/15 text-red-500",
};

export default function DocsPage() {
  return (
    <div className="p-6 max-w-4xl">
      <h1 className="display mb-1">API Docs</h1>
      <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">
        Interactive OpenAPI docs:{" "}
        <a className="font-medium text-accent hover:underline" href="/api-meta/api/docs" target="_blank" rel="noreferrer">
          /api-meta/api/docs
        </a>{" "}
        · spec: <code className="font-mono">/api-meta/api/openapi.json</code>
      </p>

      <div className="panel p-5 mb-5">
        <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">Authentication</div>
        <p className="text-sm text-slate-600 dark:text-slate-300">
          Reads, edits, exports and stats are open — no key needed. The admin
          surface (users, settings, audit, webhooks) requires login.
        </p>
        <pre className="mt-2 rounded-lg bg-slate-50 dark:bg-white/5 p-3 font-mono text-xs text-accent">{`X-Session-Token: <portal-token>`}</pre>
        <p className="mt-2 text-xs text-slate-500">
          The records API is open by design so pipelines and analysts can
          integrate without shipping keys. Editing endpoints honor{" "}
          <code className="font-mono">X-Edited-By: user:&lt;name&gt;</code> for audit attribution.
        </p>
      </div>

      <div className="panel p-5 mb-5">
        <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">Automation & SDKs</div>
        <ul className="space-y-1.5 text-sm text-slate-600 dark:text-slate-300">
          <li>
            <strong className="text-slate-800 dark:text-slate-100">Python SDK:</strong>{" "}
            <code className="font-mono text-xs">pip install ./sdk</code> — typed client for every endpoint (in-repo at <code className="font-mono text-xs">sdk/</code>)
          </li>
          <li>
            <strong className="text-slate-800 dark:text-slate-100">Airflow DAGs:</strong>{" "}
            <code className="font-mono text-xs">dags/</code> — batch OCR, incremental CDC sync (Parquet), dataset snapshots
          </li>
          <li>
            <strong className="text-slate-800 dark:text-slate-100">Postman:</strong>{" "}
            <a className="font-medium text-accent hover:underline" href="/api-meta/docs/romdoul.postman_collection.json" download>
              download collection
            </a>
          </li>
          <li>
            <strong className="text-slate-800 dark:text-slate-100">Traceability:</strong>{" "}
            <code className="font-mono text-xs">GET /api/v1/records/{'{id}'}/trace</code> — lineage + immutable audit chain
          </li>
        </ul>
      </div>

      <div className="space-y-3">
        {endpoints.map((e) => (
          <div key={e.method + e.path} className="panel p-4">
            <div className="mb-1 flex items-center gap-3">
              <span className={`badge border-transparent ${methodTone[e.method] ?? ""}`}>{e.method}</span>
              <code className="font-mono text-sm text-slate-800 dark:text-slate-100 break-all">{e.path}</code>
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-300">{e.desc}</p>
            {e.body && (
              <pre className="mt-2 rounded-lg bg-slate-50 dark:bg-white/5 p-3 font-mono text-xs overflow-auto">{e.body}</pre>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
