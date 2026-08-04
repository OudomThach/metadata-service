const endpoints = [
  {
    method: "POST",
    path: "/api/v1/records",
    desc: "Ingest a record. Client-supplied id is idempotent (409 on duplicate).",
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
    method: "GET",
    path: "/api/v1/records?type=&domain=&status=&tag=&business_from=&business_to=&created_from=&created_to=&q=&page=1&page_size=50&sort=created_at:desc",
    desc: "List records with filters, pagination and sorting.",
  },
  { method: "GET", path: "/api/v1/records/{id}", desc: "Fetch one record (full envelope + data)." },
  {
    method: "PATCH",
    path: "/api/v1/records/{id}",
    desc: "Edit data / business / status. Auto-updates audit: edited_at, edited_by, edit_count++, status→edited. Send X-Edited-By: user:<name>.",
    body: `{ "data": { "order_no": "INV-9999" }, "status": "verified" }`,
  },
  { method: "DELETE", path: "/api/v1/records/{id}", desc: "Delete a record (audit entry is kept)." },
  {
    method: "GET",
    path: "/api/v1/export?format=csv|json",
    desc: "Export filtered records. CSV is flattened for spreadsheets, JSON is the full envelope.",
  },
  { method: "GET", path: "/api/v1/stats", desc: "Aggregates: totals by status / type / domain, per-day." },
  { method: "GET", path: "/api/v1/meta", desc: "Distinct types and domains (for filter dropdowns)." },
  { method: "GET", path: "/health", desc: "Liveness + DB check." },
];

export default function DocsPage() {
  return (
    <div className="p-6 max-w-4xl">
      <h1 className="text-xl font-semibold text-slate-100 mb-1">API Docs</h1>
      <p className="text-sm text-slate-400 mb-4">
        Interactive OpenAPI docs: <a className="text-accent hover:underline" href="/api/docs" target="_blank">/api/docs</a> ·
        OpenAPI spec: <code className="text-slate-300">/api/openapi.json</code>
      </p>

      <div className="card p-4 mb-5">
        <div className="text-xs font-semibold uppercase tracking-wide text-slate-400 mb-2">Authentication</div>
        <p className="text-sm text-slate-300 mb-2">
          When the operator enables API keys, every request must send the header:
        </p>
        <pre className="text-xs bg-base-900 rounded p-3 text-accent">{`X-API-Key: <your-key>`}</pre>
        <p className="text-xs text-slate-500 mt-2">
          Without a key configured, the API is open (dev mode). Editing endpoints honor{" "}
          <code className="text-slate-400">X-Edited-By: user:&lt;name&gt;</code> for audit attribution.
        </p>
      </div>

      <div className="space-y-3">
        {endpoints.map((e) => (
          <div key={e.method + e.path} className="card p-4">
            <div className="flex items-center gap-3 mb-1">
              <span
                className={`px-2 py-0.5 rounded text-xs font-bold ${
                  e.method === "GET"
                    ? "bg-sky-500/15 text-sky-300"
                    : e.method === "POST"
                      ? "bg-emerald-500/15 text-emerald-300"
                      : e.method === "PATCH"
                        ? "bg-amber-500/15 text-amber-300"
                        : "bg-red-500/15 text-red-300"
                }`}
              >
                {e.method}
              </span>
              <code className="text-sm text-slate-200 break-all">{e.path}</code>
            </div>
            <p className="text-sm text-slate-400">{e.desc}</p>
            {e.body && (
              <pre className="text-xs bg-base-900 rounded p-3 mt-2 overflow-auto">{e.body}</pre>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
