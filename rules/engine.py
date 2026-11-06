"""Compare an Extraction with its OrderRecord and the grade's limit table.

Status per check:
- red:    value present and outside limit / mismatch with order
- yellow: value missing, not numeric, low confidence, or no limits known
- green:  value present, confident, within limit
Verdict = worst status of all findings.
"""
from pathlib import Path

import yaml

from schema import CheckResult, ExtractedValue, Extraction, Finding, OrderRecord, Status

LIMITS_DIR = Path(__file__).parent / "limits"
MIN_CONFIDENCE = 0.85  # see docs/decisions.md
_RANK = {Status.GREEN: 0, Status.YELLOW: 1, Status.RED: 2}


def normalize_grade(grade: str) -> str:
    return grade.replace(" ", "").upper()


def load_limits(grade: str) -> dict | None:
    """Limit file is named after the base grade, without delivery condition (+N, +AR...)."""
    base = normalize_grade(grade).split("+")[0]
    path = LIMITS_DIR / f"{base}.yaml"
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _missing(ev: ExtractedValue | None) -> bool:
    return ev is None or ev.value is None


def check_text(rule_id: str, ev: ExtractedValue | None, expected: str) -> Finding:
    if _missing(ev):
        return Finding(rule_id=rule_id, status=Status.YELLOW, message="value not found", limit=expected)
    if normalize_grade(str(ev.value)) != normalize_grade(expected):
        return Finding(
            rule_id=rule_id, status=Status.RED, value=ev.value, limit=expected, source=ev.source,
            message=f"'{ev.value}' does not match order '{expected}'",
        )
    if ev.confidence < MIN_CONFIDENCE:
        return Finding(
            rule_id=rule_id, status=Status.YELLOW, value=ev.value, limit=expected, source=ev.source,
            message=f"low reading confidence ({ev.confidence:.2f})",
        )
    return Finding(rule_id=rule_id, status=Status.GREEN, value=ev.value, limit=expected,
                   source=ev.source, message="matches order")


def _limit_text(lim: dict) -> str:
    lo, hi = lim.get("min"), lim.get("max")
    if lo is not None and hi is not None:
        return f"{lo}..{hi}"
    return f">= {lo}" if lo is not None else f"<= {hi}"


def check_value(rule_id: str, ev: ExtractedValue | None, lim: dict) -> Finding:
    limit = _limit_text(lim)
    if _missing(ev):
        return Finding(rule_id=rule_id, status=Status.YELLOW, message="value not found", limit=limit)
    if not isinstance(ev.value, (int, float)):
        return Finding(rule_id=rule_id, status=Status.YELLOW, value=ev.value, limit=limit,
                       source=ev.source, message="value is not a number")
    lo, hi = lim.get("min"), lim.get("max")
    if (lo is not None and ev.value < lo) or (hi is not None and ev.value > hi):
        return Finding(rule_id=rule_id, status=Status.RED, value=ev.value, limit=limit,
                       source=ev.source, message=f"{ev.value} outside limit {limit}")
    if ev.confidence < MIN_CONFIDENCE:
        return Finding(rule_id=rule_id, status=Status.YELLOW, value=ev.value, limit=limit,
                       source=ev.source, message=f"low reading confidence ({ev.confidence:.2f})")
    return Finding(rule_id=rule_id, status=Status.GREEN, value=ev.value, limit=limit,
                   source=ev.source, message="within limit")


def check(extraction: Extraction, order: OrderRecord) -> CheckResult:
    findings = [
        check_text("certificate.type", extraction.certificate_type, order.certificate_type),
        check_text("order.number", extraction.order_number, order.order_number),
        check_text("grade.match", extraction.grade, order.grade),
    ]

    limits = load_limits(order.grade)
    if limits is None:
        findings.append(Finding(rule_id="limits.available", status=Status.YELLOW,
                                message=f"no limit table for grade '{order.grade}'"))
    else:
        t_lo, t_hi = limits["thickness_range_mm"]
        if not t_lo <= order.thickness_mm <= t_hi:
            findings.append(Finding(
                rule_id="limits.thickness", status=Status.YELLOW,
                message=f"limit table covers {t_lo}..{t_hi} mm, order is {order.thickness_mm} mm",
            ))
        for group in ("chemistry", "mechanical"):
            values: dict[str, ExtractedValue] = getattr(extraction, group)
            for key, lim in limits.get(group, {}).items():
                findings.append(check_value(f"{group}.{key}", values.get(key), lim))

    verdict = max((f.status for f in findings), key=_RANK.__getitem__)
    return CheckResult(certificate_id=extraction.certificate_id, order_number=order.order_number,
                       verdict=verdict, findings=findings)
