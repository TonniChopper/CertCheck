# Decisions log

Format: date - decision - why - who.

- 2026-11-06 - Python 3.11, Pydantic v2, uv lockfile, pytest, GitHub Actions CI - simple, CLAUDE.md section 6/7 - Andrii
- 2026-11-06 - Schema v0.1: `Extraction` / `OrderRecord` / `CheckResult`; chemistry and mechanical as dicts keyed by symbol (C, Mn, ReH, Rm, A, KV) - easy to add elements without schema bump - Andrii (needs Dler approval)
- 2026-11-06 - Schema enforces source on every non-empty value (validator) - principle "every value carries its source" - Andrii
- 2026-11-06 - Rule engine: out of limit -> red (even with low confidence); missing / non-numeric / confidence < 0.85 -> yellow; verdict = worst finding - missing never green; threshold 0.85 is a first guess, tune in eval (weeks 8-9) - Andrii
- 2026-11-06 - Limit tables per base grade, one thickness band (3-16 mm) for now, marked `verified: false` until checked against a licensed copy of EN 10025-2 - copyright + correctness - Andrii

## Open
- Extraction model / OCR (Dler)
- UI framework (Dler)
- Archive database
- Hosting (Germany)
- Dimension check: compare certificate thickness with order (not in v0.1)
