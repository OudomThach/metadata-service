export interface Page<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface RecordOut {
  id: string;
  schema_version: string;
  type: string;
  domain: string | null;
  status: string;
  business_date: string | null;
  tags: string[] | null;
  source: Record<string, unknown> | null;
  audit: Record<string, unknown> | null;
  pipeline: Record<string, unknown> | null;
  record: Record<string, unknown> | null;
  business: Record<string, unknown> | null;
  data: Record<string, unknown>;
  envelope: Record<string, unknown>;
  created_at: string;
  created_by: string;
  edited_at: string | null;
  edited_by: string | null;
  edit_count: number;
  source_model: string | null;
  source_system: string | null;
}

export interface Stats {  total: number;
  by_status: Record<string, number>;
  by_type: Record<string, number>;
  by_domain: Record<string, number>;
  by_model: Record<string, number>;
  edited: number;
  verified: number;
  coverage_avg: number | null;
  per_day: Record<string, number>[];
}

export interface TraceOut {
  record: RecordOut;
  lineage: Record<string, unknown>;
  audit: AuditEventOut[];
  dataset: Record<string, unknown> | null;
}

export interface Meta {
  types: string[];
  domains: string[];
}

// ── Romdoul Data Sharing types ────────────────────────────────────────────
export interface OrganizationOut {
  id: number;
  name: string;
  org_type: string;
  contact: Record<string, unknown> | null;
  created_at: string;
}
export interface OrganizationIn {
  name: string;
  org_type: string;
  contact?: Record<string, unknown> | null;
}

export interface CategoryOut {
  id: number;
  parent_id: number | null;
  name: string;
  description: string | null;
  sort: number;
  created_at: string;
}
export interface CategoryIn {
  parent_id?: number | null;
  name: string;
  description?: string | null;
  sort?: number;
}

export interface CollectionOut {
  id: number;
  name: string;
  description: string | null;
  organization_id: number | null;
  created_at: string;
}
export interface CollectionIn {
  name: string;
  description?: string | null;
  organization_id?: number | null;
}

export interface DatasetOut {
  id: string;
  record_id: string | null;
  name: string;
  description: string | null;
  organization_id: number | null;
  category_id: number | null;
  collection_id: number | null;
  coverage_start: string | null;
  coverage_end: string | null;
  frequency: string | null;
  url: string | null;
  status: string;
  published_at: string | null;
  file_name: string | null;
  file_size: number | null;
  file_type: string | null;
  file_base64: string | null;
  created_at: string;
  updated_at: string | null;
}
export interface DatasetIn {
  id?: string;
  record_id?: string | null;
  name: string;
  description?: string | null;
  organization_id?: number | null;
  category_id?: number | null;
  collection_id?: number | null;
  coverage_start?: string | null;
  coverage_end?: string | null;
  frequency?: string | null;
  url?: string | null;
  file_name?: string | null;
  file_size?: number | null;
  file_type?: string | null;
  file_base64?: string | null;
}
export interface DatasetPage {
  items: DatasetOut[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}
export interface DatasetQuery {
  page?: number;
  page_size?: number;
  status?: string;
  category_id?: number;
  collection_id?: number;
  organization_id?: number;
  q?: string;
  public?: boolean;
}

export interface AuditEventOut {
  id: number;
  actor: string;
  action: string;
  entity_type: string;
  entity_id: string | null;
  detail: Record<string, unknown> | null;
  at: string;
}
export interface AuditQuery {
  entity_type?: string;
  action?: string;
  actor_name?: string;
  limit?: number;
  offset?: number;
}

export interface SettingOut {
  key: string;
  value: Record<string, unknown> | null;
  updated_at: string;
}

export interface UserOut {
  id: number;
  username: string;
  role: string;
  organization_id: number | null;
}

export interface AuditEventOut {
  id: number;
  action: string;
  actor: string;
  at: string;
  snapshot: Record<string, unknown>;
}

export interface QueryParams {
  page?: number;
  page_size?: number;
  type?: string;
  domain?: string;
  status?: string;
  tag?: string;
  business_from?: string;
  business_to?: string;
  created_from?: string;
  created_to?: string;
  q?: string;
  sort?: string;
}

// The portal is served at /portal on the shared Romdoul host, where the API
// lives behind the /api-meta prefix (romdoul nginx → metadata-service). The
// service also accepts /api-meta directly, so this one base works everywhere:
// public netlify, localhost:8181/portal, and direct :8095.
const API = "/api-meta/api/v1";
const TOKEN_KEY = "metadata_token";
const USER_KEY = "metadata_user";

export interface PortalUser {
  username: string;
  role: string;
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function getUser(): PortalUser | null {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? (JSON.parse(raw) as PortalUser) : null;
  } catch {
    return null;
  }
}

export function setSession(token: string | null, user?: PortalUser): void {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
  if (user) localStorage.setItem(USER_KEY, JSON.stringify(user));
  else localStorage.removeItem(USER_KEY);
}

async function http<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = { ...(init?.headers as Record<string, string> | undefined) };
  if (token) headers["X-Session-Token"] = token;
  const res = await fetch(path, { ...init, headers });
  if (res.status === 401 && token) {
    setSession(null);
    window.dispatchEvent(new Event("auth:required"));
  }
  if (!res.ok) {
    let message = `${res.status} ${res.statusText}`;
    try {
      const body = await res.json();
      message = body?.error?.message ?? body?.detail ?? message;
    } catch {
      /* keep default message */
    }
    throw new Error(message);
  }
  return res.status === 204 ? (undefined as T) : res.json();
}

