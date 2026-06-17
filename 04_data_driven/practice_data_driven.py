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
