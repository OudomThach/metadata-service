// Minimal toast store (no deps) — portal counterpart of the SPA's toasts.

export interface ToastItem {
  id: number;
  message: string;
  variant: "success" | "error" | "info";
}

type Listener = () => void;

let items: ToastItem[] = [];
const listeners = new Set<Listener>();
let nextId = 1;

function emit(): void {
  listeners.forEach((l) => l());
}

export function subscribeToasts(cb: Listener): () => void {
  listeners.add(cb);
  return () => {
    listeners.delete(cb);
  };
}

export function getToasts(): ToastItem[] {
  return items;
}

export function dismissToast(id: number): void {
  items = items.filter((t) => t.id !== id);
  emit();
}

export function pushToast(message: string, variant: ToastItem["variant"] = "info"): void {
  const id = nextId++;
  items = [...items, { id, message, variant }];
  emit();
  window.setTimeout(() => dismissToast(id), variant === "error" ? 5000 : 3200);
}

export const toast = {
  success: (m: string) => pushToast(m, "success"),
  error: (m: string) => pushToast(m, "error"),
  info: (m: string) => pushToast(m, "info"),
};
