"""One-off backfill: regenerate markdown/csv for records that have full_text
but were saved before auto-save v2 (or via paths that skipped artifacts).

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


def main() -> int:
    login = requests.post(f"{API}/auth/login", json={"username": USER, "password": PASS}, timeout=30)
    login.raise_for_status()
    token = login.json()["token"]
    headers = {"X-Session-Token": token}

    fixed = skipped = page = 0
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
            text = (data.get("full_text") or "").strip()
            has_md = bool((data.get("markdown") or "").strip())
            has_csv = bool((data.get("csv") or "").strip())
            if not text:
                continue
            if has_md and has_csv:
                skipped += 1
                continue
            next_data = dict(data)
            if not has_md:
                next_data["markdown"] = text
            if not has_csv:
                next_data["csv"] = build_csv(text)
            pr = requests.patch(f"{API}/records/{rec['id']}", json={"data": next_data}, headers=headers, timeout=60)
            if pr.ok:
                fixed += 1
            else:
                print(f"  !! failed {rec['id']}: {pr.status_code}", file=sys.stderr)
        if page >= (body.get("total_pages") or 1):
            break

    print(f"done — backfilled {fixed}, already-ok {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
