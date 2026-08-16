import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api, type AuditEventOut } from "../api/client";
import StatusBadge from "../components/StatusBadge";
import { MarkdownView } from "../components/MarkdownView";
import { DatasetOverview, DatasetColumns, DatasetReferences, DatasetData, deriveRecordText } from "../components/DatasetEditor";
import { getUser } from "../api/client";

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="panel p-4">
      <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">{title}</div>
      {children}
    </div>
  );
}

function formatVal(v: unknown): string {
  if (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(v)) {
    try {
      const d = new Date(v);
      return d.toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit', hour12: true });
    } catch { return String(v); }
  }
  return typeof v === 'object' ? JSON.stringify(v) : String(v);
}

function KV({ obj }: { obj: Record<string, unknown> | null | undefined }) {
  if (!obj || Object.keys(obj).length === 0) return <div className="text-xs text-slate-500">—</div>;
  const skip = new Set(['thumbnail_base64']);
  return (
    <dl className="grid grid-cols-[160px_1fr] gap-x-3 gap-y-1.5">
      {Object.entries(obj).filter(([k]) => !skip.has(k)).map(([k, v]) => (
        <div key={k} className="contents">
          <dt className="text-xs text-slate-500 break-all">{k}</dt>
          <dd className="text-sm text-slate-700 dark:text-slate-200 break-all">{formatVal(v)}</dd>
        </div>
      ))}
    </dl>
  );
}

function TabButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-md px-3 py-1 text-xs font-medium transition-colors ${
        active ? "bg-slate-100 text-slate-950" : "text-slate-500 hover:text-slate-800"
      }`}
    >
      {children}
    </button>
  );
}

function HistoryTimeline({ recordId }: { recordId: string }) {
  const { data: events, isLoading, isError } = useQuery({
    queryKey: ["history", recordId],
    queryFn: () => api.recordHistory(recordId),
  });
  const [expanded, setExpanded] = useState<number | null>(null);

  if (isLoading) return <div className="text-sm text-slate-500">Loading history…</div>;
  if (isError || !events) return <div className="text-sm text-red-500">Could not load history.</div>;
  if (events.length === 0) return <div className="text-sm text-slate-500">No history yet.</div>;

  const tone: Record<string, string> = {
    create: "border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
    delete: "border-red-500/30 bg-red-500/10 text-red-500",
    update: "border-accent2/30 bg-accent2/10 text-accent2",
  };

  const dataDiff = (prev: Record<string, unknown> | undefined, curr: Record<string, unknown> | undefined): Record<string, unknown> | null => {
    if (!prev || !curr) return null;
    const prevData = (prev.data || {}) as Record<string, unknown>;
    const currData = (curr.data || {}) as Record<string, unknown>;
    const diff: Record<string, unknown> = {};
    for (const k of new Set([...Object.keys(prevData), ...Object.keys(currData)])) {
      const was = JSON.stringify(prevData[k]), now = JSON.stringify(currData[k]);
      if (was !== now) diff[k] = { from: prevData[k], to: currData[k] };
    }
    return Object.keys(diff).length > 0 ? diff : null;
  };

  const bizDiff = (prev: Record<string, unknown> | undefined, curr: Record<string, unknown> | undefined): Record<string, unknown> | null => {
    if (!prev || !curr) return null;
    const prevBiz = (prev.business || {}) as Record<string, unknown>;
    const currBiz = (curr.business || {}) as Record<string, unknown>;
    const diff: Record<string, unknown> = {};
    for (const k of new Set([...Object.keys(prevBiz), ...Object.keys(currBiz)])) {
      const was = JSON.stringify(prevBiz[k]), now = JSON.stringify(currBiz[k]);
      if (was !== now) diff[k] = { from: prevBiz[k], to: currBiz[k] };
    }
    return Object.keys(diff).length > 0 ? diff : null;
  };

  return (
    <ol className="relative space-y-4 border-l border-slate-200 dark:border-white/10 pl-4">
      {events.map((ev: AuditEventOut, i: number) => {
        const prev = i > 0 ? events[i - 1].snapshot : undefined;
        const dD = ev.action === "update" ? dataDiff(prev, ev.snapshot) : null;
        const bD = ev.action === "update" ? bizDiff(prev, ev.snapshot) : null;
        return (
        <li key={ev.id} className="relative">
          <span className="absolute -left-[21px] top-1.5 h-2.5 w-2.5 rounded-full border-2 border-white dark:border-base-800 bg-accent shadow" />
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className={`badge ${tone[ev.action] ?? tone.update}`}>{ev.action}</span>
            <span className="font-mono text-xs text-slate-600 dark:text-slate-300">{ev.actor}</span>
            <span className="text-xs text-slate-400">{new Date(ev.at).toLocaleString()}</span>
            <button type="button" className="ml-auto text-xs text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"
              onClick={() => setExpanded(expanded === ev.id ? null : ev.id)}>
              {expanded === ev.id ? "hide" : "view"}
            </button>
          </div>
          {dD && (
            <div className="mt-1 text-xs text-slate-500">
              <span className="font-medium text-accent2">data changed:</span>{" "}
              {Object.keys(dD).join(", ")}
            </div>
          )}
          {bD && (
            <div className="mt-0.5 text-xs text-slate-500">
              <span className="font-medium text-accent">business changed:</span>{" "}
              {Object.keys(bD).join(", ")}
            </div>
          )}
          {expanded === ev.id && (
            <pre className="mt-2 max-h-56 overflow-auto whitespace-pre-wrap break-all rounded-lg bg-slate-50 dark:bg-white/5 p-3 font-mono text-[11px]">
              {JSON.stringify(ev.snapshot, null, 2)}
            </pre>
          )}
        </li>
        );
      })}
    </ol>
  );
}

export default function RecordDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const [tab, setTab] = useState<"overview" | "columns" | "references" | "data" | "details" | "history">("overview");
  const [textEditing, setTextEditing] = useState(false);
  const [textDraft, setTextDraft] = useState('');
  const [textView, setTextView] = useState<'text' | 'markdown'>('markdown');
  const user = getUser();
  const canEdit = user?.role === "admin" || user?.role === "editor";

  const { data: rec, isLoading } = useQuery({
    queryKey: ["record", id],
    queryFn: () => api.getRecord(id!),
  });

  const patch = useMutation({
    mutationFn: (body: Record<string, unknown>) => api.patchRecord(id!, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["record", id] });
      qc.invalidateQueries({ queryKey: ["records"] });
      qc.invalidateQueries({ queryKey: ["stats"] });
      qc.invalidateQueries({ queryKey: ["history", id] });
    },
  });

  const remove = useMutation({
    mutationFn: () => api.deleteRecord(id!),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["records"] });
      qc.invalidateQueries({ queryKey: ["stats"] });
      navigate("/records");
    },
  });

  if (isLoading || !rec) return <div className="p-8 text-slate-500">Loading…</div>;

  return (
    <div className="p-6 max-w-5xl">
      <div className="flex items-center gap-3 mb-4">
        <Link to="/records" className="btn-ghost">← Records</Link>
        <h1 className="display break-all">{rec.type}</h1>
        <StatusBadge status={rec.status} />
        <code className="text-xs text-slate-500 break-all">{rec.id}</code>
      </div>

      <div className="flex items-center gap-1 rounded-lg border border-slate-200 bg-white dark:bg-white/5 p-0.5 shadow-sm w-fit mb-4">
        <TabButton active={tab === "overview"} onClick={() => setTab("overview")}>Overview</TabButton>
        <TabButton active={tab === "columns"} onClick={() => setTab("columns")}>Columns</TabButton>
        <TabButton active={tab === "references"} onClick={() => setTab("references")}>References</TabButton>
        <TabButton active={tab === "data"} onClick={() => setTab("data")}>Data</TabButton>
        <TabButton active={tab === "details"} onClick={() => setTab("details")}>Details</TabButton>
        <TabButton active={tab === "history"} onClick={() => setTab("history")}>History</TabButton>
      </div>

      {tab === "details" && (
        <div className="grid md:grid-cols-2 gap-4">
          <Section title="Source">
            {(rec.source?.thumbnail_base64 as string) && (
              <img src={rec.source?.thumbnail_base64 as string} alt="Source preview" className="mb-3 max-h-44 rounded-lg border border-slate-200 dark:border-white/10 object-contain" />
            )}
            <KV obj={rec.source} />
            <div className="mt-2 text-xs text-slate-500">model: {rec.source_model ?? "—"} · system: {rec.source_system ?? "—"}</div>
          </Section>
          <Section title="Audit">
            <KV obj={rec.audit} />
            <div className="mt-2 text-xs text-slate-500">
              created_by: {rec.created_by} · edited_by: {rec.edited_by ?? "—"} · edits: {rec.edit_count}
            </div>
          </Section>
          <Section title="Pipeline">
            <KV obj={rec.pipeline} />
          </Section>
          <Section title="Business">
            <KV obj={rec.business} />
          </Section>
          <Section title="Record / validation">
            <KV obj={rec.record} />
          </Section>
        </div>
      )}

      {tab === "overview" && (
        <div className="space-y-4">
          {(rec.source?.thumbnail_base64 as string) && (
            <div className="flex items-start gap-4 mb-2">
              <img src={rec.source?.thumbnail_base64 as string} alt="Source" className="h-28 w-28 rounded-lg border border-slate-200 dark:border-white/10 object-cover shrink-0" />
              <div className="min-w-0 pt-1">
                <div className="text-sm font-medium text-slate-900 dark:text-slate-100 break-all">{String(rec.data?.document_name ?? rec.source?.filename ?? "—")}</div>
                <div className="mt-1 flex flex-wrap items-center gap-2">
                  <StatusBadge status={rec.status} />
                  <span className="text-xs text-slate-500">{rec.type} · edited ×{rec.edit_count}</span>
                </div>
              </div>
            </div>
          )}

          {/* Verification actions */}
          {canEdit && rec.status !== "verified" && (
            <Section title="Verification">
              <div className="flex flex-wrap items-center gap-2">
                <button
                  type="button"
                  className="rounded-md bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-600 hover:bg-emerald-500/20 disabled:opacity-50"
                  disabled={patch.isPending}
                  onClick={() => patch.mutate({ status: "verified" })}
                >
                  ✓ Approve (mark verified)
                </button>
                <button
                  type="button"
                  className="rounded-md bg-amber-500/10 px-3 py-1.5 text-xs font-medium text-amber-600 hover:bg-amber-500/20 disabled:opacity-50"
                  disabled={patch.isPending}
                  onClick={() => patch.mutate({ status: "edited" })}
                >
                  Needs edits
                </button>
                <span className="text-xs text-slate-400">Recheck the OCR text and metadata, then approve.</span>
              </div>
            </Section>
          )}

          {/* OCR text — readable, editable like the review panel */}
          <Section title="OCR text">
            {(() => {
              const hasText = Boolean(deriveRecordText(rec.data).trim());
              if (!hasText) {
                return (
                  <div className="grid gap-1.5 rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm dark:bg-amber-500/10">
                    <span className="font-medium text-amber-700 dark:text-amber-400">No text was extracted from this document.</span>
                    <span className="text-amber-600/80 dark:text-amber-500/70">
                      The OCR engine returned nothing for this scan — re-run it in the app, or upload a clearer image. The record is kept so nothing is lost.
                    </span>
                  </div>
                );
              }
              return null;
            })()}
            {Boolean(deriveRecordText(rec.data).trim()) && (
            <>
            <div className="mb-2 flex items-center gap-2">
              <div className="flex items-center rounded-lg border border-slate-200 bg-white p-0.5 shadow-sm">
                <button
                  type="button"
                  onClick={() => setTextView("text")}
                  className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${textView === "text" ? "bg-slate-100 text-slate-950" : "text-slate-500"}`}
                >
                  Text
                </button>
                <button
                  type="button"
                  onClick={() => setTextView("markdown")}
                  className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${textView === "markdown" ? "bg-slate-100 text-slate-950" : "text-slate-500"}`}
                >
                  Markdown
                </button>
              </div>
              {canEdit && !textEditing && (
                <button
                  type="button"
                  className="rounded-md px-2.5 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-900"
                  onClick={() => { setTextDraft(String(rec.data?.full_text ?? "")); setTextEditing(true); }}
                >
                  ✏️ Edit text
                </button>
              )}
            </div>
            {textEditing && canEdit ? (
              <div className="space-y-2">
                <textarea
                  className="input min-h-40 w-full resize-y text-sm leading-relaxed"
                  value={textDraft}
                  onChange={(e) => setTextDraft(e.target.value)}
                  spellCheck={false}
                />
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    className="btn-primary px-3 py-1.5 text-xs"
                    disabled={patch.isPending}
                    onClick={() => {
                      const draft = textDraft;
                      patch.mutate({ data: { ...rec.data, full_text: draft, markdown: draft } });
                    }}
                  >
                    Save text
                  </button>
                  <button type="button" className="btn-ghost px-3 py-1.5 text-xs" onClick={() => { setTextEditing(false); setTextDraft(String(rec.data?.full_text ?? "")); }}>
                    Cancel
                  </button>
                </div>
              </div>
            ) : textView === "markdown" ? (
              <MarkdownView source={deriveRecordText(rec.data)} maxHeight="520px" />
            ) : (
              <div className="whitespace-pre-wrap break-words rounded-lg bg-slate-50 dark:bg-white/5 p-3 text-sm leading-relaxed text-slate-700 dark:text-slate-300" style={{ fontFamily: "'Noto Sans Khmer', 'Khmer OS Siemreap', 'Segoe UI', sans-serif" }}>
                {String(rec.data?.full_text ?? rec.data?.markdown ?? "—")}
              </div>
            )}
            </>
            )}
          </Section>

          <DatasetOverview rec={rec} canEdit={canEdit} onPatch={(b) => patch.mutate(b)} />
        </div>
      )}

      {tab === "columns" && (
        <DatasetColumns rec={rec} canEdit={canEdit} onPatch={(b) => patch.mutate(b)} />
      )}

      {tab === "references" && (
        <DatasetReferences rec={rec} canEdit={canEdit} onPatch={(b) => patch.mutate(b)} />
      )}

      {tab === "data" && (
        <DatasetData rec={rec} canEdit={canEdit} onPatch={(b) => patch.mutate(b)} />
      )}

      {tab === "history" && (
        <Section title="Edit history">
          <HistoryTimeline recordId={rec.id} />
        </Section>
      )}

      <div className="mt-4 flex justify-end">
        <button
          className="btn-ghost text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10"
          onClick={() => {
            if (confirm("Delete this record?")) remove.mutate();
          }}
        >
          Delete record
        </button>
      </div>
    </div>
  );
}