function qs(params: Record<string, string | number | boolean | undefined>): string {
  const parts = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== "")
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`);
  return parts.length ? `?${parts.join("&")}` : "";
}

export const api = {
  login: (username: string, password: string) =>
    http<{ token: string; user: PortalUser }>(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    }),
  logout: () => http<{ ok: boolean }>(`${API}/auth/logout`, { method: "POST" }),
  me: () => http<PortalUser>(`${API}/auth/me`),
  listRecords: (p: QueryParams) =>
    http<Page<RecordOut>>(`${API}/records${qs({ ...p })}`),
  getRecord: (id: string) => http<RecordOut>(`${API}/records/${encodeURIComponent(id)}`),
  recordHistory: (id: string) => http<AuditEventOut[]>(`${API}/records/${encodeURIComponent(id)}/history`),
  recordTrace: (id: string) => http<TraceOut>(`${API}/records/${encodeURIComponent(id)}/trace`),
  patchRecord: (id: string, body: Record<string, unknown>) =>
    http<RecordOut>(`${API}/records/${encodeURIComponent(id)}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  deleteRecord: (id: string) => http<void>(`${API}/records/${encodeURIComponent(id)}`, { method: "DELETE" }),
  stats: () => http<Stats>(`${API}/stats`),
  meta: () => http<Meta>(`${API}/meta`),
  exportUrl: (format: "csv" | "json" | "jsonl" | "parquet", p: QueryParams) =>
    `${API}/export${qs({ format, ...p })}`,
  datasetFileUrl: (id: string) => `${API}/datasets/${encodeURIComponent(id)}/file`,
  // ── Romdoul Data Sharing entities ────────────────────────────────────
  changePassword: (body: { current_password: string; new_password: string }) =>
    http<{ ok: boolean }>(`${API}/auth/me/password`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  listUsers: () => http<UserOut[]>(`${API}/auth/users`),
  createUser: (body: { username: string; password: string; role: string; organization_id?: number | null }) =>
    http<UserOut>(`${API}/auth/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  updateUser: (id: number, body: { role?: string; organization_id?: number | null }) =>
    http<UserOut>(`${API}/auth/users/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  deleteUser: (id: number) => http<void>(`${API}/auth/users/${id}`, { method: "DELETE" }),
  listOrganizations: () => http<OrganizationOut[]>(`${API}/organizations`),
  createOrganization: (body: OrganizationIn) =>
    http<OrganizationOut>(`${API}/organizations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  updateOrganization: (id: number, body: OrganizationIn) =>
    http<OrganizationOut>(`${API}/organizations/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  deleteOrganization: (id: number) => http<void>(`${API}/organizations/${id}`, { method: "DELETE" }),
  listCategories: () => http<CategoryOut[]>(`${API}/categories`),
  createCategory: (body: CategoryIn) =>
    http<CategoryOut>(`${API}/categories`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  updateCategory: (id: number, body: CategoryIn) =>
    http<CategoryOut>(`${API}/categories/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  deleteCategory: (id: number) => http<void>(`${API}/categories/${id}`, { method: "DELETE" }),
  listCollections: () => http<CollectionOut[]>(`${API}/collections`),
  createCollection: (body: CollectionIn) =>
    http<CollectionOut>(`${API}/collections`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  updateCollection: (id: number, body: CollectionIn) =>
    http<CollectionOut>(`${API}/collections/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  deleteCollection: (id: number) => http<void>(`${API}/collections/${id}`, { method: "DELETE" }),
  listDatasets: (p: DatasetQuery = {}) =>
    http<DatasetPage>(`${API}/datasets${qs({ ...p })}`),
  getDataset: (id: string) => http<DatasetOut>(`${API}/datasets/${encodeURIComponent(id)}`),
  createDataset: (body: DatasetIn) =>
    http<DatasetOut>(`${API}/datasets`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  updateDataset: (id: string, body: Partial<DatasetIn>) =>
    http<DatasetOut>(`${API}/datasets/${encodeURIComponent(id)}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  publishDataset: (id: string) => http<DatasetOut>(`${API}/datasets/${encodeURIComponent(id)}/publish`, { method: "POST" }),
  unpublishDataset: (id: string) => http<DatasetOut>(`${API}/datasets/${encodeURIComponent(id)}/unpublish`, { method: "POST" }),
  promoteRecordToDataset: (recordId: string) =>
    http<DatasetOut>(`${API}/datasets/from-record/${encodeURIComponent(recordId)}`, { method: "POST" }),
  deleteDataset: (id: string) => http<void>(`${API}/datasets/${encodeURIComponent(id)}`, { method: "DELETE" }),
  listAudit: (p: AuditQuery = {}) =>
    http<AuditEventOut[]>(`${API}/audit${qs({ ...p })}`),
  listSettings: () => http<SettingOut[]>(`${API}/settings`),
  upsertSetting: (key: string, value: Record<string, unknown>) =>
    http<SettingOut>(`${API}/settings/${encodeURIComponent(key)}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key, value }),
    }),
  deleteSetting: (key: string) => http<void>(`${API}/settings/${encodeURIComponent(key)}`, { method: "DELETE" }),
};
