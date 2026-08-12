import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, getUser } from "../api/client";
import { toast } from "../lib/toast";

/** Settings — portal configuration key/value store (admin). */
export default function Settings() {
  const qc = useQueryClient();
  const me = getUser();
  const isAdmin = me?.role === "admin";
  const [key, setKey] = useState("");
  const [value, setValue] = useState("{}");
  const [error, setError] = useState<string | null>(null);

  const { data: settings, isLoading } = useQuery({ queryKey: ["settings"], queryFn: api.listSettings, enabled: isAdmin });
  const invalidate = () => qc.invalidateQueries({ queryKey: ["settings"] });

  const save = useMutation({
    mutationFn: () => {
      let parsed: Record<string, unknown>;
      try {
        parsed = JSON.parse(value);
      } catch {
        throw new Error("Value must be valid JSON");
      }
      return api.upsertSetting(key, parsed);
    },
    onSuccess: () => { setKey(""); setValue("{}"); setError(null); invalidate(); },
    onError: (err: Error) => { setError(err.message); toast.error(err.message); },
  });
  const remove = useMutation({ mutationFn: (k: string) => api.deleteSetting(k), onSuccess: invalidate });

  if (!isAdmin) {
    return <div className="p-6 text-sm text-slate-500">Admin role required to manage settings.</div>;
  }

  return (
    <div className="p-6 max-w-4xl">
      <h1 className="display mb-1">Settings</h1>
      <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">Portal configuration (key → JSON value)</p>

      <div className="panel mb-4 flex flex-wrap items-end gap-2 p-3">
        <div>
          <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Key</label>
          <input className="input w-48" value={key} onChange={(e) => setKey(e.target.value)} placeholder="e.g. portal.name" />
        </div>
        <div className="flex-1">
          <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Value (JSON)</label>
          <input className="input w-full font-mono text-xs" value={value} onChange={(e) => setValue(e.target.value)} placeholder='{"en": "Romdoul Data Sharing"}' />
        </div>
        <button type="button" className="btn-primary px-4 py-1.5 text-xs"
          disabled={!key.trim() || save.isPending}
          onClick={() => save.mutate()}>
          Save setting
        </button>
        {error && <span className="text-xs text-red-500">{error}</span>}
      </div>

      <div className="panel overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-slate-200 bg-slate-50/60 dark:bg-white/5">
            <tr><th className="th">Key</th><th className="th">Value</th><th className="th w-28">Updated</th><th className="th w-20"></th></tr>
          </thead>
          <tbody>
            {isLoading && <tr><td className="td text-slate-500" colSpan={4}>Loading…</td></tr>}
            {!isLoading && (settings ?? []).length === 0 && <tr><td className="td text-slate-500" colSpan={4}>No settings yet.</td></tr>}
            {!isLoading && (settings ?? []).map((s) => (
              <tr key={s.key} className="border-b border-slate-100 last:border-0 hover:bg-slate-50/60 dark:border-white/5 dark:hover:bg-white/5">
                <td className="td font-mono text-xs font-medium text-slate-900 dark:text-slate-100">{s.key}</td>
                <td className="td max-w-md truncate font-mono text-xs text-slate-500" title={JSON.stringify(s.value)}>{JSON.stringify(s.value)}</td>
                <td className="td text-xs text-slate-500">{s.updated_at.slice(0, 10)}</td>
                <td className="td py-1.5">
                  <button type="button" className="rounded-md px-2 py-1 text-xs text-red-500 hover:bg-red-50"
                    onClick={() => { if (confirm(`Delete setting "${s.key}"?`)) remove.mutate(s.key); }}>
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
