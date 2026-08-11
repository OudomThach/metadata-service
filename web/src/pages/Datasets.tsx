import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, getUser, type DatasetOut } from "../api/client";

/**
 * Datasets — first-class entities with draft -> published -> archived.
 * Published datasets are visible on the public Explore page.
 */
export default function Datasets() {
  const qc = useQueryClient();
  const me = getUser();
  const canEdit = me?.role === "admin" || me?.role === "editor";
  const [status, setStatus] = useState("");
  const [q, setQ] = useState("");
  const [openId, setOpenId] = useState<string | null>(null);

  const { data: page, isLoading } = useQuery({
    queryKey: ["datasets", status, q],
    queryFn: () => api.listDatasets({ page_size: 100, status: status || undefined, q: q || undefined }),
  });
  const { data: orgs } = useQuery({ queryKey: ["organizations"], queryFn: api.listOrganizations });
  const { data: cats } = useQuery({ queryKey: ["categories"], queryFn: api.listCategories });
  const { data: cols } = useQuery({ queryKey: ["collections"], queryFn: api.listCollections });

  const invalidate = () => {
    qc.invalidateQueries({ queryKey: ["datasets"] });
    qc.invalidateQueries({ queryKey: ["records"] });
  };
  const publish = useMutation({ mutationFn: (id: string) => api.publishDataset(id), onSuccess: invalidate });
  const unpublish = useMutation({ mutationFn: (id: string) => api.unpublishDataset(id), onSuccess: invalidate });
  const remove = useMutation({ mutationFn: (id: string) => api.deleteDataset(id), onSuccess: invalidate });

  const orgName = (id: number | null) => orgs?.find((o) => o.id === id)?.name ?? "—";
  const catName = (id: number | null) => cats?.find((c) => c.id === id)?.name ?? "—";
  const colName = (id: number | null) => cols?.find((c) => c.id === id)?.name ?? "—";

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
            First-class datasets — draft → published → archived ({page?.total ?? 0} total)
          </p>
        </div>
        <div className="flex gap-2">
          <input className="input w-52" placeholder="Search datasets…" value={q} onChange={(e) => setQ(e.target.value)} />
          <select className="input w-36" value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="">All statuses</option>
            <option value="draft">draft</option><option value="published">published</option><option value="archived">archived</option>
          </select>
        </div>
      </div>

      {isLoading && <div className="panel p-6 text-sm text-slate-500">Loading…</div>}
      {!isLoading && (page?.items.length ?? 0) === 0 && (
        <div className="panel p-6 text-sm text-slate-500">No datasets yet — OCR a document and complete the dataset form to create one.</div>
      )}

      <div className="space-y-3">
        {(page?.items ?? []).map((d) => {
          const expanded = openId === d.id;
          return (
            <div key={d.id} className="panel overflow-hidden">
              <div className="flex flex-wrap items-center gap-x-4 gap-y-1 px-4 py-3">
                <button type="button" className="min-w-0 flex-1 text-left" onClick={() => setOpenId(expanded ? null : d.id)}>
                  <span className="block truncate font-medium text-slate-900 dark:text-slate-100">{d.name}</span>
                  <span className="mt-0.5 block truncate text-xs text-slate-500">
                    {orgName(d.organization_id)} · {catName(d.category_id)} · {colName(d.collection_id)}
                    {d.coverage_start && ` · ${d.coverage_start} → ${d.coverage_end ?? "…"}`}
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
                      onClick={() => { if (confirm(`Delete dataset "${d.name}"?`)) remove.mutate(d.id); }}>
                      Delete
                    </button>
                    <button type="button" className="rounded-md px-2 py-1 text-xs text-slate-500 hover:bg-slate-100" onClick={() => setOpenId(expanded ? null : d.id)}>
                      {expanded ? "▲" : "▼"}
                    </button>
                  </div>
                )}
              </div>

              {expanded && (
                <div className="border-t border-slate-200 px-4 py-3 dark:border-white/10">
                  {d.description && <p className="mb-2 text-sm text-slate-600 dark:text-slate-300">{d.description}</p>}
                  <div className="mb-2 flex flex-wrap items-center gap-2">
                    {d.record_id && (
                      <a className="btn-ghost px-2.5 py-1 text-xs" href={`/records/${d.record_id}`} target="_blank" rel="noreferrer">Source record ↗</a>
                    )}
                    {d.url && <a href={d.url} target="_blank" rel="noreferrer" className="btn-ghost px-2.5 py-1 text-xs">Source link ↗</a>}
                    {d.file_base64 && d.file_name && (
                      <button type="button" className="btn-secondary px-2.5 py-1 text-xs" onClick={() => downloadFile(d)}>
                        ⬇ {d.file_name}
                      </button>
                    )}
                    {d.record_id && (
                      <button type="button" className="btn-secondary px-2.5 py-1 text-xs"
                        onClick={() => { void api.getRecord(d.record_id!).then((r) => {
                          const csv = String(r.data?.csv ?? "");
                          if (csv) downloadText(`${d.name.replace(/[^\w.-]+/g, "_")}.csv`, csv, "text/csv");
                        }); }}>
                        ⬇ CSV
                      </button>
                    )}
                    {d.record_id && (
                      <button type="button" className="btn-secondary px-2.5 py-1 text-xs"
                        onClick={() => { void api.getRecord(d.record_id!).then((r) => {
                          const md = String(r.data?.markdown ?? r.data?.full_text ?? "");
                          if (md) downloadText(`${d.name.replace(/[^\w.-]+/g, "_")}.md`, md, "text/markdown");
                        }); }}>
                        ⬇ .md
                      </button>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
