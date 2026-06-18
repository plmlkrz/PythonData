# MODULE 2a — The code under test (a simple royalty calculator)
# This is NOT a test file. It's the production code you will test.

class RoyaltyCalculator:  # Define a class to calculate royalties
    """Calculate mechanical royalties for a batch of usage records."""

    STATUTORY_RATE = 0.091  # Class constant: default royalty rate (9.1%)

    def __init__(self, rate: float = None):  # Constructor method: initialize the instance with an optional custom rate
        self.rate = rate if rate is not None else self.STATUTORY_RATE  # Set rate: use provided rate or default to statutory rate

    def calculate(self, plays: int) -> float:  # Method to calculate royalty for a single track
        """Return royalty amount for a single track's play count."""
        if plays < 0:  # Validate: check if play count is negative
            raise ValueError(f"Play count cannot be negative, got {plays}")  # Raise error if plays < 0
        return round(plays * self.rate, 4)  # Calculate royalty (plays × rate), round to 4 decimals, and return

    def calculate_batch(self, records: list[dict]) -> list[dict]:  # Method to process multiple records at once
        """
        Accept a list of dicts with 'isrc' and 'plays'.
        Return the same list with a 'royalty' key added to each.
        """
        result = []  # Initialize empty list to store results
        for record in records:  # Loop through each record in the input list
            enriched = record.copy()  # Create a shallow copy of the record (avoid mutating original)
            enriched["royalty"] = self.calculate(record["plays"])  # Calculate royalty and add it as new key
            result.append(enriched)  # Add enriched record to results list
        return result  # Return list of records with royalty values added

    def total(self, records: list[dict]) -> float:  # Method to sum all royalties in a batch
        """Sum all royalties in a batch result."""
        return round(sum(r["royalty"] for r in records), 4)  # Sum all "royalty" values, round to 4 decimals, and return
