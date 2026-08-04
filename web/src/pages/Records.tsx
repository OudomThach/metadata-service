import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api, type QueryParams } from "../api/client";
import StatusBadge from "../components/StatusBadge";

const PAGE_SIZE = 25;

export default function Records() {
  const [filters, setFilters] = useState<QueryParams>({ page: 1, page_size: PAGE_SIZE, sort: "created_at:desc" });
  const [search, setSearch] = useState("");

  const { data: meta } = useQuery({ queryKey: ["meta"], queryFn: api.meta });
  const { data: page, isLoading, isFetching } = useQuery({
    queryKey: ["records", filters],
    queryFn: () => api.listRecords(filters),
  });

  const apply = (patch: Partial<QueryParams>) => setFilters((f) => ({ ...f, ...patch, page: 1 }));

  return (
    <div className="p-6 max-w-7xl">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-semibold text-slate-100">Records</h1>
        <div className="flex gap-2">
          <a className="btn-ghost" href={api.exportUrl("csv", filters)}>CSV</a>
          <a className="btn-ghost" href={api.exportUrl("json", filters)}>JSON</a>
        </div>
      </div>

      <div className="card p-3 mb-4 flex flex-wrap gap-2">
        <input className="input w-64" placeholder="Search data…" value={search}
               onChange={(e) => setSearch(e.target.value)}
               onKeyDown={(e) => { if (e.key === "Enter") apply({ q: search }); }} />
        <select className="input" value={filters.type ?? ""} onChange={(e) => apply({ type: e.target.value || undefined })}>
          <option value="">All types</option>
          {(meta?.types ?? []).map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
        <select className="input" value={filters.domain ?? ""} onChange={(e) => apply({ domain: e.target.value || undefined })}>
          <option value="">All domains</option>
          {(meta?.domains ?? []).map((d) => <option key={d} value={d}>{d}</option>)}
        </select>
        <select className="input" value={filters.status ?? ""} onChange={(e) => apply({ status: e.target.value || undefined })}>
          <option value="">All statuses</option>
          <option value="raw">raw</option>
          <option value="edited">edited</option>
          <option value="verified">verified</option>
        </select>
        <input type="date" className="input" value={filters.business_from ?? ""}
               onChange={(e) => apply({ business_from: e.target.value || undefined })} />
        <span className="self-center text-slate-500 text-sm">→</span>
        <input type="date" className="input" value={filters.business_to ?? ""}
               onChange={(e) => apply({ business_to: e.target.value || undefined })} />
        <button className="btn-ghost" onClick={() => { setSearch(""); setFilters({ page: 1, page_size: PAGE_SIZE, sort: "created_at:desc" }); }}>
          Reset
        </button>
        {isFetching && <span className="self-center text-xs text-slate-500">…</span>}
      </div>

      <div className="card overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-base-600/60 bg-base-850">
            <tr>
              <th className="th">Type</th>
              <th className="th">Status</th>
              <th className="th">Domain</th>
              <th className="th">Business date</th>
              <th className="th">Tags</th>
              <th className="th">Created</th>
              <th className="th">Edited</th>
              <th className="th">Source</th>
            </tr>
          </thead>
          <tbody>
            {isLoading && (
              <tr><td className="td text-slate-500" colSpan={8}>Loading…</td></tr>
            )}
            {page?.items.length === 0 && (
              <tr><td className="td text-slate-500" colSpan={8}>No records match the filters.</td></tr>
            )}
            {page?.items.map((r) => (
              <tr key={r.id} className="border-b border-base-600/40 hover:bg-base-700/40">
                <td className="td">
                  <Link to={`/records/${r.id}`} className="text-accent hover:underline">{r.type}</Link>
                </td>
                <td className="td"><StatusBadge status={r.status} /></td>
                <td className="td text-slate-300">{r.domain ?? "—"}</td>
                <td className="td text-slate-400">{r.business_date ?? "—"}</td>
                <td className="td text-slate-400">{r.tags?.join(", ") ?? "—"}</td>
                <td className="td text-slate-400">{r.created_at?.slice(0, 10)}</td>
                <td className="td text-slate-400">
                  {r.edit_count > 0 ? `×${r.edit_count} ${r.edited_at?.slice(0, 10) ?? ""}` : "—"}
                </td>
                <td className="td text-slate-400 truncate max-w-[180px]">{r.source_model ?? r.source_system ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {page && page.total_pages > 1 && (
        <div className="flex items-center justify-between mt-4 text-sm text-slate-400">
          <span>{page.total} records · page {page.page}/{page.total_pages}</span>
          <div className="flex gap-2">
            <button className="btn-ghost" disabled={page.page <= 1} onClick={() => setFilters((f) => ({ ...f, page: f.page! - 1 }))}>
              Prev
            </button>
            <button className="btn-ghost" disabled={page.page >= page.total_pages} onClick={() => setFilters((f) => ({ ...f, page: f.page! + 1 }))}>
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
