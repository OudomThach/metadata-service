import { useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api, type RecordOut } from "../api/client";

// --------------------------------------------------------------------------- //
// The three dataset tabs: Overview (metadata + file + validation),
// Columns (schema editor) and References (url/text/citation/linked dataset).
// All state is saved to the record's data JSON via onPatch({ data }).
// --------------------------------------------------------------------------- //

const FREQUENCIES = ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly", "Once", "Irregular"];
const COLUMN_TYPES = ["text", "number", "date", "boolean", "json"];
const REF_TYPES = ["url", "text", "citation", "linked dataset"];
const EMBED_MAX = 5 * 1024 * 1024;
const ACCEPTED_EXT = [".csv", ".geojson", ".kml", ".pdf", ".parquet", ".orc", ".xlsx", ".xls", ".xlsm"];

interface ColumnRow {
  name: string;
  type: string;
  description: string;
}

interface ReferenceRow {
  type: string;
  url?: string;
  text?: string;
  citation?: string;
  linked_dataset_id?: string | null;
  linked_name?: string;
}

type PatchFn = (body: Record<string, unknown>) => void;

function Section({ title, children, right }: { title: string; children: React.ReactNode; right?: React.ReactNode }) {
  return (
    <div className="panel p-4">
      <div className="mb-2 flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">{title}</span>
        {right}
      </div>
      {children}
    </div>
  );
}

function fmtSize(bytes: number): string {
  return bytes >= 1024 * 1024 ? `${(bytes / (1024 * 1024)).toFixed(1)} MB` : bytes >= 1024 ? `${(bytes / 1024).toFixed(0)} KB` : `${bytes} B`;
}

