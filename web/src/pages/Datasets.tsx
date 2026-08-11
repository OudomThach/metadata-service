import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api, type RecordOut } from "../api/client";
import StatusBadge from "../components/StatusBadge";

interface DatasetView {
  name?: string;
  managed_by?: string;
  frequency?: string;
  coverage_start?: string;
  coverage_end?: string;
  categories?: string;
  collection?: string;
  url?: string;
  description?: string;
  file?: { name?: string; size?: number; type?: string } | null;
  file_base64?: string | null;
}

/**
 * Datasets — every record carrying a `data.dataset` (created by the post-OCR
 * "Create New Public Dataset" form), with the saved CSV/Markdown preview.
 */
export default function Datasets() {
  const [q, setQ] = useState("");
  const [openId, setOpenId] = useState<string | null>(null);
  const [view, setView] = useState<"markdown" | "csv">("markdown");

  const { data: page, isLoading } = useQuery({
    queryKey: ["records", { page_size: 200, sort: "created_at:desc" }],
    queryFn: () => api.listRecords({ page_size: 200, sort: "created_at:desc" }),
  });

  const datasets: { record: RecordOut; ds: DatasetView }[] = (page?.items ?? [])
    .filter((r) => {
      const ds = (r.data?.dataset ?? null) as DatasetView | null;
      return Boolean(ds && (ds.name || ds.managed_by));
    })
    .map((record) => ({ record, ds: (record.data?.dataset ?? {}) as DatasetView }))
    .filter(({ ds }) => (ds.name ?? "").toLowerCase().includes(q.toLowerCase()));

  const fmtDate = (v?: string) => (v ? v.slice(0, 10) : "—");
  const fmtSize = (b?: number) => {
    if (!b) return "";
    return b >= 1024 * 1024 ? `${(b / (1024 * 1024)).toFixed(1)} MB` : b >= 1024 ? `${(b / 1024).toFixed(0)} KB` : `${b} B`;
  };

  const downloadText = (name: string, content: string, type = "text/plain") => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadEmbedded = (ds: DatasetView) => {
    if (!ds.file_base64 || !ds.file?.name) return;
    const raw = atob(ds.file_base64.replace(/-/g, "+").replace(/_/g, "/"));
    const bytes = new Uint8Array(raw.length);
    for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
    const blob = new Blob([bytes], { type: ds.file.type || "application/octet-stream" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = ds.file.name;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-6 max-w-7xl">
      <div className="flex items-center justify-between gap-3 mb-3">
        <div>
          <h1 className="display">Datasets</h1>
          <p className="mt-0.5 text-sm text-slate-600 dark:text-slate-400">
            Records with public-dataset metadata ({datasets.length}) — CSV & Markdown auto-saved from the final (corrected) OCR text
          </p>
        </div>
        <input
          className="input w-56"
          placeholder="Search dataset name…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
      </div>

      {isLoading && <div className="panel p-6 text-sm text-slate-500">Loading…</div>}
      {!isLoading && datasets.length === 0 && (
        <div className="panel p-6 text-sm text-slate-500">
          No datasets yet. OCR a document and complete the "Create New Public Dataset" form after extraction.
        </div>
      )}

      <div className="space-y-3">
        {datasets.map(({ record, ds }) => {
          const expanded = openId === record.id;
          return (
            <div key={record.id} className="panel overflow-hidden">
              <button
                type="button"
                className="flex w-full flex-wrap items-center gap-x-4 gap-y-1 px-4 py-3 text-left hover:bg-slate-50/60 dark:hover:bg-white/5"
                onClick={() => setOpenId(expanded ? null : record.id)}
              >
                <span className="min-w-0 flex-1">
                  <span className="block truncate font-medium text-slate-900 dark:text-slate-100">{ds.name || "—"}</span>
                  <span className="mt-0.5 block truncate text-xs text-slate-500">
                    {ds.managed_by || "—"} · {ds.frequency || "—"} · {fmtDate(ds.coverage_start)} → {fmtDate(ds.coverage_end)}
                  </span>
                </span>
                <StatusBadge status={record.status} />
                <span className="text-xs text-slate-400">{ds.file?.name ?? "no file"}{ds.file?.size ? ` (${fmtSize(ds.file.size)})` : ""}</span>
                <span className="text-xs text-slate-500">{expanded ? "▲" : "▼"}</span>
              </button>

              {expanded && (
                <div className="border-t border-slate-200 px-4 py-3 dark:border-white/10">
                  <div className="mb-2 flex flex-wrap items-center gap-2">
                    <div className="flex items-center rounded-lg border border-slate-200 bg-white p-0.5 shadow-sm">
                      <button
                        type="button"
                        onClick={() => setView("markdown")}
                        className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${view === "markdown" ? "bg-slate-100 text-slate-950" : "text-slate-500"}`}
                      >
                        Markdown
                      </button>
                      <button
                        type="button"
                        onClick={() => setView("csv")}
                        className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${view === "csv" ? "bg-slate-100 text-slate-950" : "text-slate-500"}`}
                      >
                        CSV
                      </button>
                    </div>
                    <button
                      type="button"
                      className="btn-secondary px-2.5 py-1 text-xs"
                      onClick={() => downloadText(`${(ds.name ?? record.id).replace(/[^\w.-]+/g, "_")}.csv`, String(record.data?.csv ?? ""), "text/csv")}
                      disabled={!record.data?.csv}
                      title="Download the saved CSV"
                    >
                      ⬇ CSV
                    </button>
                    <button
                      type="button"
                      className="btn-secondary px-2.5 py-1 text-xs"
                      onClick={() => downloadText(`${(ds.name ?? record.id).replace(/[^\w.-]+/g, "_")}.md`, String(record.data?.markdown ?? record.data?.full_text ?? ""), "text/markdown")}
                      disabled={!record.data?.markdown && !record.data?.full_text}
                      title="Download the saved Markdown"
                    >
                      ⬇ .md
                    </button>
                    {ds.file_base64 && ds.file?.name && (
                      <button
                        type="button"
                        className="btn-secondary px-2.5 py-1 text-xs"
                        onClick={() => downloadEmbedded(ds)}
                        title={`Download the uploaded file (${fmtSize(ds.file?.size)})`}
                      >
                        ⬇ {ds.file.name}
                      </button>
                    )}
                    <Link to={`/records/${record.id}`} className="btn-ghost px-2.5 py-1 text-xs">Full record</Link>
                    {ds.url && (
                      <a href={ds.url} target="_blank" rel="noreferrer" className="btn-ghost px-2.5 py-1 text-xs">Source link ↗</a>
                    )}
                    {ds.description && <span className="text-xs text-slate-500 italic">“{ds.description.slice(0, 120)}…”</span>}
                  </div>
                  <pre className="max-h-72 overflow-auto whitespace-pre-wrap break-all rounded-lg bg-slate-50 dark:bg-white/5 p-3 font-mono text-[11px] text-slate-700 dark:text-slate-300">
                    {view === "markdown"
                      ? String(record.data?.markdown ?? record.data?.full_text ?? "—")
                      : String(record.data?.csv ?? "—")}
                  </pre>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
