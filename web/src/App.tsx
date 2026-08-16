import { useEffect, useState, type ReactNode } from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import Dashboard from "./pages/Dashboard";
import Records from "./pages/Records";
import RecordDetail from "./pages/RecordDetail";
import VerifyQueue from "./pages/VerifyQueue";
import Datasets from "./pages/Datasets";
import Categories from "./pages/Categories";
import Collections from "./pages/Collections";
import Organizations from "./pages/Organizations";
import Users from "./pages/Users";
import AuditLogs from "./pages/AuditLogs";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";
import Explore from "./pages/Explore";
import DocsPage from "./pages/DocsPage";
import LoginScreen from "./components/LoginScreen";
import { Toaster } from "./components/Toaster";
import { api, getToken, getUser, setSession } from "./api/client";
import { useTheme } from "./hooks/useTheme";

// --------------------------------------------------------------------------- //
// Icons — one distinct glyph per nav item
// --------------------------------------------------------------------------- //
function Icon({ children, className = "h-4.5 w-4.5" }: { children: ReactNode; className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      {children}
    </svg>
  );
}
const I = {
  dashboard: <Icon><rect x="3" y="3" width="7" height="9" rx="1.5" /><rect x="14" y="3" width="7" height="5" rx="1.5" /><rect x="14" y="12" width="7" height="9" rx="1.5" /><rect x="3" y="16" width="7" height="5" rx="1.5" /></Icon>,
  explore: <Icon><circle cx="12" cy="12" r="9" /><path d="m15.5 8.5-2 5-5 2 2-5z" /></Icon>,
  records: <Icon><ellipse cx="12" cy="5" rx="8" ry="3" /><path d="M4 5v14a8 3 0 0 0 16 0V5" /><path d="M4 12a8 3 0 0 0 16 0" /></Icon>,
  verify: <Icon><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z" /><path d="m8.5 12 2.5 2.5 4.5-5" /></Icon>,
  datasets: <Icon><path d="m12 2 9 5-9 5-9-5z" /><path d="m3 12 9 5 9-5" /><path d="m3 17 9 5 9-5" /></Icon>,
  categories: <Icon><path d="M20.6 13.4 12 22l-8.6-8.6A2 2 0 0 1 3 12V4a1 1 0 0 1 1-1h8a2 2 0 0 1 1.4.6z" /><circle cx="7.5" cy="7.5" r="1.2" /></Icon>,
  collections: <Icon><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" /><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" /></Icon>,
  organizations: <Icon><rect x="4" y="3" width="16" height="18" rx="1.5" /><path d="M9 8h6M9 12h6M9 16h3" /><path d="M12 21v-5" /></Icon>,
  users: <Icon><circle cx="9" cy="8" r="3.5" /><path d="M2.5 20a6.5 6.5 0 0 1 13 0" /><path d="M16 4.8a3.5 3.5 0 0 1 0 6.4M21.5 20a6.5 6.5 0 0 0-4.2-6" /></Icon>,
  audit: <Icon><path d="M3 12a9 9 0 1 0 3-6.7L3 8" /><path d="M3 3v5h5" /><path d="M12 7v5l3 2" /></Icon>,
  settings: <Icon><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.9 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.9.3h.1a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5h.1a1.7 1.7 0 0 0 1.9-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.9v.1a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z" /></Icon>,
  profile: <Icon><circle cx="12" cy="8" r="4" /><path d="M4 21c0-4 3.6-6.5 8-6.5s8 2.5 8 6.5" /></Icon>,
  docs: <Icon><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" /><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" /><path d="M9 7h6M9 11h6" /></Icon>,
};

// --------------------------------------------------------------------------- //
// Nav model — grouped sections, distinct icon + optional live badge per item
// --------------------------------------------------------------------------- //
interface NavItem {
  to: string;
  label: string;
  end?: boolean;
  icon: ReactNode;
  badge?: (count: number) => ReactNode | null;
}

