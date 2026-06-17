# MODULE 2b — pytest test suite for RoyaltyCalculator
# Run with:  pytest 02_pytest_basics/source_test_royalty_calculator.py -v
#
# KEY CONCEPTS:
#   - Test functions must start with  test_
#   - Use plain assert statements
#   - Fixtures (decorated with @pytest.fixture) set up shared state
#   - pytest.raises() asserts that an exception IS raised
#   - pytest.approx() compares floats without precision errors

import pytest
from source_royalty_calculator import RoyaltyCalculator


# ─────────────────────────────────────────
# FIXTURES  — reusable setup
# ─────────────────────────────────────────

@pytest.fixture
def calculator():
    """Return a RoyaltyCalculator at the default statutory rate."""
    return RoyaltyCalculator()


@pytest.fixture
def sample_records():
    """A small batch of usage records for batch-calculation tests."""
    return [
        {"isrc": "US-S1Z-99-00001", "plays": 1000},
        {"isrc": "US-S1Z-99-00002", "plays": 500},
        {"isrc": "US-S1Z-99-00003", "plays": 0},
    ]


# ─────────────────────────────────────────
# BASIC UNIT TESTS
# ─────────────────────────────────────────

def test_calculate_positive_plays(calculator):
    result = calculator.calculate(1000)
    assert result == pytest.approx(91.0, rel=1e-3)


def test_calculate_zero_plays(calculator):
    assert calculator.calculate(0) == 0.0


def test_calculate_raises_on_negative_plays(calculator):
    with pytest.raises(ValueError, match="negative"):
        calculator.calculate(-1)


def test_custom_rate():
    calc = RoyaltyCalculator(rate=0.10)
    assert calc.calculate(1000) == pytest.approx(100.0)


# ─────────────────────────────────────────
# BATCH TESTS
# ─────────────────────────────────────────

def test_batch_adds_royalty_key(calculator, sample_records):
    result = calculator.calculate_batch(sample_records)
    for record in result:
        assert "royalty" in record


def test_batch_does_not_mutate_input(calculator, sample_records):
    original_keys = set(sample_records[0].keys())
    calculator.calculate_batch(sample_records)
    assert set(sample_records[0].keys()) == original_keys


def test_batch_royalty_values(calculator, sample_records):
    result = calculator.calculate_batch(sample_records)
    assert result[0]["royalty"] == pytest.approx(91.0, rel=1e-3)
    assert result[1]["royalty"] == pytest.approx(45.5, rel=1e-3)
    assert result[2]["royalty"] == 0.0


def test_batch_total(calculator, sample_records):
    result = calculator.calculate_batch(sample_records)
    total = calculator.total(result)
    assert total == pytest.approx(136.5, rel=1e-3)


# ─────────────────────────────────────────
# EDGE CASES
# ─────────────────────────────────────────

def test_very_large_play_count(calculator):
    result = calculator.calculate(1_000_000_000)
    assert result > 0


def test_batch_empty_list(calculator):
    result = calculator.calculate_batch([])
    assert result == []


def test_total_of_empty_batch(calculator):
    assert calculator.total([]) == 0.0
