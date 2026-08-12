import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, getUser, type DatasetOut } from "../api/client";
import { toast } from "../lib/toast";
import { MarkdownView } from "../components/MarkdownView";

/**
 * Datasets â€” first-class entities with draft -> published -> archived.
 * Published datasets are visible on the public Explore page.
 */
export default function Datasets() {
  const qc = useQueryClient();
  const me = getUser();
  const canEdit = me?.role === "admin" || me?.role === "editor";
  const [status, setStatus] = useState("");
  const [q, setQ] = useState("");
  const [openId, setOpenId] = useState<string | null>(null);
  const [page, setPage] = useState(1);

  const { data: pageData, isLoading } = useQuery({
    queryKey: ["datasets", status, q, page],
    queryFn: () => api.listDatasets({ page: page, page_size: 25, status: status || undefined, q: q || undefined }),
  });
  const { data: orgs } = useQuery({ queryKey: ["organizations"], queryFn: api.listOrganizations });
  const { data: cats } = useQuery({ queryKey: ["categories"], queryFn: api.listCategories });
  const { data: cols } = useQuery({ queryKey: ["collections"], queryFn: api.listCollections });

  const invalidate = () => {
    qc.invalidateQueries({ queryKey: ["datasets"] });
    qc.invalidateQueries({ queryKey: ["records"] });
  };
  const publish = useMutation({
    mutationFn: (id: string) => api.publishDataset(id),
    onSuccess: () => { invalidate(); toast.success("Dataset published â€” live on Explore."); },
  });
  const unpublish = useMutation({
    mutationFn: (id: string) => api.unpublishDataset(id),
    onSuccess: () => { invalidate(); toast.info("Dataset unpublished."); },
  });
  const remove = useMutation({
    mutationFn: (id: string) => api.deleteDataset(id),
    onSuccess: () => { invalidate(); toast.info("Dataset deleted."); },
  });

  const orgName = (id: number | null) => orgs?.find((o) => o.id === id)?.name ?? "â€”";
  const catName = (id: number | null) => cats?.find((c) => c.id === id)?.name ?? "â€”";
  const colName = (id: number | null) => cols?.find((c) => c.id === id)?.name ?? "â€”";

  const downloadText = (name: string, content: string, type: string) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    a.click();
    URL.revokeObjectURL(url);
  };
  const downloadFile = (d: DatasetOut) => {
    if (!d.file_base64 || !d.file_name) return;
    const raw = atob(d.file_base64.replace(/-/g, "+").replace(/_/g, "/"));
    const bytes = new Uint8Array(raw.length);
    for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
    downloadText(d.file_name, "", "application/octet-stream");
    const blob = new Blob([bytes], { type: d.file_type || "application/octet-stream" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = d.file_name;
    a.click();
    URL.revokeObjectURL(url);
  };

  const STATUS_BADGE: Record<string, string> = {
    draft: "border-slate-300 bg-slate-100 text-slate-600",
    published: "border-emerald-500/30 bg-emerald-500/10 text-emerald-600",
    archived: "border-amber-500/30 bg-amber-500/10 text-amber-600",
  };

  return (
    <div className="p-6 max-w-7xl">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
        <div>
          <h1 className="display">Datasets</h1>
          <p className="mt-0.5 text-sm text-slate-600 dark:text-slate-400">
            First-class datasets â€” draft â†’ published â†’ archived ({pageData?.total ?? 0} total)
          </p>
        </div>
        <div className="flex gap-2">
          <input className="input w-52" placeholder="Search datasetsâ€¦" value={q} onChange={(e) => { setQ(e.target.value); setPage(1); }} />
          <select className="input w-36" value={status} onChange={(e) => { setStatus(e.target.value); setPage(1); }}>
            <option value="">All statuses</option>
            <option value="draft">draft</option><option value="published">published</option><option value="archived">archived</option>
          </select>
        </div>
      </div>

      {isLoading && <div className="panel p-6 text-sm text-slate-500">Loadingâ€¦</div>}
      {!isLoading && (pageData?.items.length ?? 0) === 0 && (
        <div className="panel p-6 text-sm text-slate-500">No datasets yet â€” OCR a document and complete the dataset form to create one.</div>
      )}

      <div className="space-y-3">
        {(pageData?.items ?? []).map((d) => {
          const expanded = openId === d.id;
          return (
            <div key={d.id} className="panel overflow-hidden">
              <div className="flex flex-wrap items-center gap-x-4 gap-y-1 px-4 py-3">
                <button type="button" className="min-w-0 flex-1 text-left" onClick={() => setOpenId(expanded ? null : d.id)}>
                  <span className="block truncate font-medium text-slate-900 dark:text-slate-100">{d.name}</span>
                  <span className="mt-0.5 block truncate text-xs text-slate-500">
                    {orgName(d.organization_id)} Â· {catName(d.category_id)} Â· {colName(d.collection_id)}
                    {d.coverage_start && ` Â· ${d.coverage_start} â†’ ${d.coverage_end ?? "â€¦"}`}
                  </span>
                </button>
                <span className={`badge ${STATUS_BADGE[d.status] ?? STATUS_BADGE.draft}`}>{d.status}</span>
                {d.published_at && <span className="text-xs text-slate-400">{d.published_at.slice(0, 10)}</span>}
                <span className="text-xs text-slate-400">{d.file_name ?? "no file"}</span>
                {canEdit && (
                  <div className="flex items-center gap-1.5">
                    {d.status !== "published" ? (
                      <button type="button" className="rounded-md bg-emerald-500/10 px-2.5 py-1 text-xs font-medium text-emerald-600 hover:bg-emerald-500/20 disabled:opacity-50"
                        disabled={publish.isPending} onClick={() => publish.mutate(d.id)}>
                        Publish
                      </button>
                    ) : (
                      <button type="button" className="rounded-md bg-amber-500/10 px-2.5 py-1 text-xs font-medium text-amber-600 hover:bg-amber-500/20 disabled:opacity-50"
                        disabled={unpublish.isPending} onClick={() => unpublish.mutate(d.id)}>
                        Unpublish
                      </button>
                    )}
                    <button type="button" className="rounded-md px-2 py-1 text-xs text-red-500 hover:bg-red-50"
                      onClick={() => remove.mutate(d.id)}>
                      Delete
                    </button>
                    <button type="button" className="rounded-md px-2 py-1 text-xs text-slate-500 hover:bg-slate-100" onClick={() => setOpenId(expanded ? null : d.id)}>
                      {expanded ? "â–²" : "â–¼"}
                    </button>
                  </div>
                )}
              </div>

              {expanded && (
                <div className="border-t border-slate-200 px-4 py-3 dark:border-white/10">
                  {d.description && <p className="mb-2 text-sm text-slate-600 dark:text-slate-300">{d.description}</p>}
                  <div className="mb-2 flex flex-wrap items-center gap-2">
                    {d.record_id && (
                      <a className="btn-ghost px-2.5 py-1 text-xs" href={`/records/${d.record_id}`} target="_blank" rel="noreferrer">Source record â†—</a>
                    )}
                    {d.url && <a href={d.url} target="_blank" rel="noreferrer" className="btn-ghost px-2.5 py-1 text-xs">Source link â†—</a>}
                    {d.file_base64 && d.file_name && (
                      <button type="button" className="btn-secondary px-2.5 py-1 text-xs" onClick={() => downloadFile(d)}>
                        â¬‡ {d.file_name}
                      </button>
                    )}
                    {d.record_id && (
                      <button type="button" className="btn-secondary px-2.5 py-1 text-xs"
                        onClick={() => { void api.getRecord(d.record_id!).then((r) => {
                          const csv = String(r.data?.csv ?? "");
                          if (csv) downloadText(`${d.name.replace(/[^\w.-]+/g, "_")}.csv`, csv, "text/csv");
                        }); }}>
                        â¬‡ CSV
                      </button>
                    )}
                    {d.record_id && (
                      <button type="button" className="btn-secondary px-2.5 py-1 text-xs"
                        onClick={() => { void api.getRecord(d.record_id!).then((r) => {
                          const md = String(r.data?.markdown ?? r.data?.full_text ?? "");
                          if (md) downloadText(`${d.name.replace(/[^\w.-]+/g, "_")}.md`, md, "text/markdown");
                        }); }}>
                        â¬‡ .md
                      </button>
                    )}
                  </div>

                  {d.record_id && (
                    <DatasetPreview recordId={d.record_id} datasetName={d.name} />
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {pageData && pageData.total_pages > 1 && (
        <div className="mt-3 flex items-center justify-between text-sm text-slate-500">
          <span>{pageData.total} datasets · page {page}/{pageData.total_pages}</span>
          <div className="flex gap-2">
            <button type="button" className="btn-secondary px-3 py-1.5 text-xs" disabled={page <= 1} onClick={() => setPage((p) => Math.max(1, p - 1))}>Prev</button>
            <button type="button" className="btn-secondary px-3 py-1.5 text-xs" disabled={page >= pageData.total_pages} onClick={() => setPage((p) => Math.min(pageData.total_pages, p + 1))}>Next</button>
          </div>
        </div>
      )}
    </div>
  );
}

/** Rendered Markdown preview of the linked record's auto-saved artifact. */
function DatasetPreview({ recordId, datasetName }: { recordId: string; datasetName: string }) {
  const [view, setView] = useState<"markdown" | "csv">("markdown");
  const [raw, setRaw] = useState(false);
  const { data: rec } = useQuery({
    queryKey: ["record", recordId],
    queryFn: () => api.getRecord(recordId),
  });
  const markdown = String(rec?.data?.markdown ?? rec?.data?.full_text ?? "");
  const csv = String(rec?.data?.csv ?? "");

  if (!markdown && !csv) return null;
  return (
    <div className="mt-3 rounded-xl border border-slate-200 bg-slate-50/60 p-3 dark:border-white/10 dark:bg-white/5">
      <div className="mb-2 flex flex-wrap items-center gap-2">
        <span className="text-[11px] font-semibold uppercase tracking-wide text-slate-500">Preview — {datasetName}</span>
        <div className="flex items-center rounded-lg border border-slate-200 bg-white p-0.5 shadow-sm">
          <button type="button" onClick={() => setView("markdown")}
            className={`rounded-md px-2 py-0.5 text-[11px] font-medium transition-colors ${view === "markdown" ? "bg-slate-100 text-slate-950" : "text-slate-500"}`}>
            Markdown
          </button>
          <button type="button" onClick={() => setView("csv")}
            className={`rounded-md px-2 py-0.5 text-[11px] font-medium transition-colors ${view === "csv" ? "bg-slate-100 text-slate-950" : "text-slate-500"}`}>
            CSV
          </button>
        </div>
        <button type="button" className="rounded-md px-2 py-0.5 text-[11px] text-slate-400 hover:bg-slate-100 hover:text-slate-700"
          onClick={() => setRaw((r) => !r)}>
          {raw ? "Rendered" : "Raw source"}
        </button>
      </div>
      {view === "markdown" ? (
        raw ? (
          <pre className="max-h-72 overflow-auto whitespace-pre-wrap break-all rounded-lg bg-white p-3 font-mono text-[11px] text-slate-700 dark:bg-white/5 dark:text-slate-300">{markdown}</pre>
        ) : (
          <MarkdownView source={markdown} maxHeight="288px" showCopy={false} />
        )
      ) : raw ? (
        <pre className="max-h-72 overflow-auto whitespace-pre-wrap break-all rounded-lg bg-white p-3 font-mono text-[11px] text-slate-700 dark:bg-white/5 dark:text-slate-300">{csv}</pre>
      ) : (
        <CsvTable csv={csv} maxHeight={288} />
      )}
    </div>
  );
}

/** Tiny CSV renderer: rows -> table (quote-aware-ish, good enough for previews). */
function CsvTable({ csv, maxHeight }: { csv: string; maxHeight: number }) {
  const lines = csv.replace(/^\uFEFF/, "").split(/\r?\n/).filter((l) => l.trim() !== "");
  const rows = lines.map((l) => {
    const cells: string[] = [];
    let cur = "";
    let inQ = false;
    for (let i = 0; i < l.length; i++) {
      const ch = l[i];
      if (inQ) {
        if (ch === '"' && l[i + 1] === '"') { cur += '"'; i++; }
        else if (ch === '"') inQ = false;
        else cur += ch;
      } else if (ch === '"') inQ = true;
      else if (ch === ",") { cells.push(cur); cur = ""; }
      else cur += ch;
    }
    cells.push(cur);
    return cells;
  });
  if (rows.length === 0) return <div className="text-xs text-slate-400">(empty CSV)</div>;
  const [header, ...body] = rows;
  return (
    <div className="overflow-auto rounded-lg border border-slate-200 bg-white" style={{ maxHeight }}>
      <table className="w-full border-collapse text-xs">
        <thead className="sticky top-0">
          <tr className="bg-slate-100">
            {header.map((h, i) => <th key={i} className="border-b border-r border-slate-200 px-2.5 py-1.5 text-left font-semibold text-slate-800 last:border-r-0">{h}</th>)}
          </tr>
        </thead>
        <tbody>
          {body.map((r, ri) => (
            <tr key={ri} className="border-b border-slate-100 odd:bg-white even:bg-slate-50/60 last:border-b-0">
              {r.map((c, ci) => <td key={ci} className="border-r border-slate-100 px-2.5 py-1.5 text-slate-700 last:border-r-0">{c}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
