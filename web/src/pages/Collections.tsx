import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, type CollectionOut } from "../api/client";
import { getUser } from "../api/client";

/** Collections — curated groups of datasets (e.g. NIS Publications). */
export default function Collections() {
  const qc = useQueryClient();
  const user = getUser();
  const canEdit = user?.role === "admin" || user?.role === "editor";
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [orgId, setOrgId] = useState<number | null>(null);
  const [editing, setEditing] = useState<CollectionOut | null>(null);

  const { data: cols, isLoading } = useQuery({ queryKey: ["collections"], queryFn: api.listCollections });
  const { data: orgs } = useQuery({ queryKey: ["organizations"], queryFn: api.listOrganizations });
  const invalidate = () => qc.invalidateQueries({ queryKey: ["collections"] });

  const create = useMutation({
    mutationFn: () => api.createCollection({ name, description: description || null, organization_id: orgId }),
    onSuccess: () => { setName(""); setDescription(""); invalidate(); },
  });
  const update = useMutation({
    mutationFn: () => api.updateCollection(editing!.id, { name, description: description || null, organization_id: orgId }),
    onSuccess: () => { setEditing(null); setName(""); setDescription(""); invalidate(); },
  });
  const remove = useMutation({ mutationFn: (id: number) => api.deleteCollection(id), onSuccess: invalidate });

  return (
    <div className="p-6 max-w-6xl">
      <h1 className="display mb-1">Collections</h1>
      <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">Curated groups of datasets, optionally owned by an organization</p>

      {canEdit && (
        <div className="panel mb-4 flex flex-wrap items-end gap-2 p-3">
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Name</label>
            <input className="input w-56" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. NIS Publications" />
          </div>
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Organization</label>
            <select className="input w-44" value={orgId ?? ""} onChange={(e) => setOrgId(e.target.value ? Number(e.target.value) : null)}>
              <option value="">(none)</option>
              {(orgs ?? []).map((o) => <option key={o.id} value={o.id}>{o.name}</option>)}
            </select>
          </div>
          <div className="flex-1">
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Description</label>
            <input className="input w-full" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Optional" />
          </div>
          <button type="button" className="btn-primary px-4 py-1.5 text-xs"
            disabled={!name.trim() || create.isPending || update.isPending}
            onClick={() => (editing ? update.mutate() : create.mutate())}>
            {editing ? "Save changes" : "+ Add collection"}
          </button>
          {editing && (
            <button type="button" className="btn-ghost px-3 py-1.5 text-xs"
              onClick={() => { setEditing(null); setName(""); setDescription(""); setOrgId(null); }}>
              Cancel
            </button>
          )}
        </div>
      )}

      <div className="panel overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-slate-200 bg-slate-50/60 dark:bg-white/5">
            <tr><th className="th">Name</th><th className="th">Organization</th><th className="th">Description</th><th className="th w-28">Actions</th></tr>
          </thead>
          <tbody>
            {isLoading && <tr><td className="td text-slate-500" colSpan={4}>Loading…</td></tr>}
            {!isLoading && (cols ?? []).length === 0 && <tr><td className="td text-slate-500" colSpan={4}>No collections yet.</td></tr>}
            {!isLoading && (cols ?? []).map((c) => (
              <tr key={c.id} className="border-b border-slate-100 last:border-0 hover:bg-slate-50/60 dark:border-white/5 dark:hover:bg-white/5">
                <td className="td font-medium text-slate-900 dark:text-slate-100">{c.name}</td>
                <td className="td text-slate-500">{(orgs ?? []).find((o) => o.id === c.organization_id)?.name ?? "—"}</td>
                <td className="td text-slate-500">{c.description ?? "—"}</td>
                <td className="td py-1.5">
                  {canEdit && (
                    <div className="flex items-center gap-1.5">
                      <button type="button" className="rounded-md px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-900"
                        onClick={() => { setEditing(c); setName(c.name); setDescription(c.description ?? ""); setOrgId(c.organization_id); }}>
                        Edit
                      </button>
                      <button type="button" className="rounded-md px-2 py-1 text-xs text-red-500 hover:bg-red-50"
                        onClick={() => { if (confirm(`Delete collection "${c.name}"?`)) remove.mutate(c.id); }}>
                        Delete
                      </button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