// ── Overview ──────────────────────────────────────────────────────────────── //
export function DatasetOverview({ rec, canEdit, onPatch }: { rec: RecordOut; canEdit: boolean; onPatch: PatchFn }) {
  const ds = (rec.data?.dataset ?? {}) as Record<string, unknown>;
  const [name, setName] = useState(String(ds.name ?? ""));
  const [managedBy, setManagedBy] = useState(String(ds.managed_by ?? ""));
  const [frequency, setFrequency] = useState(String(ds.frequency ?? ""));
  const [coverageStart, setCoverageStart] = useState(String(ds.coverage_start ?? ""));
  const [coverageEnd, setCoverageEnd] = useState(String(ds.coverage_end ?? ""));
  const [categories, setCategories] = useState(Array.isArray(ds.categories) ? (ds.categories as string[]).join(", ") : String(ds.categories ?? ""));
  const [collection, setCollection] = useState(String(ds.collection ?? ""));
  const [url, setUrl] = useState(String(ds.url ?? ""));
  const [description, setDescription] = useState(String(ds.description ?? ""));
  const [file, setFile] = useState<{ name: string; size: number; type: string } | null>(() => {
    const f = ds.file as { name?: string; size?: number; type?: string } | null;
    return f && f.name ? { name: String(f.name), size: Number(f.size ?? 0), type: String(f.type ?? "") } : null;
  });
  const [fileBase64, setFileBase64] = useState<string | null>(String(ds.file_base64 ?? "") || null);
  const [embedNote, setEmbedNote] = useState<string | null>(null);
  const [managedByCustom, setManagedByCustom] = useState(false);
  const [collectionCustom, setCollectionCustom] = useState(false);
  const [validation, setValidation] = useState<{ ok: boolean; issues: string[] } | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);

  const { data: orgs } = useQuery({ queryKey: ["organizations"], queryFn: api.listOrganizations });
  const { data: cats } = useQuery({ queryKey: ["categories"], queryFn: api.listCategories });
  const { data: cols } = useQuery({ queryKey: ["collections"], queryFn: api.listCollections });

  const save = () => {
    onPatch({
      data: {
        ...rec.data,
        dataset: {
          name: name.trim() || null,
          managed_by: managedBy.trim() || null,
          frequency: frequency || null,
          coverage_start: coverageStart || null,
          coverage_end: coverageEnd || null,
          categories: categories.trim() || null,
          collection: collection.trim() || null,
          url: url.trim() || null,
          description: description.trim() || null,
          file,
          file_base64: fileBase64,
        },
      },
    });
  };

  const runValidation = () => {
    const issues: string[] = [];
    if (!name.trim()) issues.push("Dataset name is required.");
    if (!managedBy.trim()) issues.push("Managed by is required.");
    if (!frequency) issues.push("Frequency is required.");
    if (!coverageStart) issues.push("Coverage start is required.");
    if (!categories.trim()) issues.push("Categories are required.");
    if (description.length > 1500) issues.push(`Description exceeds 1500 characters (${description.length}).`);
    if (!file) issues.push("Upload a data file.");
    setValidation({ ok: issues.length === 0, issues });
  };

  const acceptFile = (f: File | undefined | null) => {
    if (!f) return;
    const ext = f.name.slice(f.name.lastIndexOf(".")).toLowerCase();
    if (!ACCEPTED_EXT.includes(ext)) {
      setEmbedNote(`Only ${ACCEPTED_EXT.join(" ")} files are accepted`);
      return;
    }
    setFile({ name: f.name, size: f.size, type: f.type });
    setEmbedNote(null);
    if (f.size <= EMBED_MAX) {
      const reader = new FileReader();
      reader.onload = () => {
        const dataUrl = String(reader.result ?? "");
        setFileBase64(dataUrl.includes(",") ? dataUrl.split(",", 2)[1] : dataUrl);
        setEmbedNote(null);
      };
      reader.readAsDataURL(f);
    } else {
      setFileBase64(null);
      setEmbedNote("too large to embed (name/size saved only)");
    }
  };

  // Category chips, tree-ordered like the SPA form.
  const categoryChips = (() => {
    const list = cats ?? [];
    const byParent = new Map<number | null, typeof list>();
    for (const c of list) byParent.set(c.parent_id, [...(byParent.get(c.parent_id) ?? []), c]);
    const ordered: { name: string; depth: number }[] = [];
    const walk = (parent: number | null, depth: number) => {
      for (const c of (byParent.get(parent) ?? []).sort((a, b) => a.sort - b.sort)) {
        ordered.push({ name: c.name, depth });
        walk(c.id, depth + 1);
      }
    };
    walk(null, 0);
    return ordered;
  })();
  const selectedCats = new Set(categories.split(",").map((c) => c.trim()).filter(Boolean));
  const toggleCat = (name: string) => {
    const next = new Set(selectedCats);
    if (next.has(name)) next.delete(name); else next.add(name);
    setCategories([...next].join(", "));
  };

  return (
    <div className="space-y-4">
      <Section title="Dataset">
        <div className="grid gap-3 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Dataset name *</label>
            <input className="input w-full" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Cambodia's Actual Subsidies and Tax Less Subsidies on Product 2000" disabled={!canEdit} />
          </div>
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Managed by *</label>
            <select
              className="input w-full"
              disabled={!canEdit}
              value={managedByCustom ? "__custom__" : (orgs ?? []).some((o) => o.name === managedBy) ? managedBy : (managedBy ? "__custom__" : "")}
              onChange={(e) => {
                if (e.target.value === "__custom__") { setManagedByCustom(true); setManagedBy(""); }
                else { setManagedByCustom(false); setManagedBy(e.target.value); }
              }}
            >
              <option value="">Select…</option>
              {(orgs ?? []).map((o) => <option key={o.id} value={o.name}>{o.name}</option>)}
              <option value="__custom__">— custom —</option>
            </select>
            {managedByCustom && <input className="input mt-1 w-full" value={managedBy} onChange={(e) => setManagedBy(e.target.value)} disabled={!canEdit} placeholder="e.g. GDDE, MEF" />}
          </div>
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Frequency *</label>
            <select className="input w-full" value={frequency} onChange={(e) => setFrequency(e.target.value)} disabled={!canEdit}>
              <option value="">Select…</option>
              {FREQUENCIES.map((f) => <option key={f} value={f}>{f}</option>)}
            </select>
          </div>
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Coverage start *</label>
            <input className="input w-full" type="date" value={coverageStart} onChange={(e) => setCoverageStart(e.target.value)} disabled={!canEdit} />
          </div>
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Coverage end</label>
            <input className="input w-full" type="date" value={coverageEnd} onChange={(e) => setCoverageEnd(e.target.value)} disabled={!canEdit} />
          </div>
          <div className="sm:col-span-2">
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Categories *</label>
            <div className="flex flex-wrap items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-2 py-1.5">
              {categoryChips.map((c) => (
                <button
                  key={c.name}
                  type="button"
                  disabled={!canEdit}
                  onClick={() => toggleCat(c.name)}
                  aria-pressed={selectedCats.has(c.name)}
                  className={`rounded-full px-2 py-0.5 text-[11px] font-medium transition-colors disabled:cursor-default ${
                    selectedCats.has(c.name) ? "bg-accent text-white" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                  }`}
                  style={{ marginLeft: `${c.depth * 10}px` }}
                >
                  {c.name}
                </button>
              ))}
              <input
                className="ml-1 w-48 border-0 bg-transparent text-[11px] text-slate-700 outline-none placeholder:text-slate-400"
                value={categories}
                onChange={(e) => setCategories(e.target.value)}
                disabled={!canEdit}
                placeholder="receipt, bank transfer"
              />
            </div>
          </div>
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">Collection</label>
            <select
              className="input w-full"
              disabled={!canEdit}
              value={collectionCustom ? "__custom__" : (cols ?? []).some((c) => c.name === collection) ? collection : (collection ? "__custom__" : "")}
              onChange={(e) => {
                if (e.target.value === "__custom__") { setCollectionCustom(true); setCollection(""); }
                else { setCollectionCustom(false); setCollection(e.target.value); }
              }}
            >
              <option value="">Select…</option>
              {(cols ?? []).map((c) => <option key={c.id} value={c.name}>{c.name}</option>)}
              <option value="__custom__">— custom —</option>
            </select>
            {collectionCustom && <input className="input mt-1 w-full" value={collection} onChange={(e) => setCollection(e.target.value)} disabled={!canEdit} placeholder="e.g. NIS Publications" />}
          </div>
          <div>
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">URL / Source link</label>
            <input className="input w-full" value={url} onChange={(e) => setUrl(e.target.value)} disabled={!canEdit} placeholder="https://…" />
          </div>
          <div className="sm:col-span-2">
            <label className="mb-0.5 block text-[11px] font-semibold uppercase tracking-wide text-slate-500">
              Description <span className="normal-case text-slate-400">({description.length}/1500)</span>
            </label>
            <textarea className="input min-h-20 w-full" value={description} onChange={(e) => setDescription(e.target.value.slice(0, 1500))} disabled={!canEdit} rows={3} />
          </div>
        </div>
      </Section>

      <Section title="Data and validation">
        <p className="mb-2 text-xs text-slate-500">Ensure display formats, and details are accurately filled. Start the validation when you're ready.</p>
        <div className="flex items-center gap-2">
          <button type="button" className="btn-secondary px-3 py-1.5 text-xs" onClick={runValidation} disabled={!canEdit}>
            Start the validation
          </button>
          {validation && (
            <span className={`text-xs ${validation.ok ? "text-emerald-600" : "text-red-500"}`}>
              {validation.ok ? "Validation passed — ready to publish." : `${validation.issues.length} issue(s) found.`}
            </span>
          )}
        </div>
        {validation && !validation.ok && (
          <ul className="mt-2 space-y-0.5">
            {validation.issues.map((issue, i) => <li key={i} className="text-xs text-red-500">• {issue}</li>)}
          </ul>
        )}
      </Section>

      <Section title="Upload a data file">
        <div
          tabIndex={0}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => { e.preventDefault(); acceptFile(e.dataTransfer.files?.[0]); }}
          onClick={() => canEdit && fileInput.current?.click()}
          className="cursor-pointer rounded-xl border border-dashed border-slate-300 bg-white/60 px-4 py-5 text-center outline-none transition-colors hover:border-accent focus:border-accent"
        >
          {file ? (
            <div className="text-sm">
              <span className="font-medium text-slate-900">{file.name}</span>
              <span className="ml-2 text-xs text-slate-500">{fmtSize(file.size)}</span>
              <span className={`ml-2 text-xs ${embedNote ? "text-amber-600" : "text-emerald-600"}`}>
                {embedNote ?? "embedded — downloadable from the portal"}
              </span>
              {canEdit && (
                <button type="button" className="ml-3 text-xs text-red-500 hover:underline" onClick={(e) => { e.stopPropagation(); setFile(null); setFileBase64(null); }}>
                  remove
                </button>
              )}
            </div>
          ) : (
            <div className="text-sm text-slate-500">
              Drop file here, Click or press Ctrl + V to upload.
              <div className="mt-1 text-[11px] text-slate-400">Only {ACCEPTED_EXT.join(" ")} formats are accepted</div>
            </div>
          )}
        </div>
        <input ref={fileInput} type="file" className="hidden" accept={ACCEPTED_EXT.join(",")} onChange={(e) => { acceptFile(e.target.files?.[0]); e.target.value = ""; }} />
      </Section>

      {canEdit && (
        <div className="flex justify-end">
          <button type="button" className="btn-primary px-4 py-2 text-sm" onClick={save}>
            Save dataset
          </button>
        </div>
      )}
    </div>
  );
}

