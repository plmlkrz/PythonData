# MODULE 2a — PRACTICE: reproduce the RoyaltyCalculator class from memory.
#
# CLASS: RoyaltyCalculator
#   - class attribute: STATUTORY_RATE = 0.091
#   - __init__(self, rate=None)   — use STATUTORY_RATE if none given
#   - calculate(self, plays: int) -> float   — raise ValueError if plays < 0
#   - calculate_batch(self, records: list[dict]) -> list[dict]   — adds 'royalty' key
#   - total(self, records: list[dict]) -> float   — sums 'royalty' values
#
# Write your code below.
# ─────────────────────────────────────────────────────────────────────────────
class RoyalCalculator:
    STATUTORY_RATE = 0.091
    def __init__(self, rate: float = None):
       self.rate = rate if rate is not None else self.STATUTORY_RATE

    def calculate(self, plays: int) -> float:
        if plays < 0:
            raise ValueError(f"Play count cannot be negative, got {plays} ")
        return round(plays * self.rate, 4)

    def calculate_batch(self, records: list[dict]) -> list[dict]:
        result = []
        for record in records:
            enriched = record.copy()
            enriched["royalty"] = self.calculate(record["plays"])
            result.append(enriched)
        return result

    def total(self, records: list[dict]) -> float:
        return round(sum(r["royalty"] for r in records), 4)

