import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, getUser } from "../api/client";

/** Users — admin management: create, change role/org, delete. */
export default function Users() {
  const qc = useQueryClient();
  const me = getUser();
  const isAdmin = me?.role === "admin";
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("viewer");
  const [orgId, setOrgId] = useState<number | null>(null);

  const { data: users, isLoading } = useQuery({ queryKey: ["users"], queryFn: api.listUsers, enabled: isAdmin });
  const { data: orgs } = useQuery({ queryKey: ["organizations"], queryFn: api.listOrganizations, enabled: isAdmin });
  const invalidate = () => { qc.invalidateQueries({ queryKey: ["users"] }); };

  const create = useMutation({
    mutationFn: () => api.createUser({ username, password, role, organization_id: orgId }),
    onSuccess: () => { setUsername(""); setPassword(""); invalidate(); },
    onError: (err: Error) => window.alert(err.message),
  });
  const update = useMutation({
    mutationFn: ({ id, patch }: { id: number; patch: { role?: string; organization_id?: number | null } }) => api.updateUser(id, patch),
    onSuccess: invalidate,
  });
  const remove = useMutation({ mutationFn: (id: number) => api.deleteUser(id), onSuccess: invalidate });

  if (!isAdmin) {
    return <div className="p-6 text-sm text-slate-500">Admin role required to manage users.</div>;
  }

  const ROLE_BADGE: Record<string, string> = {
    admin: "border-accent/30 bg-accent/10 text-accent",
    editor: "border-accent2/30 bg-accent2/10 text-accent2",
    viewer: "border-slate-300 bg-slate-100 text-slate-600",
  };

  return (
    <div className="p-6 max-w-6xl">
      <h1 className="display mb-1">Users</h1>
      <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">Accounts with access to the portal</p>

      <div className="panel mb-4 flex flex-wrap items-end gap-2 p-3">
        <div>
          <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Username</label>
          <input className="input w-44" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="e.g. sokha" />
        </div>
        <div>
          <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Password (8+)</label>
          <input className="input w-44" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <div>
          <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Role</label>
          <select className="input w-28" value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="viewer">viewer</option><option value="editor">editor</option><option value="admin">admin</option>
          </select>
        </div>
        <div>
          <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Organization</label>
          <select className="input w-40" value={orgId ?? ""} onChange={(e) => setOrgId(e.target.value ? Number(e.target.value) : null)}>
            <option value="">(none)</option>
            {(orgs ?? []).map((o) => <option key={o.id} value={o.id}>{o.name}</option>)}
          </select>
        </div>
        <button type="button" className="btn-primary px-4 py-1.5 text-xs"
          disabled={!username.trim() || password.length < 8 || create.isPending}
          onClick={() => create.mutate()}>
          + Add user
        </button>
      </div>

      <div className="panel overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-slate-200 bg-slate-50/60 dark:bg-white/5">
            <tr><th className="th">Username</th><th className="th">Role</th><th className="th">Organization</th><th className="th w-64">Actions</th></tr>
          </thead>
          <tbody>
            {isLoading && <tr><td className="td text-slate-500" colSpan={4}>Loading…</td></tr>}
            {!isLoading && (users ?? []).length === 0 && <tr><td className="td text-slate-500" colSpan={4}>No users yet.</td></tr>}
            {!isLoading && (users ?? []).map((u) => (
              <tr key={u.id} className="border-b border-slate-100 last:border-0 hover:bg-slate-50/60 dark:border-white/5 dark:hover:bg-white/5">
                <td className="td font-medium text-slate-900 dark:text-slate-100">
                  {u.username}{u.username === me?.username && <span className="ml-1.5 text-xs text-slate-400">(you)</span>}
                </td>
                <td className="td">
                  <select
                    className={`badge cursor-pointer ${ROLE_BADGE[u.role] ?? ROLE_BADGE.viewer}`}
                    value={u.role}
                    disabled={u.username === me?.username}
                    onChange={(e) => update.mutate({ id: u.id, patch: { role: e.target.value } })}
                  >
                    <option value="viewer">viewer</option><option value="editor">editor</option><option value="admin">admin</option>
                  </select>
                </td>
                <td className="td">
                  <select className="input w-40 py-1 text-xs" value={u.organization_id ?? ""}
                    onChange={(e) => update.mutate({ id: u.id, patch: { organization_id: e.target.value ? Number(e.target.value) : null } })}>
                    <option value="">(none)</option>
                    {(orgs ?? []).map((o) => <option key={o.id} value={o.id}>{o.name}</option>)}
                  </select>
                </td>
                <td className="td py-1.5">
                  <button type="button" className="rounded-md px-2 py-1 text-xs text-red-500 hover:bg-red-50"
                    disabled={u.username === me?.username}
                    onClick={() => { if (confirm(`Delete user "${u.username}"?`)) remove.mutate(u.id); }}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
