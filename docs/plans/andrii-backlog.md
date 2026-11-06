# Andrii backlog

Roadmap (CLAUDE.md section 8) is a guide, not a contract. Order here = what is most
useful now. Re-sort freely; move done items to the bottom.

## Now
1. **Pilot outreach** (deadline this week). Research agent -> `docs/leads.csv`
   (German steel-construction / metal-working SMEs), 10-15 personalised German email drafts.
   Human sends every email. Unblocks: real certificates, real order format, time measurements.
2. **Business case + pricing** (half page for proposal). 300 cert/month baseline, sourced
   hourly cost of a quality inspector, savings in h and EUR, 3 pricing options.
3. **Domain + AI for Good paragraph**. Proposed: rail and bridge safety; confirm with Dler.

## Next (rules / eval)
4. Verify `rules/limits/*.yaml` against licensed EN 10025-2, set `verified: true`.
5. Synthetic error generator: take a green extraction, inject one wrong value
   (out of limit, wrong grade, wrong order no., missing value), store expected verdict.
   This is the core metric: zero missed wrong values.
6. Eval harness: detection rate on synthetic set, false-red rate, cost per certificate.
7. More grades (10-20): S275JR, S355JR/J0/K2, S460, aluminium EN AW-5754 / 6082.

## Later / when needed
- Thickness bands in limit tables (now only 3-16 mm).
- Checks: certificate thickness vs order, batch number present, CEV if order requires it.
- Research agent spec + outreach agent spec (text for "agents as employees").

## Done
- Week 0 skeleton: schema v0.1, 5 golden fixtures, minimal engine, CI (2026-11-06).
