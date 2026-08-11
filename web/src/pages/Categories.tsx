import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, type CategoryOut } from "../api/client";
import { getUser } from "../api/client";

/**
 * Categories — managed taxonomy tree (e.g. Economics > Prices > CPI).
 * The dataset form will pick from these instead of free text.
 */
export default function Categories() {
  const qc = useQueryClient();
  const user = getUser();
  const canEdit = user?.role === "admin" || user?.role === "editor";
  const [name, setName] = useState("");
  const [parentId, setParentId] = useState<number | null>(null);
  const [description, setDescription] = useState("");
  const [editing, setEditing] = useState<CategoryOut | null>(null);

  const { data: cats, isLoading } = useQuery({ queryKey: ["categories"], queryFn: api.listCategories });

  const invalidate = () => {
    qc.invalidateQueries({ queryKey: ["categories"] });
  };

  const create = useMutation({
    mutationFn: () => api.createCategory({ name, parent_id: parentId, description: description || null }),
    onSuccess: () => { setName(""); setDescription(""); invalidate(); },
  });
  const update = useMutation({
    mutationFn: () => api.updateCategory(editing!.id, { name, parent_id: parentId, description: description || null }),
    onSuccess: () => { setEditing(null); setName(""); setDescription(""); invalidate(); },
  });
  const remove = useMutation({
    mutationFn: (id: number) => api.deleteCategory(id),
    onSuccess: invalidate,
  });

  const tree = (parent: number | null, depth: number): CategoryOut[] =>
    (cats ?? [])
      .filter((c) => c.parent_id === parent)
      .sort((a, b) => a.sort - b.sort)
      .flatMap((c) => [c, ...tree(c.id, depth + 1)]);

  const rows = tree(null, 0);

  return (
    <div className="p-6 max-w-6xl">
      <h1 className="display mb-1">Categories</h1>
      <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">Managed taxonomy for datasets (tree)</p>

      {canEdit && (
        <div className="panel mb-4 flex flex-wrap items-end gap-2 p-3">
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Name</label>
            <input className="input w-56" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Consumer Price Index" />
          </div>
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Parent</label>
            <select className="input w-44" value={parentId ?? ""} onChange={(e) => setParentId(e.target.value ? Number(e.target.value) : null)}>
              <option value="">(root)</option>
              {(cats ?? []).filter((c) => c.id !== editing?.id).map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>
          <div className="flex-1">
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Description</label>
            <input className="input w-full" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Optional" />
          </div>
          <button
            type="button"
            className="btn-primary px-4 py-1.5 text-xs"
            disabled={!name.trim() || create.isPending || update.isPending}
            onClick={() => (editing ? update.mutate() : create.mutate())}
          >
            {editing ? "Save changes" : "+ Add category"}
          </button>
          {editing && (
            <button type="button" className="btn-ghost px-3 py-1.5 text-xs" onClick={() => { setEditing(null); setName(""); setParentId(null); setDescription(""); }}>
              Cancel
            </button>
          )}
        </div>
      )}

      <div className="panel overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-slate-200 bg-slate-50/60 dark:bg-white/5">
            <tr>
              <th className="th">Name</th>
              <th className="th">Parent</th>
              <th className="th">Description</th>
              <th className="th w-28">Actions</th>
            </tr>
          </thead>
          <tbody>
            {isLoading && <tr><td className="td text-slate-500" colSpan={4}>Loading…</td></tr>}
            {!isLoading && rows.length === 0 && (
              <tr><td className="td text-slate-500" colSpan={4}>No categories yet.</td></tr>
            )}
            {!isLoading && rows.map((c) => {
              const depth = (() => { let d = 0; let p = c.parent_id; const byId = new Map((cats ?? []).map((x) => [x.id, x])); while (p !== null && byId.has(p)) { d++; p = byId.get(p)!.parent_id; } return d; })();
              const parent = (cats ?? []).find((x) => x.id === c.parent_id);
              return (
                <tr key={c.id} className="border-b border-slate-100 last:border-0 hover:bg-slate-50/60 dark:border-white/5 dark:hover:bg-white/5">
                  <td className="td font-medium text-slate-900 dark:text-slate-100" style={{ paddingLeft: `${12 + depth * 18}px` }}>
                    {depth > 0 && <span className="mr-1 text-slate-400">└</span>}{c.name}
                  </td>
                  <td className="td text-slate-500">{parent ? parent.name : "—"}</td>
                  <td className="td text-slate-500">{c.description ?? "—"}</td>
                  <td className="td py-1.5">
                    {canEdit && (
                      <div className="flex items-center gap-1.5">
                        <button type="button" className="rounded-md px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-900"
                          onClick={() => { setEditing(c); setName(c.name); setParentId(c.parent_id); setDescription(c.description ?? ""); }}>
                          Edit
                        </button>
                        <button type="button" className="rounded-md px-2 py-1 text-xs text-red-500 hover:bg-red-50"
                          onClick={() => { if (confirm(`Delete category "${c.name}"?`)) remove.mutate(c.id); }}>
                          Delete
                        </button>
                      </div>
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
