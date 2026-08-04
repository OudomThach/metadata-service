const styles: Record<string, string> = {
  raw: "bg-slate-500/15 text-slate-300 border-slate-500/40",
  edited: "bg-amber-500/15 text-amber-300 border-amber-500/40",
  verified: "bg-emerald-500/15 text-emerald-300 border-emerald-500/40",
};

export default function StatusBadge({ status }: { status: string }) {
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium border ${styles[status] ?? styles.raw}`}>
      {status}
    </span>
  );
}
