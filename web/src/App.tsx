import { useEffect, useState } from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Records from "./pages/Records";
import RecordDetail from "./pages/RecordDetail";
import DocsPage from "./pages/DocsPage";
import LoginScreen from "./components/LoginScreen";
import { getToken, setToken } from "./api/client";

const nav = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/records", label: "Records", end: false },
  { to: "/docs", label: "API Docs", end: false },
];

export default function App() {
  const [authed, setAuthed] = useState<boolean>(() => getToken() !== null);

  useEffect(() => {
    const onAuthRequired = () => setAuthed(false);
    window.addEventListener("auth:required", onAuthRequired);
    return () => window.removeEventListener("auth:required", onAuthRequired);
  }, []);

  if (!authed) {
    return (
      <LoginScreen
        onSuccess={() => {
          setAuthed(true);
          window.location.hash = "#/";
        }}
      />
    );
  }

  return (
    <div className="flex h-screen">
      <aside className="w-56 shrink-0 border-r border-base-600/60 bg-base-850 flex flex-col">
        <div className="px-4 py-4 border-b border-base-600/60">
          <div className="text-accent font-bold tracking-tight">Metadata Portal</div>
          <div className="text-[11px] text-slate-500 mt-0.5">v1 · extracted records</div>
        </div>
        <nav className="flex-1 px-2 py-3 space-y-1">
          {nav.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              end={n.end}
              className={({ isActive }) =>
                `block px-3 py-2 rounded-md text-sm transition-colors ${
                  isActive ? "bg-accent/10 text-accent" : "text-slate-400 hover:bg-base-700 hover:text-slate-200"
                }`
              }
            >
              {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="px-4 py-3 space-y-2 text-[11px] text-slate-500 border-t border-base-600/60">
          <div>API base: <code className="text-slate-400">/api/v1</code></div>
          <button className="text-slate-400 hover:text-slate-200 underline" onClick={() => { setToken(null); setAuthed(false); }}>
            Sign out
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/records" element={<Records />} />
          <Route path="/records/:id" element={<RecordDetail />} />
          <Route path="/docs" element={<DocsPage />} />
        </Routes>
      </main>
    </div>
  );
}
