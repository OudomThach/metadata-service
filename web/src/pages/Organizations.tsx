import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, type OrganizationOut } from "../api/client";
import { getUser } from "../api/client";

/** Organizations — the publishers behind records, collections and datasets. */
export default function Organizations() {
  const qc = useQueryClient();
  const user = getUser();
  const canEdit = user?.role === "admin" || user?.role === "editor";
  const [name, setName] = useState("");
  const [orgType, setOrgType] = useState("government");
  const [contact, setContact] = useState("");
  const [editing, setEditing] = useState<OrganizationOut | null>(null);

  const { data: orgs, isLoading } = useQuery({ queryKey: ["organizations"], queryFn: api.listOrganizations });
  const invalidate = () => qc.invalidateQueries({ queryKey: ["organizations"] });

  const create = useMutation({
    mutationFn: () => api.createOrganization({ name, org_type: orgType, contact: contact.trim() ? { email: contact.trim() } : null }),
    onSuccess: () => { setName(""); setContact(""); invalidate(); },
  });
  const update = useMutation({
    mutationFn: () => api.updateOrganization(editing!.id, { name, org_type: orgType, contact: contact.trim() ? { email: contact.trim() } : null }),
    onSuccess: () => { setEditing(null); setName(""); setContact(""); invalidate(); },
  });
  const remove = useMutation({ mutationFn: (id: number) => api.deleteOrganization(id), onSuccess: invalidate });

  const TYPE_BADGE: Record<string, string> = {
    government: "border-accent/30 bg-accent/10 text-accent",
    private: "border-accent2/30 bg-accent2/10 text-accent2",
    ngo: "border-emerald-500/30 bg-emerald-500/10 text-emerald-600",
    other: "border-slate-300 bg-slate-100 text-slate-600",
  };

  return (
    <div className="p-6 max-w-6xl">
      <h1 className="display mb-1">Organizations</h1>
      <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">Publishers behind datasets and collections</p>

      {canEdit && (
        <div className="panel mb-4 flex flex-wrap items-end gap-2 p-3">
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Name</label>
            <input className="input w-56" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. NIS Cambodia" />
          </div>
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Type</label>
            <select className="input w-36" value={orgType} onChange={(e) => setOrgType(e.target.value)}>
              <option value="government">government</option>
              <option value="private">private</option>
              <option value="ngo">ngo</option>
              <option value="other">other</option>
            </select>
          </div>
          <div className="flex-1">
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Contact email</label>
            <input className="input w-full" value={contact} onChange={(e) => setContact(e.target.value)} placeholder="Optional" />
          </div>
          <button type="button" className="btn-primary px-4 py-1.5 text-xs"
            disabled={!name.trim() || create.isPending || update.isPending}
            onClick={() => (editing ? update.mutate() : create.mutate())}>
            {editing ? "Save changes" : "+ Add organization"}
          </button>
          {editing && (
            <button type="button" className="btn-ghost px-3 py-1.5 text-xs"
              onClick={() => { setEditing(null); setName(""); setOrgType("government"); setContact(""); }}>
              Cancel
            </button>
          )}
        </div>
      )}

      <div className="panel overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-slate-200 bg-slate-50/60 dark:bg-white/5">
            <tr><th className="th">Name</th><th className="th">Type</th><th className="th">Contact</th><th className="th w-28">Actions</th></tr>
          </thead>
          <tbody>
            {isLoading && <tr><td className="td text-slate-500" colSpan={4}>Loading…</td></tr>}
            {!isLoading && (orgs ?? []).length === 0 && <tr><td className="td text-slate-500" colSpan={4}>No organizations yet.</td></tr>}
            {!isLoading && (orgs ?? []).map((o) => (
              <tr key={o.id} className="border-b border-slate-100 last:border-0 hover:bg-slate-50/60 dark:border-white/5 dark:hover:bg-white/5">
                <td className="td font-medium text-slate-900 dark:text-slate-100">{o.name}</td>
                <td className="td"><span className={`badge ${TYPE_BADGE[o.org_type] ?? TYPE_BADGE.other}`}>{o.org_type}</span></td>
                <td className="td text-slate-500">{(o.contact as { email?: string } | null)?.email ?? "—"}</td>
                <td className="td py-1.5">
                  {canEdit && (
                    <div className="flex items-center gap-1.5">
                      <button type="button" className="rounded-md px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-900"
                        onClick={() => { setEditing(o); setName(o.name); setOrgType(o.org_type); setContact((o.contact as { email?: string } | null)?.email ?? ""); }}>
                        Edit
                      </button>
                      <button type="button" className="rounded-md px-2 py-1 text-xs text-red-500 hover:bg-red-50"
                        onClick={() => { if (confirm(`Delete organization "${o.name}"?`)) remove.mutate(o.id); }}>
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
