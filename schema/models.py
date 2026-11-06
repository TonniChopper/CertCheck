"""CertCheck data contract v0.1.

Three objects:
- Extraction:  what the reader found on a certificate (data only, no verdict).
- OrderRecord: what was ordered (from intake / ERP).
- CheckResult: verdict of the rule engine with one Finding per check.

Units: chemistry in % by mass, ReH/Rm in MPa, A in %, KV in J, thickness in mm.
"""
from enum import Enum

from pydantic import BaseModel, Field, model_validator

SCHEMA_VERSION = "0.1.0"


class Source(BaseModel):
    """Where on the document a value was read."""

    page: int = Field(ge=1)
    # (x0, y0, x1, y1), normalised to 0..1 of page width/height
    bbox: tuple[float, float, float, float] | None = None
    snippet: str | None = None  # raw text as printed, e.g. "C 0,17"


class ExtractedValue(BaseModel):
    value: float | str | None
    unit: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source: Source | None = None

    @model_validator(mode="after")
    def value_needs_source(self) -> "ExtractedValue":
        # Principle: every extracted value carries its source.
        if self.value is not None and self.source is None:
            raise ValueError("extracted value without source")
        return self


class Extraction(BaseModel):
    schema_version: str = SCHEMA_VERSION
    certificate_id: str  # internal id assigned at intake
    source_file: str
    reader: str | None = None  # model / pipeline version
    cost_eur: float | None = None  # compute cost for this certificate

    certificate_type: ExtractedValue | None = None  # expected "3.1"
    order_number: ExtractedValue | None = None
    manufacturer: ExtractedValue | None = None
    standard: ExtractedValue | None = None  # e.g. "EN 10025-2"
    grade: ExtractedValue | None = None  # e.g. "S355J2+N"
    batch_number: ExtractedValue | None = None  # heat / melt number (Schmelze)
    thickness_mm: ExtractedValue | None = None

    # keys: element symbols (C, Si, Mn, P, S, Cu, ...)
    chemistry: dict[str, ExtractedValue] = Field(default_factory=dict)
    # keys: ReH, Rm, A, KV
    mechanical: dict[str, ExtractedValue] = Field(default_factory=dict)


class OrderRecord(BaseModel):
    schema_version: str = SCHEMA_VERSION
    order_number: str
    supplier: str
    grade: str
    standard: str
    thickness_mm: float = Field(gt=0)
    certificate_type: str = "3.1"
    quantity_t: float | None = None


class Status(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class Finding(BaseModel):
    rule_id: str  # e.g. "chemistry.C", "grade.match"
    status: Status
    message: str  # human-readable reason, shown in review UI
    value: float | str | None = None
    limit: str | None = None  # e.g. "<= 0.20", "470..630"
    source: Source | None = None  # copied from the extracted value for the review UI


class CheckResult(BaseModel):
    schema_version: str = SCHEMA_VERSION
    certificate_id: str
    order_number: str
    verdict: Status
    findings: list[Finding]
