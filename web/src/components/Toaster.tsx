import { useSyncExternalStore } from "react";
import { dismissToast, getToasts, subscribeToasts } from "../lib/toast";

/** Fixed toast stack — mounted once in App.tsx. */
export function Toaster() {
  const items = useSyncExternalStore(subscribeToasts, getToasts, getToasts);
  if (items.length === 0) return null;
  return (
    <div className="pointer-events-none fixed inset-x-0 bottom-6 z-[100] flex flex-col items-center gap-2 px-4">
      {items.map((t) => (
        <div
          key={t.id}
          onClick={() => dismissToast(t.id)}
          className={`toast-in pointer-events-auto flex items-center gap-2.5 rounded-xl px-4 py-2.5 text-sm font-medium shadow-lg ring-1 transition-colors ${
            t.variant === "success"
              ? "bg-emerald-50 text-emerald-800 ring-emerald-200"
              : t.variant === "error"
                ? "bg-rose-50 text-rose-800 ring-rose-200"
                : "bg-slate-900 text-white ring-slate-700"
          }`}
        >
          <span>{t.variant === "success" ? "✓" : t.variant === "error" ? "✕" : "ℹ"}</span>
          <span>{t.message}</span>
        </div>
      ))}
    </div>
  );
}
