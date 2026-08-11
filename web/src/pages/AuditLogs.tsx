import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api, getUser } from "../api/client";

/** Audit logs — global "who did what, when" across all entities. */
export default function AuditLogs() {
  const me = getUser();
  const isAdmin = me?.role === "admin";
  const [entityType, setEntityType] = useState("");
  const [action, setAction] = useState("");
  const [actorName, setActorName] = useState("");

  const { data: events, isLoading } = useQuery({
    queryKey: ["audit", entityType, action, actorName],
    queryFn: () => api.listAudit({
      entity_type: entityType || undefined,
      action: action || undefined,
      actor_name: actorName || undefined,
      limit: 200,
    }),
    enabled: isAdmin,
  });

  if (!isAdmin) {
    return <div className="p-6 text-sm text-slate-500">Admin role required to view audit logs.</div>;
  }

  const ACTION_TONE: Record<string, string> = {
    create: "border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
    delete: "border-red-500/30 bg-red-500/10 text-red-500",
    update: "border-accent2/30 bg-accent2/10 text-accent2",
    publish: "border-accent/30 bg-accent/10 text-accent",
    unpublish: "border-amber-500/30 bg-amber-500/10 text-amber-600",
    login: "border-slate-300 bg-slate-100 text-slate-600",
  };

  return (
    <div className="p-6 max-w-7xl">
      <h1 className="display mb-1">Audit logs</h1>
      <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">Every action across records, datasets, users and settings</p>

      <div className="panel mb-4 flex flex-wrap gap-2 p-3">
        <select className="input w-40" value={entityType} onChange={(e) => setEntityType(e.target.value)}>
          <option value="">All entities</option>
          {["record", "dataset", "user", "category", "collection", "organization", "setting"].map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
        <select className="input w-36" value={action} onChange={(e) => setAction(e.target.value)}>
          <option value="">All actions</option>
          {["create", "update", "delete", "verify", "publish", "unpublish", "login"].map((a) => (
            <option key={a} value={a}>{a}</option>
          ))}
        </select>
        <input className="input w-48" placeholder="Actor (e.g. admin)" value={actorName} onChange={(e) => setActorName(e.target.value)} />
      </div>

      <div className="panel overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-slate-200 bg-slate-50/60 dark:bg-white/5">
            <tr><th className="th w-32">When</th><th className="th">Actor</th><th className="th w-28">Action</th><th className="th">Entity</th><th className="th">Detail</th></tr>
          </thead>
          <tbody>
            {isLoading && <tr><td className="td text-slate-500" colSpan={5}>Loading…</td></tr>}
            {!isLoading && (events ?? []).length === 0 && <tr><td className="td text-slate-500" colSpan={5}>No events match.</td></tr>}
            {!isLoading && (events ?? []).map((e) => (
              <tr key={e.id} className="border-b border-slate-100 last:border-0 hover:bg-slate-50/60 dark:border-white/5 dark:hover:bg-white/5">
                <td className="td text-slate-500">{e.at.slice(0, 19).replace("T", " ")}</td>
                <td className="td font-mono text-xs text-slate-700 dark:text-slate-300">{e.actor}</td>
                <td className="td"><span className={`badge ${ACTION_TONE[e.action] ?? ACTION_TONE.update}`}>{e.action}</span></td>
                <td className="td text-slate-600 dark:text-slate-300">
                  {e.entity_type}
                  {e.entity_id && <code className="ml-1.5 text-[11px] text-slate-400">{e.entity_id.slice(0, 12)}</code>}
                </td>
                <td className="td max-w-md truncate text-xs text-slate-500" title={JSON.stringify(e.detail)}>
                  {JSON.stringify(e.detail ?? {})}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
