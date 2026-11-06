import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from schema import SCHEMA_VERSION, CheckResult, ExtractedValue, Extraction, OrderRecord

EXAMPLES = Path(__file__).parents[2] / "schema" / "examples"
MODELS = {"extraction.json": Extraction, "order.json": OrderRecord, "check_result.json": CheckResult}


@pytest.mark.parametrize("name", MODELS)
def test_example_is_valid(name: str):
    data = json.loads((EXAMPLES / name).read_text(encoding="utf-8"))
    obj = MODELS[name].model_validate(data)
    assert obj.schema_version == SCHEMA_VERSION


def test_value_without_source_is_rejected():
    with pytest.raises(ValidationError):
        ExtractedValue(value=0.17, confidence=0.9)


def test_empty_value_may_have_no_source():
    ExtractedValue(value=None, confidence=0.0)
