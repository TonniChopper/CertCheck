"""Golden fixtures must pass on main at all times (CLAUDE.md section 6)."""
import json
from pathlib import Path

import pytest

from rules import check
from schema import Extraction, OrderRecord, Status

GOLDEN = Path(__file__).parents[2] / "data" / "fixtures" / "golden"
CASES = sorted(p for p in GOLDEN.iterdir() if p.is_dir())


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_at_least_five_fixtures_incl_red():
    assert len(CASES) >= 5
    assert any(_load(c / "expected.json")["verdict"] == "red" for c in CASES)


@pytest.mark.parametrize("case", CASES, ids=lambda p: p.name)
def test_golden_case(case: Path):
    extraction = Extraction.model_validate(_load(case / "extraction.json"))
    order = OrderRecord.model_validate(_load(case / "order.json"))
    expected = _load(case / "expected.json")

    result = check(extraction, order)

    assert result.verdict == Status(expected["verdict"])
    non_green = sorted(f.rule_id for f in result.findings if f.status != Status.GREEN)
    assert non_green == sorted(expected["non_green_rules"])