const NAV_SECTIONS: { label: string; items: NavItem[] }[] = [
  {
    label: "Overview",
    items: [
      { to: "/", label: "Dashboard", end: true, icon: I.dashboard },
      { to: "/explore", label: "Explore", icon: I.explore },
    ],
  },
  {
    label: "Data",
    items: [
      { to: "/records", label: "Data management", icon: I.records },
      {
        to: "/verify",
        label: "Verify queue",
        icon: I.verify,
        badge: (raw) => (raw > 0 ? <span className="nav-badge">{raw}</span> : null),
      },
      { to: "/datasets", label: "Datasets", icon: I.datasets },
    ],
  },
  {
    label: "Taxonomy",
    items: [
      { to: "/categories", label: "Categories", icon: I.categories },
      { to: "/collections", label: "Collections", icon: I.collections },
      { to: "/organizations", label: "Organizations", icon: I.organizations },
    ],
  },
  {
    label: "Admin",
    items: [
      { to: "/users", label: "Users", icon: I.users },
      { to: "/audit", label: "Audit logs", icon: I.audit },
      { to: "/settings", label: "Settings", icon: I.settings },
    ],
  },
  {
    label: "Account",
    items: [
      { to: "/profile", label: "My profile", icon: I.profile },
      { to: "/docs", label: "API Docs", icon: I.docs },
    ],
  },
];

function SunIcon({ className }: { className?: string }) {
  return (
    <Icon className={className}><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" /></Icon>
  );
}

function MoonIcon({ className }: { className?: string }) {
  return (
    <Icon className={className}><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></Icon>
  );
}

function BrandMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M3 5v14a9 3 0 0 0 18 0V5" />
      <path d="M3 12a9 3 0 0 0 18 0" />
      <path d="M8 9v6M12 9v6M16 9v6" />
    </svg>
  );
}

function NavContent({ rawPending, onNavigate }: { rawPending: number; onNavigate?: () => void }) {
  return (
    <nav className="flex-1 space-y-4 overflow-y-auto px-2 py-2" aria-label="Primary">
      {NAV_SECTIONS.map((section) => (
        <div key={section.label}>
          <div className="mb-1 px-2.5 text-[10px] font-semibold uppercase tracking-[0.14em] text-slate-400">
            {section.label}
          </div>
          <div className="space-y-0.5">
            {section.items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                onClick={onNavigate}
                className={({ isActive }) =>
                  `nav-item w-full ${isActive ? "nav-item-active" : ""}`
                }
              >
                <span className="nav-icon shrink-0">{item.icon}</span>
                <span className="truncate">{item.label}</span>
                {item.badge?.(rawPending)}
              </NavLink>
            ))}
          </div>
        </div>
      ))}
    </nav>
  );
}

