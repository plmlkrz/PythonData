# MODULE 4 — Data-Driven Testing with pytest.mark.parametrize
# Run:  pytest 04_data_driven/source_data_driven.py -v
#
# KEY CONCEPTS:
#   - @pytest.mark.parametrize runs one test function with many inputs
#   - Test IDs make failures easy to read
#   - You can parametrize on fixtures too (indirect=True — advanced)
#   - Reading test cases from CSV or JSON keeps data separate from logic

import json  # Import json module for reading JSON files
import csv  # Import csv module for reading CSV files
import pytest  # Import pytest testing framework
from pathlib import Path  # Import Path for file path operations

# The function under test — validate a usage record
def validate_usage_record(record: dict) -> list[str]:  # Function that returns list of validation error messages (empty if valid)
    """
    Return a list of validation errors for a usage record.
    Empty list means the record is valid.
    """
    errors = []  # Initialize empty list to collect error messages

    if not record.get("isrc"):  # Check if "isrc" key exists and has a truthy value
        errors.append("missing_isrc")  # Add error if isrc is missing or empty

    if not isinstance(record.get("plays"), int) or record["plays"] < 0:  # Check if plays is integer AND >= 0
        errors.append("invalid_plays")  # Add error if plays is wrong type or negative

    if record.get("service") not in {"Spotify", "Apple Music", "Tidal", "YouTube Music"}:  # Check if service is valid
        errors.append("unknown_service")  # Add error if service not in approved list

    return errors  # Return list of errors (empty if all validations pass)


# ─────────────────────────────────────────
# 1. INLINE PARAMETRIZE
#    Format: @pytest.mark.parametrize("arg1, arg2", [(val1, val2), ...])
# ─────────────────────────────────────────

@pytest.mark.parametrize("plays, expected_errors", [  # Parametrize decorator: run test once for each (plays, expected_errors) tuple
    (0,          []),                     # Test case 1: zero plays should have no errors
    (1_000_000,  []),                     # Test case 2: large number should have no errors
    (-1,         ["invalid_plays"]),      # Test case 3: negative plays should error
    ("lots",     ["invalid_plays"]),      # Test case 4: string plays should error
    (None,       ["invalid_plays"]),      # Test case 5: None plays should error
])
def test_validate_plays(plays, expected_errors):  # Test function receives plays and expected_errors from parametrize
    record = {"isrc": "US-S1Z-99-00001", "plays": plays, "service": "Spotify"}  # Create test record with given plays
    errors = validate_usage_record(record)  # Call validation function
    assert errors == expected_errors  # Assert returned errors match expected


@pytest.mark.parametrize("service, is_valid", [  # Parametrize: run test once for each (service, is_valid) tuple
    ("Spotify",       True),              # Test case 1: Spotify is valid
    ("Apple Music",   True),              # Test case 2: Apple Music is valid
    ("Tidal",         True),              # Test case 3: Tidal is valid
    ("YouTube Music", True),              # Test case 4: YouTube Music is valid
    ("Napster",       False),             # Test case 5: Napster not in approved list
    ("",              False),             # Test case 6: empty string is invalid
    (None,            False),             # Test case 7: None is invalid
])
def test_validate_service(service, is_valid):  # Test function receives service and is_valid from parametrize
    record = {"isrc": "US-S1Z-99-00001", "plays": 100, "service": service}  # Create test record with given service
    errors = validate_usage_record(record)  # Call validation function
    if is_valid:  # If service is valid
        assert "unknown_service" not in errors  # Assert no unknown_service error
    else:  # If service is invalid
        assert "unknown_service" in errors  # Assert unknown_service error is present


# ─────────────────────────────────────────
# 2. PARAMETRIZE WITH CUSTOM TEST IDs
#    pytest.param(..., id="my-label")
# ─────────────────────────────────────────

@pytest.mark.parametrize("record, expected_error_count", [  # Parametrize with custom test IDs
    pytest.param(  # Use pytest.param() for custom ID
        {"isrc": "US-001", "plays": 100, "service": "Spotify"},  # Test data
        0,  # Expected error count
        id="valid_record"  # Custom test ID (shows in pytest output instead of tuple)
    ),
    pytest.param(  # Use pytest.param() for custom ID
        {"isrc": "", "plays": -1, "service": "Napster"},  # All fields invalid
        3,  # Expected 3 errors
        id="all_fields_invalid"  # Custom test ID
    ),
    pytest.param(  # Use pytest.param() for custom ID
        {"isrc": "US-001", "plays": 50, "service": "Unknown"},  # Only service is invalid
        1,  # Expected 1 error
        id="bad_service_only"  # Custom test ID
    ),
])
def test_validate_record_error_count(record, expected_error_count):  # Test function receives record and expected_error_count
    errors = validate_usage_record(record)  # Call validation function
    assert len(errors) == expected_error_count  # Assert number of errors matches expected


