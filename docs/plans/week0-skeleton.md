# Plan: week 0 skeleton

Goal (roadmap week 0): schema v0.1 + 5 golden fixtures + CI green.

Done:
1. Repo layout per CLAUDE.md section 4, `.gitignore` (data/private, CLAUDE.local.md).
2. `schema/models.py`: Source, ExtractedValue, Extraction, OrderRecord, Finding, CheckResult, `SCHEMA_VERSION = "0.1.0"`.
3. `schema/examples/`: one example per model.
4. `data/fixtures/golden/`: 01 green, 02 red (ReH too low), 03 yellow (low confidence),
   04 red (grade mismatch), 05 yellow (missing KV). Each: extraction.json, order.json, expected.json.
5. Minimal deterministic `rules/engine.py` + limit tables S355J2, S235JR (unverified).
6. Tests: `tests/shared/` (schema + golden), `tests/andrii/` (engine). CI: `uv sync --locked && uv run pytest`.

Next:
- Dler: review + approve schema PR, push repo to GitHub, CI.
- Andrii: verify limit values, extend to 10-20 grades, synthetic generator (weeks 1-2), sample order format from pilot.
