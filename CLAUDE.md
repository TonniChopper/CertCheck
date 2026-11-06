# CLAUDE.md: CertCheck

> Shared project brief for Claude Code. Read fully before any task. Personal role notes go in `CLAUDE.local.md` (git-ignored).

## 1. Project description
CertCheck reads the material certificates (EN 10204 type 3.1) that German manufacturers receive with every steel or aluminium delivery and checks them automatically.
- AI reads the documents (any layout, including scans) and extracts grade, batch number, chemical values and strength values, plus where on the page each value came from.
- Fixed rules (no AI) compare every value with the purchase order and the limits of the relevant standard.
- A person signs off only on yellow/red cases.

Goal: show that the AI / rules / human split cuts checking time from minutes to seconds per certificate without letting errors slip through.
Context: course project "Frontier Systems", Leibniz Universitaet Hannover. Team: Dler Ahmed, Andrii Kozlov. Competitors: GoSmarter MillCert Reader, DocumentIQ, MTR.AI (mostly UK/US). Our focus: German SMEs, German-language documents, European standards, hosting in Germany, traceability.

## 2. Pipeline
1. Intake: email/upload, match certificate to purchase order.
2. Reading (AI): extract fields + source snippet (page, bbox) per value.
3. Checking (rule engine): deterministic, explainable. Output green / yellow / red with reasons.
4. Review: inspector sees only yellow/red, with the original snippet next to each value.
5. Archive: searchable by batch number, supplier, order.

## 3. Non-negotiable principles
- The AI never approves anything. The reader outputs data only; the verdict comes only from `rules/`.
- Rule engine is deterministic: no LLM calls in `rules/`.
- Every extracted value carries its source (page + bbox/snippet) and a confidence.
- Missing, unreadable or low-confidence values lead to yellow/red, never green.
- Target: miss zero deliberately wrong values in the synthetic test set.
- Do not copy text from standards (copyright). Store only needed limit values in `rules/limits/*.yaml`.
- Never commit real partner certificates (NDA); keep them in git-ignored `data/private/`.

## 4. Repo layout and ownership
```
schema/     SHARED: Pydantic models + JSON examples (changes only via PR, both approve)
data/       SHARED: raw/, synthetic/, labels/, fixtures/ (private/ is git-ignored)
reader/     DLER: PDF/scan -> extraction JSON
importers/  DLER: structured digital-certificate formats -> same schema (later)
app/        DLER: intake, review UI, archive
rules/      ANDRII: rule engine, limit tables (YAML)
eval/       ANDRII: metrics and benchmark scripts
tests/      each person in own subfolder
docs/       plans/, decisions.md, business case, agents, report notes
```
Only edit files in the folder owned by the current user unless the task explicitly says otherwise.

## 5. Roles
- Dler Ahmed: reading pipeline, review screen, archive.
- Andrii Kozlov: rule engine, limit tables, evaluation, pilot company contact.
- Both: data collection, testing, final presentation.

## 6. Contract and versioning rules
- `schema/` is the single contract: extraction output, order record, check result.
- Schema change: separate small PR, bump `SCHEMA_VERSION`, update examples and golden fixtures, both approve.
- Golden fixtures (at least 5, incl. a red one) must pass CI at all times.
- Develop against fixtures; do not wait for the other person's component.
- Pin dependencies with a lockfile (`uv`); dependency changes only via PR.
- Git: short-lived branches `dler/<topic>` / `andrii/<topic>`, small PRs, merge to `main` daily, no force-push.
- Tags: `v0.1` end of week 5 (end-to-end CLI), `v0.2` end of week 7 (review UI demo), `v1.0` final.

## 7. How Claude should work
1. For non-trivial tasks, write a short plan to `docs/plans/<feature>.md` first, then implement.
2. Stay inside the owner's folder; if a change elsewhere is needed, stop and say so.
3. Write tests with the code; run tests and schema validation before declaring done.
4. Log notable choices (model, OCR, thresholds, libraries) in `docs/decisions.md`.
5. Simple, readable Python 3.11+, type hints, Pydantic v2. Messy prototypes are fine early, but never break schema or tests on `main`.
6. Track cost per certificate in eval runs.
7. Ask before large refactors or new dependencies.

