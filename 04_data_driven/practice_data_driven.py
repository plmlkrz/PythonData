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
@pytest.mark.parametrize(["plays", "expected_errors"], [
    (0,          []),
    (1_000_000,  []),
    (-1,         ["invalid_plays"]),
    ("lots",     ["invalid_plays"]),
    (None,       ["invalid_plays"]),
    ])

def test_validate_plays(plays, expected_errors):
    record = {"isrc": "US-S1Z-99-00001", "plays": plays, "service": "Spotify"}
    errors = validate_usage_record(record)
    assert errors == expected_errors
