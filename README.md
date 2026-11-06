# CertCheck

Reads EN 10204 type 3.1 material certificates (AI), checks every value against the
purchase order and standard limits (deterministic rules), and sends only yellow/red
cases to a human. Project brief: [CLAUDE.md](CLAUDE.md).

## Setup
```bash
uv sync
uv run pytest
```

## Layout
| Folder | Owner | Content |
|---|---|---|
| `schema/` | shared (PR, both approve) | Pydantic models = the contract, JSON examples |
| `data/` | shared | `raw/`, `synthetic/`, `labels/`, `fixtures/golden/`; `private/` is git-ignored (NDA) |
| `reader/` | Dler | PDF/scan -> `Extraction` |
| `importers/` | Dler | structured digital certificates -> `Extraction` (later) |
| `app/` | Dler | intake, review UI, archive |
| `rules/` | Andrii | rule engine + limit tables (`rules/limits/*.yaml`) |
| `eval/` | Andrii | metrics, benchmarks, cost per certificate |
| `tests/` | each in own subfolder | `tests/shared/` = schema + golden fixtures |
| `docs/` | both | `plans/`, `decisions.md` |

## Data flow
`Extraction` (reader) + `OrderRecord` (intake) -> `rules.check()` -> `CheckResult` (green/yellow/red + reasons).
