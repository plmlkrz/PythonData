# MODULE 2b — pytest test suite for RoyaltyCalculator
# Run with:  pytest 02_pytest_basics/source_test_royalty_calculator.py -v
#
# KEY CONCEPTS:
#   - Test functions must start with  test_
#   - Use plain assert statements
#   - Fixtures (decorated with @pytest.fixture) set up shared state
#   - pytest.raises() asserts that an exception IS raised
#   - pytest.approx() compares floats without precision errors

import pytest  # Import pytest testing framework
from source_royalty_calculator import RoyaltyCalculator  # Import the class being tested


# ─────────────────────────────────────────
# FIXTURES  — reusable setup
# ─────────────────────────────────────────

@pytest.fixture  # Decorator: mark this function as a pytest fixture (setup/teardown helper)
def calculator():  # Fixture function: will be injected into test functions that request it
    """Return a RoyaltyCalculator at the default statutory rate."""
    return RoyaltyCalculator()  # Create and return a calculator instance


@pytest.fixture  # Decorator: mark this function as a pytest fixture
def sample_records():  # Fixture function: provides test data for batch operations
    """A small batch of usage records for batch-calculation tests."""
    return [  # Return a list of 3 test records
        {"isrc": "US-S1Z-99-00001", "plays": 1000},  # Record 1: 1000 plays
        {"isrc": "US-S1Z-99-00002", "plays": 500},   # Record 2: 500 plays
        {"isrc": "US-S1Z-99-00003", "plays": 0},     # Record 3: 0 plays (edge case)
    ]


# ─────────────────────────────────────────
# BASIC UNIT TESTS
# ─────────────────────────────────────────

def test_calculate_positive_plays(calculator):  # Test function: receives calculator fixture automatically
    result = calculator.calculate(1000)  # Call calculate with 1000 plays
    assert result == pytest.approx(91.0, rel=1e-3)  # Assert result equals ~91.0 (within 1e-3 relative tolerance)


def test_calculate_zero_plays(calculator):  # Test function for zero plays edge case
    assert calculator.calculate(0) == 0.0  # Assert that 0 plays returns exactly 0.0


def test_calculate_raises_on_negative_plays(calculator):  # Test that an exception is raised for negative plays
    with pytest.raises(ValueError, match="negative"):  # Expect ValueError with "negative" in the message
        calculator.calculate(-1)  # Call with negative plays (should raise ValueError)


def test_custom_rate():  # Test function: create calculator with custom rate (no fixture needed)
    calc = RoyaltyCalculator(rate=0.10)  # Create calculator with 10% rate
    assert calc.calculate(1000) == pytest.approx(100.0)  # Assert calculation returns ~100.0


# ─────────────────────────────────────────
# BATCH TESTS
# ─────────────────────────────────────────

def test_batch_adds_royalty_key(calculator, sample_records):  # Test that batch method adds "royalty" key to each record
    result = calculator.calculate_batch(sample_records)  # Call batch calculation
    for record in result:  # Loop through each record in results
        assert "royalty" in record  # Assert that "royalty" key exists in the record


def test_batch_does_not_mutate_input(calculator, sample_records):  # Test that original input list is not modified
    original_keys = set(sample_records[0].keys())  # Store original keys before batch processing
    calculator.calculate_batch(sample_records)  # Call batch calculation (should not modify input)
    assert set(sample_records[0].keys()) == original_keys  # Assert input keys haven't changed


def test_batch_royalty_values(calculator, sample_records):  # Test that calculated royalties are correct
    result = calculator.calculate_batch(sample_records)  # Call batch calculation
    assert result[0]["royalty"] == pytest.approx(91.0, rel=1e-3)    # Assert first record: 1000 × 0.091 ≈ 91.0
    assert result[1]["royalty"] == pytest.approx(45.5, rel=1e-3)    # Assert second record: 500 × 0.091 ≈ 45.5
    assert result[2]["royalty"] == 0.0  # Assert third record: 0 × 0.091 = 0.0


def test_batch_total(calculator, sample_records):  # Test that total() sums all royalties correctly
    result = calculator.calculate_batch(sample_records)  # Call batch calculation
    total = calculator.total(result)  # Call total() to sum royalties
    assert total == pytest.approx(136.5, rel=1e-3)  # Assert sum: 91.0 + 45.5 + 0.0 ≈ 136.5


# ─────────────────────────────────────────
# EDGE CASES
# ─────────────────────────────────────────

def test_very_large_play_count(calculator):  # Test with very large play count
    result = calculator.calculate(1_000_000_000)  # Calculate royalty for 1 billion plays
    assert result > 0  # Assert result is a positive number


def test_batch_empty_list(calculator):  # Test batch method with empty input
    result = calculator.calculate_batch([])  # Call batch with empty list
    assert result == []  # Assert returns empty list (not error)


def test_total_of_empty_batch(calculator):  # Test total() method with empty input
    assert calculator.total([]) == 0.0  # Assert total of empty list equals 0.0
