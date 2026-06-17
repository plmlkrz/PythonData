# MODULE 2a — The code under test (a simple royalty calculator)
# This is NOT a test file. It's the production code you will test.

class RoyaltyCalculator:
    """Calculate mechanical royalties for a batch of usage records."""

    STATUTORY_RATE = 0.091  # cents per stream (simplified)

    def __init__(self, rate: float = None):
        self.rate = rate if rate is not None else self.STATUTORY_RATE

    def calculate(self, plays: int) -> float:
        """Return royalty amount for a single track's play count."""
        if plays < 0:
            raise ValueError(f"Play count cannot be negative, got {plays}")
        return round(plays * self.rate, 4)

    def calculate_batch(self, records: list[dict]) -> list[dict]:
        """
        Accept a list of dicts with 'isrc' and 'plays'.
        Return the same list with a 'royalty' key added to each.
        """
        result = []
        for record in records:
            enriched = record.copy()
            enriched["royalty"] = self.calculate(record["plays"])
            result.append(enriched)
        return result

    def total(self, records: list[dict]) -> float:
        """Sum all royalties in a batch result."""
        return round(sum(r["royalty"] for r in records), 4)
