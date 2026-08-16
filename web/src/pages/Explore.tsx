import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";

/**
 * Explore — public, no-login browsing of published datasets.
 * The "sharing" half of Romdoul Data Sharing: browse by category/collection,
 * view metadata and download the CSV/Markdown artifacts.
 */
export default function Explore() {
  const [q, setQ] = useState("");
  const [categoryId, setCategoryId] = useState<number | null>(null);
  const [collectionId, setCollectionId] = useState<number | null>(null);
  const [openId, setOpenId] = useState<string | null>(null);

  const { data: page, isLoading } = useQuery({
    queryKey: ["datasets", "public", q, categoryId, collectionId],
    queryFn: () => api.listDatasets({ public: true, page_size: 100, q: q || undefined, category_id: categoryId ?? undefined, collection_id: collectionId ?? undefined }),
  });
  const { data: cats } = useQuery({ queryKey: ["categories"], queryFn: api.listCategories });
  const { data: cols } = useQuery({ queryKey: ["collections"], queryFn: api.listCollections });
  const { data: orgs } = useQuery({ queryKey: ["organizations"], queryFn: api.listOrganizations });

  const catName = (id: number | null) => cats?.find((c) => c.id === id)?.name ?? "—";
  const colName = (id: number | null) => cols?.find((c) => c.id === id)?.name ?? "—";
  const orgName = (id: number | null) => orgs?.find((o) => o.id === id)?.name ?? "—";

  return (
    <div className="p-6 max-w-6xl">
      <div className="mb-1 text-2xl font-semibold tracking-tight text-slate-950 dark:text-slate-50">Explore datasets</div>
      <p className="mb-5 text-sm text-slate-600 dark:text-slate-400">
        Public open datasets — browse, preview and download. No sign-in needed.
      </p>

      <div className="panel mb-4 flex flex-wrap gap-2 p-3">
        <input className="input w-56" placeholder="Search datasets…" value={q} onChange={(e) => setQ(e.target.value)} />
        <select className="input w-44" value={categoryId ?? ""} onChange={(e) => setCategoryId(e.target.value ? Number(e.target.value) : null)}>
          <option value="">All categories</option>
          {(cats ?? []).map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <select className="input w-44" value={collectionId ?? ""} onChange={(e) => setCollectionId(e.target.value ? Number(e.target.value) : null)}>
          <option value="">All collections</option>
          {(cols ?? []).map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>

      {isLoading && <div className="panel p-6 text-sm text-slate-500">Loading…</div>}
      {!isLoading && (page?.items.length ?? 0) === 0 && (
        <div className="panel p-6 text-sm text-slate-500">No published datasets match. Publish one from the Datasets page.</div>
      )}

      <div className="space-y-3">
        {(page?.items ?? []).map((d) => {
          const expanded = openId === d.id;
          return (
            <div key={d.id} className="panel overflow-hidden">
              <button type="button" className="flex w-full flex-wrap items-center gap-x-4 gap-y-1 px-4 py-3 text-left hover:bg-slate-50/60 dark:hover:bg-white/5"
                onClick={() => setOpenId(expanded ? null : d.id)}>
                <span className="min-w-0 flex-1">
                  <span className="block truncate font-medium text-slate-900 dark:text-slate-100">{d.name}</span>
                  <span className="mt-0.5 block truncate text-xs text-slate-500">
                    {orgName(d.organization_id)} · {catName(d.category_id)} · {colName(d.collection_id)}
                    {d.coverage_start && ` · ${d.coverage_start} → ${d.coverage_end ?? "…"}`}
                    {d.frequency && ` · ${d.frequency}`}
                  </span>
                </span>
                <span className="badge border-emerald-500/30 bg-emerald-500/10 text-emerald-600">published</span>
                <span className="text-xs text-slate-400">{d.published_at?.slice(0, 10)}</span>
                <span className="text-xs text-slate-500">{expanded ? "▲" : "▼"}</span>
              </button>

              {expanded && (
                <div className="border-t border-slate-200 px-4 py-3 dark:border-white/10">
                  {d.description && <p className="mb-2 text-sm text-slate-600 dark:text-slate-300">{d.description}</p>}
                  <div className="flex flex-wrap items-center gap-2">
                    {d.file_name && (
                      <a className="btn-primary px-3 py-1.5 text-xs" href={api.datasetFileUrl(d.id)}>
                        ⬇ Download {d.file_name}
                      </a>
                    )}
                    {d.url && <a href={d.url} target="_blank" rel="noreferrer" className="btn-ghost px-3 py-1.5 text-xs">Source link ↗</a>}
                    {!d.file_name && <span className="text-xs text-slate-400">No embedded file — contact the publisher for the data.</span>}
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
