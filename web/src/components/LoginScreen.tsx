import { useState } from "react";
import { api, setToken } from "../api/client";

export default function LoginScreen({ onSuccess }: { onSuccess: () => void }) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const res = await api.login(password);
      setToken(res.token);
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-base-900">
      <form onSubmit={submit} className="card w-80 p-6 space-y-4">
        <div>
          <div className="text-accent font-bold text-lg">Metadata Portal</div>
          <div className="text-xs text-slate-500">Sign in to view extraction records</div>
        </div>
        <div>
          <label className="label">Password</label>
          <input
            className="input w-full"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoFocus
            placeholder="team password"
          />
        </div>
        {error && <div className="text-xs text-red-400">{error}</div>}
        <button className="btn-primary w-full justify-center" type="submit" disabled={busy || !password}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}
