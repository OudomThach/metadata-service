import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import StatCard from "../components/StatCard";
import { api, getUser } from "../api/client";

const STATUS_COLORS: Record<string, string> = {
  raw: "bg-slate-400",
  edited: "bg-accent2",
  verified: "bg-accent",
};

export default function Dashboard() {
  const { data: stats, isLoading } = useQuery({ queryKey: ["stats"], queryFn: api.stats });

  if (isLoading || !stats) {
    return <div className="p-8 text-slate-500">Loading…</div>;
  }

  const maxType = Math.max(1, ...Object.values(stats.by_type));
  const perDay = stats.per_day.slice(0, 14).reverse();

  return (
    <div className="p-6 max-w-6xl">
      <h1 className="display mb-1">Dashboard</h1>
      <p className="mb-5 text-sm text-slate-600 dark:text-slate-400">Extraction records across every backend</p>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <StatCard label="Total records" value={stats.total} />
        <StatCard label="Edited" value={stats.edited} sub="at least one edit" />
        <StatCard label="Verified" value={stats.verified} />
        <StatCard
          label="Coverage avg"
          value={stats.coverage_avg === null ? "—" : `${(stats.coverage_avg * 100).toFixed(0)}%`}
          sub="non-null fields / total"
        />
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="panel p-5">
          <div className="mb-3 flex items-center justify-between">
            <span className="text-sm font-semibold text-slate-950 dark:text-slate-100">By status</span>
            {(stats.by_status.raw ?? 0) > 0 && (
              <Link to="/verify" className="text-xs font-medium text-accent hover:underline">
                Open verify queue ({(stats.by_status.raw ?? 0)} awaiting review) →
              </Link>
            )}
          </div>
          <div className="space-y-2.5">
            {["raw", "edited", "verified"].map((s) => {
              const count = stats.by_status[s] ?? 0;
              const pct = stats.total ? (count / stats.total) * 100 : 0;
              return (
                <div key={s} className="flex items-center gap-3">
                  <span className="w-16 text-xs font-medium text-slate-500 capitalize">{s}</span>
                  <div className="flex-1 h-2.5 rounded-full bg-slate-100 dark:bg-white/10 overflow-hidden">
                    <div
                      className={`h-full rounded-full ${STATUS_COLORS[s] ?? "bg-slate-400"}`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                  <span className="w-10 text-right text-xs font-medium text-slate-600 dark:text-slate-300">{count}</span>
                </div>
              );
            })}
          </div>
        </div>

        <div className="panel p-5">
          <div className="mb-3 text-sm font-semibold text-slate-950 dark:text-slate-100">By type</div>
          <div className="space-y-2.5">
            {Object.entries(stats.by_type)
              .sort((a, b) => b[1] - a[1])
              .map(([t, count]) => (
                <div key={t} className="flex items-center gap-3">
                  <span className="w-40 truncate text-xs font-medium text-slate-500">{t}</span>
                  <div className="flex-1 h-2.5 rounded-full bg-slate-100 dark:bg-white/10 overflow-hidden">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-accent to-accent2"
                      style={{ width: `${(count / maxType) * 100}%` }}
                    />
                  </div>
                  <span className="w-10 text-right text-xs font-medium text-slate-600 dark:text-slate-300">{count}</span>
                </div>
              ))}
            {Object.keys(stats.by_type).length === 0 && <div className="text-xs text-slate-500">No records yet</div>}
          </div>
        </div>

        <div className="panel p-5">
          <div className="mb-3 text-sm font-semibold text-slate-950 dark:text-slate-100">By model</div>
          <div className="flex flex-wrap gap-4">
            {Object.entries(stats.by_model ?? {}).map(([m, count]) => (
              <div key={m} className="flex items-center gap-2">
                <span className={`h-3 w-3 rounded-full ${m === 'default' ? 'bg-accent' : m === 'vllm' ? 'bg-accent2' : 'bg-emerald-500'}`} />
                <span className="text-sm text-slate-700 dark:text-slate-200">{m}</span>
                <span className="text-sm font-semibold text-slate-950 dark:text-slate-100">{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel p-5 md:col-span-2">
          <div className="mb-3 text-sm font-semibold text-slate-950 dark:text-slate-100">Last 14 days</div>
          <div className="flex items-end gap-2 h-28">
            {perDay.map((day) => {
              const [date, count] = Object.entries(day)[0];
              const h = stats.total ? Math.max(3, (count / stats.total) * 100) : 0;
              return (
                <div key={date} className="flex-1 flex flex-col items-center gap-1" title={`${date}: ${count}`}>
                  <div
                    className="w-full rounded-t-lg bg-gradient-to-t from-accent/60 to-accent2/80"
                    style={{ height: `${h}%` }}
                  />
                  <div className="text-[10px] text-slate-500">{date.slice(5)}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <RecentActivity />
    </div>
  );
}

/** Last ~10 audit events — "who did what" at a glance (admin). */
function RecentActivity() {
  const me = getUser();
  if (me?.role !== "admin") return null;
  const { data: events } = useQuery({
    queryKey: ["audit", "recent"],
    queryFn: () => api.listAudit({ limit: 10 }),
    refetchInterval: 60_000,
  });
  if (!events || events.length === 0) return null;

  const TONE: Record<string, string> = {
    create: "border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
    delete: "border-red-500/30 bg-red-500/10 text-red-500",
    update: "border-accent2/30 bg-accent2/10 text-accent2",
    publish: "border-accent/30 bg-accent/10 text-accent",
    unpublish: "border-amber-500/30 bg-amber-500/10 text-amber-600",
  };

  return (
    <div className="panel mt-6 p-5">
      <div className="mb-3 flex items-center justify-between">
        <span className="text-sm font-semibold text-slate-950 dark:text-slate-100">Recent activity</span>
        <Link to="/audit" className="text-xs font-medium text-accent hover:underline">View all →</Link>
      </div>
      <div className="space-y-1.5">
        {events.map((e) => (
          <div key={e.id} className="flex flex-wrap items-center gap-2 text-sm">
            <span className={`badge ${TONE[e.action] ?? TONE.update}`}>{e.action}</span>
            <span className="font-mono text-xs text-slate-600 dark:text-slate-300">{e.actor}</span>
            <span className="text-xs text-slate-400">
              {e.entity_type}{e.entity_id ? ` · ${e.entity_id.slice(0, 10)}` : ""}
              {(e.detail as { name?: string } | null)?.name ? ` · ${(e.detail as { name?: string }).name}` : ""}
            </span>
            <span className="ml-auto text-xs text-slate-400">{e.at.slice(0, 19).replace("T", " ")}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