export default function App() {
  const [authed, setAuthed] = useState<boolean>(() => getToken() !== null);
  const [user, setUser] = useState(getUser());
  const [navOpen, setNavOpen] = useState(false);
  const { theme, toggle: toggleTheme } = useTheme();

  // Live "awaiting review" count for the Verify queue badge.
  const { data: stats } = useQuery({
    queryKey: ["stats"],
    queryFn: api.stats,
    refetchInterval: 60_000,
    enabled: authed,
  });
  const rawPending = (stats?.by_status?.raw ?? 0) as number;

  useEffect(() => {
    const onAuthRequired = () => setAuthed(false);
    window.addEventListener("auth:required", onAuthRequired);
    return () => window.removeEventListener("auth:required", onAuthRequired);
  }, []);

  const signOut = async () => {
    try {
      await api.logout();
    } catch {
      /* session may already be invalid */
    }
    setSession(null);
    setAuthed(false);
  };

  if (!authed) {
    return (
      <div className="relative min-h-screen">
        <div className="cyber-grid" aria-hidden="true" />
        <div className="cyber-scan" aria-hidden="true" />
        <div className="absolute right-4 top-4 z-10">
          <button type="button" onClick={toggleTheme} className="btn-secondary px-3 py-2" title="Toggle theme" aria-label="Toggle theme">
            {theme === "dark" ? <SunIcon className="h-4 w-4" /> : <MoonIcon className="h-4 w-4" />}
          </button>
        </div>
        <LoginScreen
          onSuccess={() => {
            setUser(getUser());
            setAuthed(true);
          }}
        />
      </div>
    );
  }

  return (
    <div className="relative flex min-h-screen">
      <div className="cyber-grid" aria-hidden="true" />
      <div className="cyber-scan" aria-hidden="true" />

      <aside className="sticky top-0 z-10 hidden h-screen w-64 shrink-0 flex-col border-r border-slate-200 bg-white/70 backdrop-blur-md sm:flex">
        <div className="flex items-center gap-2.5 px-3 py-4">
          <div className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-accent/10 text-accent ring-1 ring-accent/40 dark:drop-shadow-[0_0_10px_rgba(0,229,255,0.6)]">
            <BrandMark className="h-7 w-7" />
          </div>
          <div className="min-w-0">
            <h1 className="truncate text-sm font-semibold leading-tight tracking-tight text-slate-950">
              Romdoul <span className="text-accent dark:drop-shadow-[0_0_8px_rgba(0,229,255,0.7)]">Data Sharing</span>
            </h1>
            <p className="truncate text-[11px] uppercase tracking-wider text-slate-500">OCR → datasets → publish</p>
          </div>
        </div>
        <div className="temple-ridge mx-3 mb-2 h-px bg-gradient-to-r from-transparent via-accent/40 to-transparent" />

        <NavContent rawPending={rawPending} />

        <div className="space-y-2 border-t border-slate-200 px-3 py-3">
          <div className="flex items-center gap-2">
            <button type="button" onClick={toggleTheme} className="btn-secondary px-3 py-2" title="Toggle theme" aria-label="Toggle theme">
              {theme === "dark" ? <SunIcon className="h-4 w-4" /> : <MoonIcon className="h-4 w-4" />}
            </button>
            <button type="button" onClick={signOut} className="btn-ghost ml-auto" title="Sign out">
              Sign out
            </button>
          </div>
          <p className="px-1 text-[11px] text-slate-400">
            Signed in as <span className="font-medium text-slate-600 dark:text-slate-300">{user?.username ?? "—"}</span>
            {user?.role && <span className="badge ml-1.5 border-accent/30 bg-accent/10 text-accent">{user.role}</span>}
          </p>
        </div>
      </aside>

      <main className="relative z-10 min-w-0 flex-1">
        {/* Mobile top bar — nav lives in a drawer below sm */}
        <div className="sticky top-0 z-20 flex items-center gap-2 border-b border-slate-200 bg-white/80 px-3 py-2 backdrop-blur-md sm:hidden">
          <button
            type="button"
            onClick={() => setNavOpen(true)}
            className="btn-secondary px-2.5 py-2"
            aria-label="Open navigation"
            aria-expanded={navOpen}
          >
            <Icon><path d="M3 6h18M3 12h18M3 18h18" /></Icon>
          </button>
          <h1 className="truncate text-sm font-semibold tracking-tight text-slate-950 dark:text-slate-100">
            Romdoul <span className="text-accent">Data Sharing</span>
          </h1>
          <button type="button" onClick={toggleTheme} className="btn-secondary ml-auto px-2.5 py-2" aria-label="Toggle theme">
            {theme === "dark" ? <SunIcon className="h-4 w-4" /> : <MoonIcon className="h-4 w-4" />}
          </button>
        </div>

        {/* Mobile drawer */}
        {navOpen && (
          <div className="fixed inset-0 z-30 sm:hidden" role="dialog" aria-modal="true" aria-label="Navigation">
            <button
              type="button"
              className="absolute inset-0 bg-slate-950/50 backdrop-blur-sm"
              onClick={() => setNavOpen(false)}
              aria-label="Close navigation"
            />
            <aside className="relative flex h-full w-72 max-w-[85%] flex-col border-r border-slate-200 bg-white/95 backdrop-blur-md dark:bg-slate-900/95">
              <div className="flex items-center justify-between px-3 py-4">
                <span className="text-sm font-semibold tracking-tight text-slate-950 dark:text-slate-100">Menu</span>
                <button type="button" onClick={() => setNavOpen(false)} className="btn-ghost px-2 py-1" aria-label="Close navigation">
                  <Icon><path d="M18 6 6 18M6 6l12 12" /></Icon>
                </button>
              </div>
              <NavContent rawPending={rawPending} onNavigate={() => setNavOpen(false)} />
              <div className="space-y-2 border-t border-slate-200 px-3 py-3">
                <button type="button" onClick={signOut} className="btn-ghost w-full justify-center py-2" title="Sign out">
                  Sign out
                </button>
                <p className="px-1 text-[11px] text-slate-400">
                  Signed in as <span className="font-medium text-slate-600 dark:text-slate-300">{user?.username ?? "—"}</span>
                  {user?.role && <span className="badge ml-1.5 border-accent/30 bg-accent/10 text-accent">{user.role}</span>}
                </p>
              </div>
            </aside>
          </div>
        )}

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/explore" element={<Explore />} />
          <Route path="/records" element={<Records />} />
          <Route path="/records/:id" element={<RecordDetail />} />
          <Route path="/verify" element={<VerifyQueue />} />
          <Route path="/datasets" element={<Datasets />} />
          <Route path="/categories" element={<Categories />} />
          <Route path="/collections" element={<Collections />} />
          <Route path="/organizations" element={<Organizations />} />
          <Route path="/users" element={<Users />} />
          <Route path="/audit" element={<AuditLogs />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/docs" element={<DocsPage />} />
        </Routes>
      </main>
      <Toaster />
    </div>
  );
}
