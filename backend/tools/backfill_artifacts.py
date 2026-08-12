"""One-off backfill: regenerate markdown/csv for records that have text (or
table content) but were saved before auto-save v2 / via paths that skipped
artifacts.

Table records often have full_text="" while the grid lives in
data.json.structured_text (or data.json.cells) — those are recovered too.

Usage: python tools/backfill_artifacts.py
Reads METADATA_ADMIN_USER / METADATA_ADMIN_PASS / METADATA_BASE_URL (defaults
below). Idempotent — records that already have markdown are skipped.
"""

from __future__ import annotations

import os
import re
import sys

import requests

BASE = os.environ.get("METADATA_BASE_URL", "http://127.0.0.1:8095").rstrip("/")
USER = os.environ.get("METADATA_ADMIN_USER", "admin")
PASS = os.environ.get("METADATA_ADMIN_PASS", "romdoul-v1cgt5jkq492dhzymlwr")
API = f"{BASE}/api/v1"


def build_csv(text: str) -> str:
    def esc(s: str) -> str:
        return f'"{str(s or "").replace(chr(34), chr(34) * 2)}"'

    rows: list[list[str]] = []
    table_lines = [ln.strip() for ln in text.split("\n") if "|" in ln]
    if len(table_lines) >= 2:
        header = [c.strip() for c in table_lines[0].strip().strip("|").split("|")]
        body = []
        for ln in table_lines[1:]:
            if re.fullmatch(r"\|?\s*[-:]+\s*(\|\s*[-:]+\s*)+\|?\s*", ln):
                continue
            body.append([c.strip() for c in ln.strip().strip("|").split("|")])
        if header:
            rows = [header, *body]
    if not rows:
        rows = [[ln] for ln in text.split("\n") if ln.strip()]
    return "\ufeff" + "\r\n".join(",".join(esc(c) for c in r) for r in rows)


def cells_to_text(cells: list) -> str:
    """Rebuild a pipe table from a cells grid (row/col/text)."""
    grid: dict[tuple[int, int], str] = {}
    max_r = max_c = 0
    for c in cells:
        if not isinstance(c, dict):
            continue
        r, col = int(c.get("row", 0) or 0), int(c.get("col", 0) or 0)
        grid[(r, col)] = str(c.get("text") or "")
        max_r, max_c = max(max_r, r), max(max_c, col)
    if not grid:
        return ""
    lines = []
    for r in range(max_r + 1):
        cells_r = [grid.get((r, c), "") for c in range(max_c + 1)]
        lines.append("| " + " | ".join(cells_r) + " |")
    return "\n".join(lines)


def normalize_table(text: str) -> str:
    """Tab-separated rows (vLLM structured_text) -> pipe-table markdown."""
    if "|" in text:
        return text
    lines = [ln for ln in text.split("\n") if "\t" in ln]
    if not lines:
        return text
    return "\n".join("| " + " | ".join(ln.split("\t")) + " |" for ln in lines)


def record_text(data: dict) -> str:
    """Best available text: full_text > markdown > json.structured_text >
    json.text > cells-rebuilt grid. Normalizes tab-separated tables to pipes
    so markdown previews and the grid editors parse them."""
    for key in ("full_text", "markdown"):
        v = (data.get(key) or "").strip()
        if v:
            return normalize_table(v)
    j = data.get("json")
    if isinstance(j, dict):
        for key in ("structured_text", "text"):
            v = (j.get(key) or "").strip()
            if v:
                return normalize_table(v)
        cells = j.get("cells")
        if isinstance(cells, list) and cells:
            return cells_to_text(cells)
    cells = data.get("cells")
    if isinstance(cells, list) and cells:
        return cells_to_text(cells)
    return ""


def main() -> int:
    login = requests.post(f"{API}/auth/login", json={"username": USER, "password": PASS}, timeout=30)
    login.raise_for_status()
    token = login.json()["token"]
    headers = {"X-Session-Token": token}

    fixed = skipped = empty = page = 0
    while True:
        page += 1
        r = requests.get(f"{API}/records", params={"page": page, "page_size": 100}, headers=headers, timeout=60)
        r.raise_for_status()
        body = r.json()
        items = body.get("items") or []
        if not items:
            break
        for rec in items:
            data = rec.get("data") or {}
            has_md = bool((data.get("markdown") or "").strip())
            has_csv = bool((data.get("csv") or "").strip())
            if has_md and has_csv and "|" in (data.get("markdown") or ""):
                skipped += 1
                continue
            text = record_text(data)
            if not text:
                empty += 1
                continue
            next_data = dict(data)
            if not has_md:
                next_data["markdown"] = text
            if not has_csv:
                next_data["csv"] = build_csv(text)
            if not (next_data.get("full_text") or "").strip():
                next_data["full_text"] = text
            pr = requests.patch(f"{API}/records/{rec['id']}", json={"data": next_data}, headers=headers, timeout=60)
            if pr.ok:
                fixed += 1
            else:
                print(f"  !! failed {rec['id']}: {pr.status_code}", file=sys.stderr)
        if page >= (body.get("total_pages") or 1):
            break

    print(f"done — backfilled {fixed}, already-ok {skipped}, still-empty {empty}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
