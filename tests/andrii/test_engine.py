import json
from pathlib import Path

from rules import check
from rules.engine import check_value
from schema import ExtractedValue, Extraction, OrderRecord, Source, Status

GOLDEN = Path(__file__).parents[2] / "data" / "fixtures" / "golden" / "01_green_s355j2"


def _green_pair() -> tuple[Extraction, OrderRecord]:
    e = Extraction.model_validate_json((GOLDEN / "extraction.json").read_text(encoding="utf-8"))
    o = OrderRecord.model_validate_json((GOLDEN / "order.json").read_text(encoding="utf-8"))
    return e, o


def _ev(value, conf=0.99) -> ExtractedValue:
    return ExtractedValue(value=value, confidence=conf, source=Source(page=1, snippet=str(value)))


def test_out_of_range_is_red_even_with_low_confidence():
    assert check_value("x", _ev(0.30, conf=0.5), {"max": 0.20}).status == Status.RED


def test_text_value_for_number_is_yellow():
    assert check_value("x", _ev("n/a"), {"max": 0.20}).status == Status.YELLOW


def test_boundary_value_is_green():
    assert check_value("x", _ev(355), {"min": 355}).status == Status.GREEN


def test_unknown_grade_is_yellow():
    e, o = _green_pair()
    o.grade = e.grade.value = "X5CrNi18-10"
    result = check(e, o)
    assert result.verdict == Status.YELLOW
    assert any(f.rule_id == "limits.available" for f in result.findings)


def test_order_number_mismatch_is_red():
    e, o = _green_pair()
    o.order_number = "PO-2026-9999"
    assert check(e, o).verdict == Status.RED


def test_thickness_outside_table_is_yellow():
    e, o = _green_pair()
    o.thickness_mm = 40
    assert check(e, o).verdict == Status.YELLOW


def test_never_green_when_value_missing():
    e, o = _green_pair()
    e.chemistry.pop("C")
    assert check(e, o).verdict != Status.GREEN
