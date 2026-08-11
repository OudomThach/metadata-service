import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { getUser } from "../api/client";
import StatusBadge from "../components/StatusBadge";

/**
 * Verify queue — every `raw` extraction awaiting review.
 * Approve → status `verified`; Mark edited → status `edited` (needs corrections).
 */
export default function VerifyQueue() {
  const qc = useQueryClient();
  const user = getUser();
  const canAct = user?.role === "admin" || user?.role === "editor";
  const [busy, setBusy] = useState<string | null>(null);
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const { data: page, isLoading } = useQuery({
    queryKey: ["records", { status: "raw", page_size: 100, sort: "created_at:desc" }],
    queryFn: () => api.listRecords({ status: "raw", page_size: 100, sort: "created_at:desc" }),
  });

  const setStatus = async (id: string, status: "verified" | "edited") => {
    if (!canAct) return;
    setBusy(id);
    try {
      await api.patchRecord(id, { status });
      qc.invalidateQueries({ queryKey: ["records"] });
      qc.invalidateQueries({ queryKey: ["stats"] });
    } catch (err) {
      window.alert(err instanceof Error ? err.message : "Failed to update status");
    } finally {
      setBusy(null);
    }
  };

  const bulkSetStatus = async (status: "verified" | "edited") => {
    if (!canAct || selected.size === 0) return;
    if (!window.confirm(`Mark ${selected.size} record(s) as ${status}?`)) return;
    setBusy("bulk");
    let ok = 0;
    for (const id of selected) {
      try {
        await api.patchRecord(id, { status });
        ok++;
      } catch {
        /* skip individual failures */
      }
    }
    setBusy(null);
    setSelected(new Set());
    qc.invalidateQueries({ queryKey: ["records"] });
    qc.invalidateQueries({ queryKey: ["stats"] });
    window.alert(`Marked ${ok} of ${selected.size} as ${status}.`);
  };

  const toggle = (id: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleAll = () => {
    if (!page) return;
    if (selected.size === items.length) setSelected(new Set());
    else setSelected(new Set(items.map((r) => r.id)));
  };

  const items = page?.items ?? [];

  return (
    <div className="p-6 max-w-7xl">
      <div className="flex items-center justify-between gap-3 mb-3">
        <div>
          <h1 className="display">Verify queue</h1>
          <p className="mt-0.5 text-sm text-slate-600 dark:text-slate-400">
            Extractions awaiting review ({items.length}) — check the OCR text & metadata, then approve or mark edited
          </p>
        </div>
        <Link to="/records" className="btn-ghost px-3 py-1.5 text-xs">All records</Link>
      </div>

      <div className="panel overflow-x-auto">
        {canAct && selected.size > 0 && (
          <div className="flex items-center gap-3 border-b border-slate-200 bg-slate-950 px-3 py-2 text-white text-sm dark:border-white/10">
            <span>{selected.size} selected</span>
            <button
              type="button"
              className="rounded-md bg-emerald-500/20 px-3 py-1 text-xs font-medium text-emerald-300 hover:bg-emerald-500/30"
              disabled={busy !== null}
              onClick={() => void bulkSetStatus("verified")}
            >
              {busy === "bulk" ? "Working…" : `✓ Approve ${selected.size}`}
            </button>
            <button
              type="button"
              className="rounded-md bg-amber-500/20 px-3 py-1 text-xs font-medium text-amber-300 hover:bg-amber-500/30"
              disabled={busy !== null}
              onClick={() => void bulkSetStatus("edited")}
            >
              Needs edits
            </button>
            <button type="button" className="rounded-md bg-white/10 px-3 py-1 text-xs text-slate-300 hover:bg-white/20" onClick={() => setSelected(new Set())}>
              Clear
            </button>
          </div>
        )}
        <table className="w-full">
          <thead className="border-b border-slate-200 bg-slate-50/60 dark:bg-white/5">
            <tr>
              {canAct && (
                <th className="th w-10">
                  <input type="checkbox" onChange={toggleAll} checked={items.length > 0 && selected.size === items.length} className="rounded border-slate-300" />
                </th>
              )}
              <th className="th w-48">Document</th>
              <th className="th">Type</th>
              <th className="th">Model</th>
              <th className="th">Status</th>
              <th className="th">Created</th>
              <th className="th w-56">Action</th>
            </tr>
          </thead>
          <tbody>
            {isLoading && (
              <tr><td className="td text-slate-500" colSpan={6}>Loading…</td></tr>
            )}
            {!isLoading && items.length === 0 && (
              <tr><td className="td text-slate-500" colSpan={canAct ? 7 : 6}>Nothing to verify — queue is clear.</td></tr>
            )}
            {!isLoading && items.map((r) => {
              const docName = (r.data?.document_name as string) || (r.source?.filename as string) || "—";
              const hasDataset = Boolean((r.data?.dataset as Record<string, unknown> | undefined)?.name);
              return (
                <tr key={r.id} className="border-b border-slate-100 last:border-0 hover:bg-slate-50/60 dark:border-white/5 dark:hover:bg-white/5">
                  {canAct && (
                    <td className="td py-1.5" onClick={(e) => e.stopPropagation()}>
                      <input type="checkbox" checked={selected.has(r.id)} onChange={() => toggle(r.id)} className="rounded border-slate-300" />
                    </td>
                  )}
                  <td className="td max-w-52 truncate font-medium text-slate-900 dark:text-slate-100" title={docName}>
                    <Link to={`/records/${r.id}`} className="text-accent hover:underline">{docName}</Link>
                    {hasDataset && <span className="badge ml-1.5 border-accent/30 bg-accent/10 text-accent">dataset</span>}
                  </td>
                  <td className="td text-slate-600 dark:text-slate-300">{r.type}</td>
                  <td className="td text-slate-500">{r.source_model ?? "—"}</td>
                  <td className="td"><StatusBadge status={r.status} /></td>
                  <td className="td text-slate-500">{r.created_at?.slice(0, 16).replace("T", " ") ?? "—"}</td>
                  <td className="td py-1.5">
                    {canAct ? (
                      <div className="flex items-center gap-1.5">
                        <button
                          type="button"
                          className="rounded-md bg-emerald-500/10 px-2.5 py-1 text-xs font-medium text-emerald-600 hover:bg-emerald-500/20 disabled:opacity-50"
                          disabled={busy === r.id}
                          onClick={() => void setStatus(r.id, "verified")}
                          title="Approve: mark as verified"
                        >
                          ✓ Approve
                        </button>
                        <button
                          type="button"
                          className="rounded-md bg-amber-500/10 px-2.5 py-1 text-xs font-medium text-amber-600 hover:bg-amber-500/20 disabled:opacity-50"
                          disabled={busy === r.id}
                          onClick={() => void setStatus(r.id, "edited")}
                          title="Needs corrections: mark as edited"
                        >
                          Needs edits
                        </button>
                        <Link to={`/records/${r.id}`} className="rounded-md px-2.5 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-900">
                          Open
                        </Link>
                      </div>
                    ) : (
                      <span className="text-xs text-slate-400 italic">viewer — no actions</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
