#!/usr/bin/env python3
"""Verification script for the AI Paperwork and Forms Guide.

Run from the repository root:

    python3 tools/verify_guide.py

Exits 0 on success, nonzero on any failure. Intended as the project's
reproducible "build/test" check (no CI, no .github/workflows).
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOCS = ROOT / "docs"
TOOLS = ROOT / "tools"

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


class LinkParser(HTMLParser):
    """Collects hrefs from <a> tags and tracks open tags."""

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.links = []
        self.open_tags = []
        # Void / self-closing HTML5 elements that never need a close tag.
        self.void = {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr",
        }

    def handle_starttag(self, tag, attrs):
        self.open_tags.append(tag)
        if tag == "a":
            for k, v in attrs:
                if k == "href":
                    self.links.append(v)

    def handle_endtag(self, tag):
        while self.open_tags and self.open_tags[-1] != tag:
            self.open_tags.pop()
        if self.open_tags and self.open_tags[-1] == tag:
            self.open_tags.pop()

    def unclosed(self):
        return [t for t in self.open_tags if t not in self.void]


# ---------------------------------------------------------------------------
# Collect files
# ---------------------------------------------------------------------------
html_files = sorted(SITE.glob("*.html"))
existing_pages = {f.name for f in html_files}
existing_assets = {f.name for f in (SITE / "assets").iterdir()} if (SITE / "assets").exists() else set()
doc_md = {p.stem for p in DOCS.glob("*.md")}

print(f"Found {len(html_files)} HTML pages in site/")
print(f"Found {len(doc_md)} Markdown chapters in docs/")

# ---------------------------------------------------------------------------
# 1. HTML checks
# ---------------------------------------------------------------------------
for f in html_files:
    text = f.read_text(encoding="utf-8")
    parser = LinkParser(f)
    try:
        parser.feed(text)
    except Exception as e:
        err(f"{f.name}: HTML parse error: {e}")
        continue

    # Internal navigation links must resolve.
    for href in parser.links:
        if href.startswith(("#", "http", "https", "mailto:")):
            continue
        target = href.split("?")[0].split("#")[0]
        if target in existing_pages:
            continue
        if target in existing_assets:
            continue
        err(f"{f.name}: broken link -> {href}")

    # Required asset references.
    for ref in ("assets/style.css", "assets/script.js"):
        if ref not in text:
            err(f"{f.name}: missing reference to {ref}")

    # Required structural elements.
    if "<title>" not in text:
        err(f"{f.name}: missing <title>")
    if "<h1" not in text:
        err(f"{f.name}: missing <h1>")

    # Unclosed non-void tags.
    leftover = parser.unclosed()
    if leftover:
        warn(f"{f.name}: possibly unclosed tags: {leftover[-5:]}")

# ---------------------------------------------------------------------------
# 2. LICENSE exact copyright line
# ---------------------------------------------------------------------------
license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
expected = "Copyright (c) 2026 Asdale Dynamics, LLC"
if expected not in license_text:
    err("LICENSE missing exact copyright line")
else:
    print("LICENSE: exact copyright line present")

# ---------------------------------------------------------------------------
# 3. README credits Asdale Dynamics, LLC
# ---------------------------------------------------------------------------
readme = (ROOT / "README.md").read_text(encoding="utf-8")
if "Asdale Dynamics, LLC" not in readme:
    err("README does not credit Asdale Dynamics, LLC")
else:
    print("README: credits Asdale Dynamics, LLC")

# ---------------------------------------------------------------------------
# 4. No .github/workflows (forbidden)
# ---------------------------------------------------------------------------
if (ROOT / ".github" / "workflows").exists():
    err(".github/workflows exists (forbidden)")
else:
    print("No .github/workflows: OK")

# ---------------------------------------------------------------------------
# 5. No secrets / personal data patterns
# ---------------------------------------------------------------------------
secret_patterns = [
    (r"\bsk-[A-Za-z0-9]{20,}", "API key-like token"),
    (r"\b[0-9]{4}[-\s][0-9]{4}[-\s][0-9]{4}[-\s][0-9]{4}\b", "credit card number"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN-like"),
]
for f in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.css")) + list(ROOT.rglob("*.js")) + list(ROOT.rglob("*.py")) + list(ROOT.rglob("*.txt")):
    # Skip .git directory contents.
    if ".git" in f.parts:
        continue
    text = f.read_text(encoding="utf-8")
    for pat, label in secret_patterns:
        if re.search(pat, text):
            err(f"{f.relative_to(ROOT)}: possible {label} found")

# ---------------------------------------------------------------------------
# 6. Docs and site chapter parity
# ---------------------------------------------------------------------------
site_chapters = {p.stem for p in SITE.glob("*.html") if p.name != "index.html"}
extra_in_site = site_chapters - doc_md
extra_in_docs = doc_md - site_chapters - {"index", "privacy-checklist"}
if extra_in_site:
    err(f"site pages without docs: {sorted(extra_in_site)}")
if extra_in_docs:
    err(f"docs without site pages: {sorted(extra_in_docs)}")

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
print(f"\nErrors: {len(errors)}")
for e in errors:
    print(f"  [ERROR] {e}")
print(f"Warnings: {len(warnings)}")
for w in warnings:
    print(f"  [WARN]  {w}")

sys.exit(1 if errors else 0)
