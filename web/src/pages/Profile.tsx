import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { api, getUser } from "../api/client";

/** My profile â€” change password + account info. */
export default function Profile() {
  const me = getUser();
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [done, setDone] = useState(false);

  const change = useMutation({
    mutationFn: () => api.changePassword({ current_password: current, new_password: next }),
    onSuccess: () => { setCurrent(""); setNext(""); setDone(true); setTimeout(() => setDone(false), 3000); },
    onError: (err: Error) => window.alert(err.message),
  });

  return (
    <div className="p-6 max-w-2xl">
      <h1 className="display mb-1">My profile</h1>
      <p className="mb-5 text-sm text-slate-600 dark:text-slate-400">Your account and session</p>

      <div className="panel p-5">
        <div className="mb-4 grid grid-cols-2 gap-4 text-sm">
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-wide text-slate-500">Username</div>
            <div className="mt-0.5 font-medium text-slate-900 dark:text-slate-100">{me?.username ?? "â€”"}</div>
          </div>
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-wide text-slate-500">Role</div>
            <div className="mt-0.5"><span className="badge border-accent/30 bg-accent/10 text-accent">{me?.role ?? "â€”"}</span></div>
          </div>
        </div>

        <div className="border-t border-slate-200 pt-4 dark:border-white/10">
          <div className="mb-3 text-sm font-semibold text-slate-900 dark:text-slate-100">Change password</div>
          <div className="space-y-2">
            <div>
              <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Current password</label>
              <input className="input w-full" type="password" value={current} onChange={(e) => setCurrent(e.target.value)} />
            </div>
            <div>
              <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">New password (8+)</label>
              <input className="input w-full" type="password" value={next} onChange={(e) => setNext(e.target.value)} />
            </div>
            <button type="button" className="btn-primary px-4 py-1.5 text-xs"
              disabled={!current || next.length < 8 || change.isPending}
              onClick={() => change.mutate()}>
              {change.isPending ? "Savingâ€¦" : "Update password"}
            </button>
            {done && <span className="ml-2 text-xs font-medium text-emerald-600">Password updated.</span>}
          </div>
        </div>
      </div>
    </div>
  );
}