// ── Columns (schema) ──────────────────────────────────────────────────────── //
export function DatasetColumns({ rec, canEdit, onPatch }: { rec: RecordOut; canEdit: boolean; onPatch: PatchFn }) {
  const [columns, setColumns] = useState<ColumnRow[]>(() =>
    (Array.isArray(rec.data?.columns) ? (rec.data.columns as unknown[]) : []).map((c) => {
      const row = c as Partial<ColumnRow>;
      return { name: String(row.name ?? ""), type: String(row.type ?? "text"), description: String(row.description ?? "") };
    }),
  );

  const update = (i: number, patch: Partial<ColumnRow>) => setColumns((cs) => cs.map((c, idx) => (idx === i ? { ...c, ...patch } : c)));
  const move = (i: number, dir: -1 | 1) =>
    setColumns((cs) => {
      const j = i + dir;
      if (j < 0 || j >= cs.length) return cs;
      const next = [...cs];
      [next[i], next[j]] = [next[j], next[i]];
      return next;
    });
  const remove = (i: number) => setColumns((cs) => cs.filter((_, idx) => idx !== i));

  const save = () => onPatch({ data: { ...rec.data, columns: columns.filter((c) => c.name.trim()) } });

  return (
    <div className="space-y-4">
      <Section title={`Columns (${columns.length})`} right={<span className="text-xs text-slate-400">data type · description</span>}>
        {columns.length === 0 && <div className="py-4 text-sm text-slate-500">No columns defined yet — add the dataset's schema below.</div>}
        <div className="space-y-2">
          {columns.map((c, i) => (
            <div key={i} className="flex flex-wrap items-center gap-2 rounded-lg border border-slate-200 bg-white p-2">
              <span className="w-6 text-center text-xs text-slate-400">{i + 1}</span>
              <input className="input w-44" placeholder="Title (e.g. Province)" value={c.name} onChange={(e) => update(i, { name: e.target.value })} disabled={!canEdit} />
              <select className="input w-28" value={c.type} onChange={(e) => update(i, { type: e.target.value })} disabled={!canEdit}>
                {COLUMN_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
              </select>
              <input className="input min-w-40 flex-1" placeholder="Description" value={c.description} onChange={(e) => update(i, { description: e.target.value })} disabled={!canEdit} />
              {canEdit && (
                <div className="flex items-center gap-0.5">
                  <button type="button" className="rounded px-1.5 py-0.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700" disabled={i === 0} onClick={() => move(i, -1)} title="Move up">↑</button>
                  <button type="button" className="rounded px-1.5 py-0.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700" disabled={i === columns.length - 1} onClick={() => move(i, 1)} title="Move down">↓</button>
                  <button type="button" className="rounded px-1.5 py-0.5 text-red-400 hover:bg-red-50 hover:text-red-600" onClick={() => remove(i)} title="Delete">✕</button>
                </div>
              )}
            </div>
          ))}
        </div>
        {canEdit && (
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <button type="button" className="btn-secondary px-3 py-1.5 text-xs" onClick={() => setColumns((cs) => [...cs, { name: "", type: "text", description: "" }])}>
              + Add column
            </button>
            <button type="button" className="btn-primary px-4 py-1.5 text-xs" onClick={save}>
              Save schema
            </button>
          </div>
        )}
      </Section>
    </div>
  );
}

// ── Data (editable table grid) ────────────────────────────────────────────── //
function esc(s: string): string {
  return `"${String(s ?? "").replace(/"/g, '""')}"`;
}

export function rowsToMarkdown(rows: string[][], hasHeader: boolean): string {
  if (rows.length === 0) return "";
  const width = Math.max(...rows.map((r) => r.length));
  const pad = (r: string[]) => [...r, ...Array<string>(Math.max(0, width - r.length)).fill("")];
  const lines = rows.map((r) => `| ${pad(r).join(" | ")} |`);
  if (hasHeader && rows.length > 1) {
    lines.splice(1, 0, `| ${Array<string>(width).fill("---").join(" | ")} |`);
  }
  return lines.join("\n");
}

export function rowsToCsv(rows: string[][]): string {
  return "\uFEFF" + rows.map((r) => r.map(esc).join(",")).join("\r\n");
}

function parseRowsFromText(text: string): string[][] {
  const lines = text.split("\n").map((l) => l.trim()).filter((l) => l.includes("|"));
  const rows = lines.map((l) => l.replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim()));
  return rows.filter((r) => r.some((c) => c));
}

export function DatasetData({ rec, canEdit, onPatch }: { rec: RecordOut; canEdit: boolean; onPatch: PatchFn }) {
  const initial = (() => {
    const stored = Array.isArray(rec.data?.rows) ? (rec.data.rows as unknown[][]) : null;
    if (stored) return stored.map((r) => r.map((c) => String(c ?? "")));
    const text = String(rec.data?.markdown ?? rec.data?.full_text ?? "");
    return parseRowsFromText(text);
  })();
  const columnNames = (Array.isArray(rec.data?.columns) ? (rec.data.columns as unknown[]) : []).map((c) =>
    String((c as { name?: string }).name ?? ""),
  );
  const hasHeader = columnNames.length > 0;
  const [rows, setRows] = useState<string[][]>(initial);
  const [headerRow, setHeaderRow] = useState(columnNames);

  const width = Math.max(1, ...rows.map((r) => r.length), headerRow.length);
  const padRow = (r: string[]) => [...r, ...Array<string>(Math.max(0, width - r.length)).fill("")];

  const setCell = (r: number, c: number, v: string) =>
    setRows((rs) => rs.map((row, ri) => (ri === r ? padRow(row).map((x, ci) => (ci === c ? v : x)) : row)));
  const addRow = () => setRows((rs) => [...rs, Array<string>(width).fill("")]);
  const removeRow = (r: number) => setRows((rs) => rs.filter((_, ri) => ri !== r));
  const addColumn = () => setHeaderRow((hs) => [...hs, ""]);
  const removeColumn = (c: number) => {
    setRows((rs) => rs.map((row) => padRow(row).filter((_, ci) => ci !== c)));
    setHeaderRow((hs) => hs.filter((_, ci) => ci !== c));
  };
  const moveColumn = (c: number, dir: -1 | 1) => {
    const j = c + dir;
    if (j < 0 || j >= width) return;
    setRows((rs) => rs.map((row) => {
      const p = padRow(row);
      [p[c], p[j]] = [p[j], p[c]];
      return p;
    }));
    setHeaderRow((hs) => {
      const h = [...hs, ...Array<string>(Math.max(0, width - hs.length)).fill("")];
      [h[c], h[j]] = [h[j], h[c]];
      return h;
    });
  };

  const save = () => {
    const grid = rows.map(padRow);
    const markdown = rowsToMarkdown([...(hasHeader ? [headerRow] : []), ...grid], hasHeader);
    const csv = rowsToCsv([...(hasHeader ? [headerRow] : []), ...grid]);
    onPatch({ data: { ...rec.data, rows: grid, markdown, csv } });
  };

  return (
    <div className="space-y-4">
      <Section title={`Data (${rows.length} rows × ${width} cols)`} right={<span className="text-xs text-slate-400">click a cell to edit · markdown + csv regenerate on save</span>}>
        <div className="overflow-x-auto rounded-lg border border-slate-200">
          <table className="w-full border-collapse text-sm">
            {hasHeader && (
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50">
                  {headerRow.map((h, c) => (
                    <th key={c} className="border-r border-slate-200 px-1 py-1 last:border-r-0">
                      <div className="flex items-center gap-0.5">
                        <input
                          className="input w-full min-w-24 py-1 text-xs font-semibold"
                          placeholder={`Column ${c + 1}`}
                          value={h}
                          onChange={(e) => setHeaderRow((hs) => hs.map((x, ci) => (ci === c ? e.target.value : x)))}
                          disabled={!canEdit}
                        />
                        {canEdit && (
                          <span className="flex shrink-0 flex-col">
                            <button type="button" className="px-0.5 text-[9px] text-slate-400 hover:text-slate-700" disabled={c === 0} onClick={() => moveColumn(c, -1)}>▲</button>
                            <button type="button" className="px-0.5 text-[9px] text-slate-400 hover:text-slate-700" disabled={c === width - 1} onClick={() => moveColumn(c, 1)}>▼</button>
                            <button type="button" className="px-0.5 text-[9px] text-red-400 hover:text-red-600" onClick={() => removeColumn(c)}>✕</button>
                          </span>
                        )}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
            )}
            <tbody>
              {rows.map((row, r) => (
                <tr key={r} className="border-b border-slate-100 last:border-b-0 odd:bg-white even:bg-slate-50/60">
                  {padRow(row).map((cell, c) => (
                    <td key={c} className="border-r border-slate-100 px-1 py-0.5 last:border-r-0">
                      <input
                        className="w-full min-w-20 rounded border border-transparent bg-transparent px-1.5 py-1 text-xs text-slate-700 hover:border-slate-200 focus:border-accent focus:bg-white focus:outline-none"
                        value={cell}
                        onChange={(e) => setCell(r, c, e.target.value)}
                        disabled={!canEdit}
                      />
                    </td>
                  ))}
                  {canEdit && (
                    <td className="w-8 px-1">
                      <button type="button" className="rounded px-1 text-xs text-red-400 hover:bg-red-50 hover:text-red-600" onClick={() => removeRow(r)} title="Delete row">✕</button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {rows.length === 0 && <div className="py-3 text-sm text-slate-500">No table data parsed from this record yet.</div>}
        {canEdit && (
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <button type="button" className="btn-secondary px-3 py-1.5 text-xs" onClick={addRow}>+ Add row</button>
            <button type="button" className="btn-secondary px-3 py-1.5 text-xs" onClick={addColumn}>+ Add column</button>
            <button type="button" className="btn-primary px-4 py-1.5 text-xs" onClick={save}>Save data</button>
          </div>
        )}
      </Section>
    </div>
  );
}

// ── References ────────────────────────────────────────────────────────────── //
export function DatasetReferences({ rec, canEdit, onPatch }: { rec: RecordOut; canEdit: boolean; onPatch: PatchFn }) {
  const [refs, setRefs] = useState<ReferenceRow[]>(() =>
    (Array.isArray(rec.data?.references) ? (rec.data.references as unknown[]) : []).map((r) => r as ReferenceRow),
  );
  const { data: datasets } = useQuery({ queryKey: ["datasets"], queryFn: () => api.listDatasets({ page_size: 200 }) });

  const update = (i: number, patch: Partial<ReferenceRow>) => setRefs((rs) => rs.map((r, idx) => (idx === i ? { ...r, ...patch } : r)));
  const remove = (i: number) => setRefs((rs) => rs.filter((_, idx) => idx !== i));
  const save = () => onPatch({ data: { ...rec.data, references: refs } });

  const valueLabel = (t: string) =>
    t === "url" ? "URL" : t === "citation" ? "Citation" : t === "linked dataset" ? "Linked dataset" : "Text";

  return (
    <div className="space-y-4">
      <Section title={`References (${refs.length})`} right={<span className="text-xs text-slate-400">url · text · citation · linked dataset</span>}>
        {refs.length === 0 && <div className="py-4 text-sm text-slate-500">No references yet — add sources, citations or linked datasets.</div>}
        <div className="space-y-2">
          {refs.map((r, i) => (
            <div key={i} className="flex flex-wrap items-center gap-2 rounded-lg border border-slate-200 bg-white p-2">
              <select
                className="input w-36"
                value={r.type}
                onChange={(e) => {
                  const t = e.target.value;
                  const next: ReferenceRow = { ...r, type: t };
                  if (t !== "linked dataset") next.linked_dataset_id = null;
                  if (t === "linked dataset") { next.url = undefined; next.text = undefined; next.citation = undefined; }
                  update(i, next);
                }}
                disabled={!canEdit}
              >
                {REF_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
              </select>
              <span className="w-24 text-[11px] font-semibold uppercase tracking-wide text-slate-400">{valueLabel(r.type)}</span>
              {r.type === "linked dataset" ? (
                <select
                  className="input min-w-48 flex-1"
                  value={r.linked_dataset_id ?? ""}
                  onChange={(e) => {
                    const id = e.target.value;
                    const ds = (datasets?.items ?? []).find((d) => d.id === id);
                    update(i, { linked_dataset_id: id || null, linked_name: ds?.name });
                  }}
                  disabled={!canEdit}
                >
                  <option value="">Select dataset…</option>
                  {(datasets?.items ?? []).map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
                </select>
              ) : (
                <input
                  className="input min-w-48 flex-1"
                  placeholder={r.type === "url" ? "https://…" : r.type === "citation" ? "NIS (2000). National Accounts…" : "Reference text…"}
                  value={String(r.url ?? r.text ?? r.citation ?? "")}
                  onChange={(e) => {
                    const v = e.target.value;
                    const patch: Partial<ReferenceRow> = r.type === "url" ? { url: v } : r.type === "citation" ? { citation: v } : { text: v };
                    update(i, patch);
                  }}
                  disabled={!canEdit}
                />
              )}
              {canEdit && (
                <button type="button" className="rounded px-1.5 py-0.5 text-red-400 hover:bg-red-50 hover:text-red-600" onClick={() => remove(i)} title="Delete">✕</button>
              )}
            </div>
          ))}
        </div>
        {canEdit && (
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <button type="button" className="btn-secondary px-3 py-1.5 text-xs" onClick={() => setRefs((rs) => [...rs, { type: "url" }])}>
              + Add reference
            </button>
            <button type="button" className="btn-primary px-4 py-1.5 text-xs" onClick={save}>
              Save references
            </button>
          </div>
        )}
      </Section>
    </div>
  );
}
