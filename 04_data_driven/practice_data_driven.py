# MODULE 4 — PRACTICE: reproduce the data-driven test file from memory.
#
# FUNCTION TO TEST: validate_usage_record(record: dict) -> list[str]
#   Returns a list of error strings:
#     "missing_isrc"    if isrc is falsy
#     "invalid_plays"   if plays is not a non-negative int
#     "unknown_service" if service not in the allowed set
#
# SECTIONS TO REPRODUCE:
#
#   1. validate_usage_record() — the function itself
#
#   2. Inline parametrize — test plays values (0, large, -1, "lots", None)
#
#   3. Inline parametrize — test service names (valid and invalid)
#
#   4. Parametrize with pytest.param(..., id="label") — test full records
#      with known error counts
#
#   5. Load from JSON — create_test_data_json(), load_json_cases(),
#      parametrized test
#
#   6. Load from CSV  — create_test_data_csv(), load_csv_cases(),
#      parametrized test
#
# Write your code below.
# ─────────────────────────────────────────────────────────────────────────────
import json
import csv
import pytest
from pathlib import Path


def validate_usage_record(record: dict) -> list[str]:
    errors = []
    if not record.get("isrc"):
        errors.append("missing_isrc")

    if not isinstance(record.get("plays"), int) or record["plays"] < 0:
        errors.append("invalid_plays")

    if record.get("service") not in {"Spotify", "Apple Music", "Tidal", "YouTube Music"}:
        errors.append("invalid_service")

    return errors


# 1. INLINE PARAMETRIZE
@pytest.mark.parametrize("plays", "expected_errors", [
    (0, []),
    (1_000_000, []),
    (-1, ["invalid_plays"]),
    ("lots", ["invalid_plays"]),
    (None, ["invalid_plays"]),
])
def test_validate_plays(plays, expected_errors):
    record = {"isrc": "US-S1Z-99-00001", "plays": plays, "service": "Spotify"}
    errors = validate_usage_record(record)
    assert errors == expected_errors


@pytest.mark.parametrize("service", "is_valid", [
    ("Spotify", True),
    ("Apple Music", True),
    ("Tidal", True),
    ("YouTube Music", True),
    ("Napster", False),
    ("", False),
    (None, False),
])
def test_validate_service(service, is_valid):
    record = {"isrc": "US-S1Z-99-00001", "plays": 100, "service": service}
    errors = validate_usage_record(record)
    if is_valid:
        assert "unknown_service" not in errors
    else:
        assert "unknown_service" in errors


# 2. PARAMETRIZE WITH CUSTOM TEST IDs

@pytest.mark.parametrize("record, expected_error_count", [
    pytest.param({"isrc": "US-001", "plays": 100, "service": "Spotify"}, 0, id="valid_record"),
    pytest.param({"isrc": "", "plays": -1, "service": "Napster"}, 3, id="all_fields_invalid"),
    pytest.param({"isrc": "US-001", "plays": 50, "service": "Unknown"}, 1, id="bad_service_only"),
])
def test_validate_record_error_count(record, expected_error_count):
    errors = validate_usage_record(record)
    assert len(errors) == expected_error_count


# 3. LOADING TEST DATA FROM A JSON FILE

def create_test_data_json(path: Path):
    data = [
        {"isrc": "US-001", "plays": 200, "service": "Spotify", "expect_valid": True},
        {"isrc": "US-002", "plays": 0, "service": "Apple Music", "expect_valid": True},
        {"isrc": "", "plays": 100, "service": "Tidal", "expect_valid": False},
        {"isrc": "US-004", "plays": -10, "service": "Spotify", "expect_valid": False},
    ]
    path.write_text(json.dumps(data, indent=2))


DATA_FILE = Path(__file__).parent / "test_records.json"

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
        assert errors != [], f"Expected errors but record passed validation"


# 4. LOADING TEST DATA FROM A CSV FILE

def create_test_data_csv(path: Path):
    rows = [
        ["isrc", "plays", "service", "expect_valid"],
        ["US-001", "500", "Spotify", "true"],
        ["US-002", "-1", "Spotify", "false"],
        ["US-003", "0", "BadService", "false"],
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
