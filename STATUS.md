# STATUS

AI Paperwork and Forms Guide — Asdale Dynamics, LLC

## What was built

A beginner-friendly guide to using AI for everyday paperwork, delivered two ways:

- `docs/` — plain-English Markdown manual (11 files)
- `site/` — static HTML version of the same manual (10 pages + CSS/JS), no build step; open any `.html` file in a browser

Plus:
- `LICENSE` — MIT License, Copyright (c) 2026 Asdale Dynamics, LLC
- `README.md` — overview crediting Asdale Dynamics, LLC and Dylan Asdale
- `STATUS.md` — this file

## Contents

Chapters:

1. Getting started with AI for paperwork
2. Reading forms with AI
3. Filling out applications
4. Benefits documents
5. Leases and rental agreements
6. Insurance documents
7. What never to share (privacy rules)
8. Saving and organizing your copies
- Privacy checklist

Covered document types: forms, job/benefit/housing applications, benefits letters and appeals, leases and rental agreements, insurance policies, claims, and explanation of benefits statements.

## How to run it

No installation required.

- Markdown: read any file in `docs/` with a text editor or Markdown viewer.
- HTML site: open `site/index.html` in a web browser and use the chapter navigation. All pages link to `assets/style.css` and `assets/script.js` (relative paths), so the folder can be copied anywhere or served from any static host.

## Verification results

Ran `python3 /tmp/kilo/verify_guide.py` (custom verification, `/tmp/kilo/verify_guide.py`):

- 10 HTML pages present; all internal navigation links resolve
- Every page references `assets/style.css` and `assets/script.js`
- Every page has `<title>` and `<h1>`
- HTML well-formedness: 0 errors
- `LICENSE` contains exact line: `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` credits Asdale Dynamics, LLC
- No `.github/workflows` directory
- No API keys, SSN-like, credit-card-like, or token patterns found in any file
- Docs and site chapter parity confirmed

Result: 0 errors. (Warnings from the checker are void/implicit HTML5 tag closures, not real issues.)

## Known gaps

- No automated test suite or CI configured (intentionally: no `.github/workflows`). Verification is a one-off script.
- HTML pages are hand-written mirrors of the Markdown; if docs change, site pages must be updated manually.
- No search function, print stylesheet, or dark mode.
- Examples are illustrative and use placeholder-style details; no real personal data is included.
- Not legal, medical, financial, or insurance advice (stated in each chapter and the README).

## Credit

Written and maintained by Dylan Asdale, founder of Asdale Dynamics, LLC (Indiana, formed October 2026).

Git: one commit, existing identity only, no Co-authored-by trailers, not pushed.