# ─────────────────────────────────────────
# 3. LOADING TEST DATA FROM A JSON FILE
# ─────────────────────────────────────────

# First, write a helper to create the data file so this tutorial is self-contained.
def create_test_data_json(path: Path):  # Helper function to create JSON test data file
    data = [  # Create list of test records
        {"isrc": "US-001", "plays": 200,  "service": "Spotify",     "expect_valid": True},  # Valid record
        {"isrc": "US-002", "plays": 0,    "service": "Apple Music",  "expect_valid": True},  # Valid record
        {"isrc": "",       "plays": 100,  "service": "Tidal",        "expect_valid": False},  # Invalid (no isrc)
        {"isrc": "US-004", "plays": -10,  "service": "Spotify",      "expect_valid": False},  # Invalid (negative plays)
    ]
    path.write_text(json.dumps(data, indent=2))  # Write data as formatted JSON to file


DATA_FILE = Path(__file__).parent / "test_records.json"  # Define path to test data file in same directory

# pytest collects parametrize at import time, so we create the file eagerly
if not DATA_FILE.exists():  # Check if file doesn't exist
    create_test_data_json(DATA_FILE)  # Create it


def load_json_cases():  # Helper function to load and parse JSON test cases
    records = json.loads(DATA_FILE.read_text())  # Read JSON file and parse into list of dicts
    return [(r, r.pop("expect_valid")) for r in records]  # Return list of (record, expect_valid) tuples


@pytest.mark.parametrize("record, expect_valid", load_json_cases())  # Parametrize with test cases loaded from JSON
def test_records_from_json(record, expect_valid):  # Test function receives record and expect_valid from JSON
    errors = validate_usage_record(record)  # Call validation function
    if expect_valid:  # If record should be valid
        assert errors == [], f"Expected valid but got errors: {errors}"  # Assert no errors
    else:  # If record should be invalid
        assert errors != [], "Expected errors but record passed validation"  # Assert errors exist


# ─────────────────────────────────────────
# 4. LOADING TEST DATA FROM A CSV FILE
# ─────────────────────────────────────────

def create_test_data_csv(path: Path):  # Helper function to create CSV test data file
    rows = [  # Create list of rows
        ["isrc",   "plays", "service",     "expect_valid"],  # Header row
        ["US-001", "500",   "Spotify",     "true"],          # Valid record
        ["US-002", "-1",    "Spotify",     "false"],         # Invalid (negative plays)
        ["US-003", "0",     "BadService",  "false"],         # Invalid (unknown service)
    ]
    with path.open("w", newline="") as f:  # Open file for writing (newline="" for CSV compatibility)
        writer = csv.writer(f)  # Create CSV writer
        writer.writerows(rows)  # Write all rows to CSV file


CSV_FILE = Path(__file__).parent / "test_records.csv"  # Define path to CSV test data file
if not CSV_FILE.exists():  # Check if file doesn't exist
    create_test_data_csv(CSV_FILE)  # Create it


def load_csv_cases():  # Helper function to load and parse CSV test cases
    cases = []  # Initialize empty list for test cases
    with CSV_FILE.open() as f:  # Open CSV file
        reader = csv.DictReader(f)  # Create CSV reader that returns dicts with column names as keys
        for row in reader:  # Loop through each row
            record = {  # Create record dict for validation
                "isrc": row["isrc"],  # Get isrc value from CSV
                "plays": int(row["plays"]),  # Get plays value and convert to integer
                "service": row["service"],  # Get service value from CSV
            }
            expect_valid = row["expect_valid"].lower() == "true"  # Convert string "true"/"false" to boolean
            cases.append((record, expect_valid))  # Add (record, expect_valid) tuple to list
    return cases  # Return list of test cases


@pytest.mark.parametrize("record, expect_valid", load_csv_cases())  # Parametrize with test cases loaded from CSV
def test_records_from_csv(record, expect_valid):  # Test function receives record and expect_valid from CSV
    errors = validate_usage_record(record)  # Call validation function
    if expect_valid:  # If record should be valid
        assert errors == []  # Assert no errors
    else:  # If record should be invalid
        assert errors != []  # Assert errors exist
