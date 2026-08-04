import { useQuery } from "@tanstack/react-query";
import StatCard from "../components/StatCard";
import { api } from "../api/client";

const STATUS_COLORS: Record<string, string> = {
  raw: "bg-slate-500",
  edited: "bg-amber-500",
  verified: "bg-emerald-500",
};

export default function Dashboard() {
  const { data: stats, isLoading } = useQuery({ queryKey: ["stats"], queryFn: api.stats });

  if (isLoading || !stats) {
    return <div className="p-8 text-slate-400">Loading…</div>;
  }

  const maxType = Math.max(1, ...Object.values(stats.by_type));
  const perDay = stats.per_day.slice(0, 14).reverse();

  return (
    <div className="p-6 max-w-6xl">
      <h1 className="text-xl font-semibold text-slate-100 mb-5">Dashboard</h1>

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
        <div className="card p-4">
          <div className="text-sm font-medium text-slate-200 mb-3">By status</div>
          <div className="space-y-2">
            {["raw", "edited", "verified"].map((s) => {
              const count = stats.by_status[s] ?? 0;
              const pct = stats.total ? (count / stats.total) * 100 : 0;
              return (
                <div key={s} className="flex items-center gap-3">
                  <span className="w-16 text-xs text-slate-400 capitalize">{s}</span>
                  <div className="flex-1 h-2.5 bg-base-900 rounded overflow-hidden">
                    <div className={`h-full rounded ${STATUS_COLORS[s] ?? "bg-slate-500"}`} style={{ width: `${pct}%` }} />
                  </div>
                  <span className="w-10 text-right text-xs text-slate-300">{count}</span>
                </div>
              );
            })}
          </div>
        </div>

        <div className="card p-4">
          <div className="text-sm font-medium text-slate-200 mb-3">By type</div>
          <div className="space-y-2">
            {Object.entries(stats.by_type)
              .sort((a, b) => b[1] - a[1])
              .map(([t, count]) => (
                <div key={t} className="flex items-center gap-3">
                  <span className="w-40 truncate text-xs text-slate-400">{t}</span>
                  <div className="flex-1 h-2.5 bg-base-900 rounded overflow-hidden">
                    <div className="h-full rounded bg-accent" style={{ width: `${(count / maxType) * 100}%` }} />
                  </div>
                  <span className="w-10 text-right text-xs text-slate-300">{count}</span>
                </div>
              ))}
            {Object.keys(stats.by_type).length === 0 && <div className="text-xs text-slate-500">No records yet</div>}
          </div>
        </div>

        <div className="card p-4 md:col-span-2">
          <div className="text-sm font-medium text-slate-200 mb-3">Last 14 days</div>
          <div className="flex items-end gap-2 h-28">
            {perDay.map((day) => {
              const [date, count] = Object.entries(day)[0];
              const h = stats.total ? Math.max(3, (count / stats.total) * 100) : 0;
              return (
                <div key={date} className="flex-1 flex flex-col items-center gap-1" title={`${date}: ${count}`}>
                  <div className="w-full rounded-t bg-accent/70" style={{ height: `${h}%` }} />
                  <div className="text-[10px] text-slate-500">{date.slice(5)}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