## 8. Roadmap (10 weeks)
| Weeks | Dler | Andrii | Milestone |
|---|---|---|---|
| 0 (days 1-2) | Repo, CI, this file | Field list, sample order format | Schema v0.1, 5 golden fixtures |
| 1-2 | Collect certificates, first extraction prototype | Synthetic generator, limit tables (10-20 grades) | 100-200 certificates + synthetic set |
| 3-5 | Reader (LLM/vision), scans, snippets, German layouts | Rule engine with explainable reasons, label 100 certificates | End-to-end CLI (v0.1) |
| 6-7 | Review screen, searchable archive | Evaluation harness, line up pilot | Working demo (v0.2) |
| 8-9 | Fix reader failures, prompt tuning, cost | Evaluation, shadow pilot, time measurement | Results table |
| 10 | Demo polish | Evaluation and discussion sections | Final report + presentation |

## 9. Success metrics
Reading accuracy (fields correct vs. hand-labelled set); error detection (wrong synthetic values flagged, target all); time saved per certificate (before/after); compute cost per certificate.

## 10. Risks
AI misreads a value (source snippets, human sign-off, no AI approval); too few real certificates (public + institute + synthetic); copyrighted standards (only needed limits via university access or customer specs); competitors (position for German firms, honest evaluation).

## 11. Open decisions (log in `docs/decisions.md`)
Extraction model / OCR, UI framework, archive database, hosting.

## 12. Course feedback additions (Nov 2026)
Teacher likes: AI / rules / human split, metrics, week plan. Missing: business case, AI for Good case, "agents as employees". Open question: will digital certificates shrink the market?

### 12.1 AI for Good + first-customer domain
- CertCheck stays a general engine. Proposed first domain (confirm): rail and bridge safety. A wrong steel grade in a load-bearing part is a real safety risk, and it fits the steel-construction traceability angle.
- Alternatives: wind/solar components (weaker link); recycled / low-carbon steel traceability (original, but needs extra fields such as recycled content and CO2).
- Checkable claims: (1) share of deliberately wrong values caught, target zero missed; (2) inspector hours freed for deeper checks.

### 12.2 Business case (half page in proposal)
- Baseline: 300 certificates/month x 10 min = 50 h/month. Convert to EUR with a SOURCED loaded hourly cost of a quality inspector (TODO: find source).
- Target: 1-2 min only for flagged cases; compute hours and EUR saved.
- Source or replace the "8-15 minutes" estimate; time 2-3 real inspections, ideally at the pilot company.
- Pricing options: per certificate, monthly subscription by volume, flat per site. Anchor against competitors and savings (e.g. ~30% of savings).
- Buyer: head of quality management or purchasing (IT involved for German hosting). User: the inspector.
- Pilot: secure now. 10-15 outreach emails to German steel-construction / metal-working firms; fallback: institute deliveries.

### 12.3 Agents as employees (agents that build and run the startup)
| Agent | Job | Inputs | Outputs | Human check |
|---|---|---|---|---|
| Coding agents (Claude Code) | Reader, rule engine, synthetic generator | Plans, schema, fixtures | PRs with tests | Owner reviews; both approve schema |
| Research agent | Find German manufacturers / pilot candidates | Search criteria | docs/leads.csv | Andrii verifies before contact |
| Outreach agent | Draft personalised German emails | Leads, pitch | Drafts | Human reviews and sends every email |
| Competitor agent | Weekly check of the 3 competitors | Competitor sites | docs/competitors.md (one page) | Weekly skim |
Principle: decide what must never be left to AI alone (verdicts, sending emails, schema changes).

### 12.4 Digital certificates (research note)
- Check EN 10204 digital initiatives and machine-readable certificate formats in steel/aluminium.
- Argument: transition is slow and uneven; small suppliers keep sending PDFs/scans; rules and review still apply to structured data.
- Design: reader handles PDFs today; `importers/` maps structured formats to the same schema later.

### 12.5 Task split for these additions
- Dler: coding-agent setup and descriptions, competitor agent, importer concept, agent roster text.
- Andrii: domain choice + AI for Good paragraph, business-case calculation, pricing, pilot outreach (deadline: this week), research and outreach agents.
- Together: digital-certificate note, status update to the teacher.
