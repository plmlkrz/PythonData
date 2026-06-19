# MODULE 2b — PRACTICE: reproduce the pytest test suite from memory.
#
# WHAT TO WRITE:
#   Imports: pytest, RoyaltyCalculator (from your practice file)
#
#   Fixtures:
#     - calculator()        — returns RoyaltyCalculator()
#     - sample_records()    — returns list of 3 dicts with isrc + plays
#
#   Tests:
#     - test_calculate_positive_plays      (use pytest.approx)
#     - test_calculate_zero_plays
#     - test_calculate_raises_on_negative_plays   (use pytest.raises)
#     - test_custom_rate
#     - test_batch_adds_royalty_key
#     - test_batch_does_not_mutate_input
#     - test_batch_royalty_values
#     - test_batch_total
#     - test_very_large_play_count
#     - test_batch_empty_list
#     - test_total_of_empty_batch
#
# Write your code below.
# ─────────────────────────────────────────────────────────────────────────────
import pytest
from practice_royalty_calculator import RoyaltyCalculator

# Fixtures
@pytest.fixture
def calculator():
    return RoyaltyCalculator()

@pytest.fixture
def sample_records():
    return [
        {"isrc": "US-S1Z-99-00001", "plays": 1000},
        {"isrc": "US-S1Z-99-00002", "plays": 500},
        {"isrc": "US-S1Z-99-00003", "plays": 0},
    ]

# Basic Unit Tests
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

#Batch Tests

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

#Edge Cases

def test_very_large_play_count(calculator):
    result = calculator.calculate(1_000_000_000)
    assert result > 0

def test_batch_empty_list(calculator):
    result = calculator.calculate_batch([])
    assert result == []

def test_total_of_empty_batch(calculator):
    assert calculator.total([]) == 0.0