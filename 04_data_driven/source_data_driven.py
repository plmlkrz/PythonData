# MODULE 4 — Data-Driven Testing with pytest.mark.parametrize
# Run:  pytest 04_data_driven/source_data_driven.py -v
#
# KEY CONCEPTS:
#   - @pytest.mark.parametrize runs one test function with many inputs
#   - Test IDs make failures easy to read
#   - You can parametrize on fixtures too (indirect=True — advanced)
#   - Reading test cases from CSV or JSON keeps data separate from logic

import json
import csv
import pytest
from pathlib import Path

# The function under test — validate a usage record
def validate_usage_record(record: dict) -> list[str]:
    """
    Return a list of validation errors for a usage record.
    Empty list means the record is valid.
    """
    errors = []

    if not record.get("isrc"):
        errors.append("missing_isrc")

    if not isinstance(record.get("plays"), int) or record["plays"] < 0:
        errors.append("invalid_plays")

    if record.get("service") not in {"Spotify", "Apple Music", "Tidal", "YouTube Music"}:
        errors.append("unknown_service")

    return errors


# ─────────────────────────────────────────
# 1. INLINE PARAMETRIZE
#    Format: @pytest.mark.parametrize("arg1, arg2", [(val1, val2), ...])
# ─────────────────────────────────────────

@pytest.mark.parametrize("plays, expected_errors", [
    (0,          []),                     # zero is valid
    (1_000_000,  []),                     # large number is valid
    (-1,         ["invalid_plays"]),      # negative is invalid
    ("lots",     ["invalid_plays"]),      # wrong type is invalid
    (None,       ["invalid_plays"]),
])
def test_validate_plays(plays, expected_errors):
    record = {"isrc": "US-S1Z-99-00001", "plays": plays, "service": "Spotify"}
    errors = validate_usage_record(record)
    assert errors == expected_errors


@pytest.mark.parametrize("service, is_valid", [
    ("Spotify",       True),
    ("Apple Music",   True),
    ("Tidal",         True),
    ("YouTube Music", True),
    ("Napster",       False),
    ("",              False),
    (None,            False),
])
def test_validate_service(service, is_valid):
    record = {"isrc": "US-S1Z-99-00001", "plays": 100, "service": service}
    errors = validate_usage_record(record)
    if is_valid:
        assert "unknown_service" not in errors
    else:
        assert "unknown_service" in errors


# ─────────────────────────────────────────
# 2. PARAMETRIZE WITH CUSTOM TEST IDs
#    pytest.param(..., id="my-label")
# ─────────────────────────────────────────

@pytest.mark.parametrize("record, expected_error_count", [
    pytest.param(
        {"isrc": "US-001", "plays": 100, "service": "Spotify"},
        0,
        id="valid_record"
    ),
    pytest.param(
        {"isrc": "", "plays": -1, "service": "Napster"},
        3,
        id="all_fields_invalid"
    ),
    pytest.param(
        {"isrc": "US-001", "plays": 50, "service": "Unknown"},
        1,
        id="bad_service_only"
    ),
])
def test_validate_record_error_count(record, expected_error_count):
    errors = validate_usage_record(record)
    assert len(errors) == expected_error_count


# ─────────────────────────────────────────
# 3. LOADING TEST DATA FROM A JSON FILE
# ─────────────────────────────────────────

# First, write a helper to create the data file so this tutorial is self-contained.
def create_test_data_json(path: Path):
    data = [
        {"isrc": "US-001", "plays": 200,  "service": "Spotify",     "expect_valid": True},
        {"isrc": "US-002", "plays": 0,    "service": "Apple Music",  "expect_valid": True},
        {"isrc": "",       "plays": 100,  "service": "Tidal",        "expect_valid": False},
        {"isrc": "US-004", "plays": -10,  "service": "Spotify",      "expect_valid": False},
    ]
    path.write_text(json.dumps(data, indent=2))


DATA_FILE = Path(__file__).parent / "test_records.json"

# pytest collects parametrize at import time, so we create the file eagerly
if not DATA_FILE.exists():
    create_test_data_json(DATA_FILE)


def load_json_cases():
    records = json.loads(DATA_FILE.read_text())
    return [(r, r.pop("expect_valid")) for r in records]


@pytest.mark.parametrize("record, expect_valid", load_json_cases())
def test_records_from_json(record, expect_valid):
    errors = validate_usage_record(record)
    if expect_valid:
        assert errors == [], f"Expected valid but got errors: {errors}"
    else:
        assert errors != [], "Expected errors but record passed validation"


# ─────────────────────────────────────────
# 4. LOADING TEST DATA FROM A CSV FILE
# ─────────────────────────────────────────

def create_test_data_csv(path: Path):
    rows = [
        ["isrc",   "plays", "service",     "expect_valid"],
        ["US-001", "500",   "Spotify",     "true"],
        ["US-002", "-1",    "Spotify",     "false"],
        ["US-003", "0",     "BadService",  "false"],
    ]
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


CSV_FILE = Path(__file__).parent / "test_records.csv"
if not CSV_FILE.exists():
    create_test_data_csv(CSV_FILE)


def load_csv_cases():
    cases = []
    with CSV_FILE.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = {
                "isrc": row["isrc"],
                "plays": int(row["plays"]),
                "service": row["service"],
            }
            expect_valid = row["expect_valid"].lower() == "true"
            cases.append((record, expect_valid))
    return cases


@pytest.mark.parametrize("record, expect_valid", load_csv_cases())
def test_records_from_csv(record, expect_valid):
    errors = validate_usage_record(record)
    if expect_valid:
        assert errors == []
    else:
        assert errors != []
