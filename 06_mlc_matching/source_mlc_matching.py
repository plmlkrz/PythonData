# MODULE 6 - MLC-style matching and probabilistic QA
# Run: pytest 06_mlc_matching/source_mlc_matching.py -v
#
# Why this matters for MLC:
# Matching systems often do not return a simple yes/no answer. They may return
# a best candidate with a confidence score. QA needs to test thresholds,
# ambiguous matches, false positives, false negatives, and audit evidence.

from __future__ import annotations  # Allow lowercase type hints (list, dict) in older Python versions

import re  # Import re module for regular expression operations (used to strip punctuation)

import pytest  # Import pytest testing framework


ACCEPT_THRESHOLD = 0.90  # Scores at or above this are automatically accepted as a match
REVIEW_THRESHOLD = 0.70  # Scores at or above this (but below ACCEPT_THRESHOLD) go to manual review


def normalize_title(title: str) -> str:  # Function to clean a title string for consistent comparison
    """Normalize titles so punctuation/case do not block obvious matches."""
    if not isinstance(title, str):  # Guard: reject non-string input immediately
        raise TypeError("title must be a string")  # Raise TypeError with a clear message

    lowered = title.lower().strip()  # Convert to lowercase and remove leading/trailing whitespace
    without_punctuation = re.sub(r"[^a-z0-9\s]", " ", lowered)  # Replace any character that is not a letter, digit, or space with a space
    collapsed_spaces = re.sub(r"\s+", " ", without_punctuation)  # Collapse multiple consecutive spaces into a single space
    return collapsed_spaces.strip()  # Remove any trailing whitespace created by the substitutions and return


def classify_match(score: float) -> str:  # Function to convert a numeric score into a match status label
    """Classify a candidate match based on a confidence score."""
    if score < 0 or score > 1:  # Validate that the score is within the legal 0–1 range
        raise ValueError("score must be between 0 and 1")  # Raise ValueError if score is out of range

    if score >= ACCEPT_THRESHOLD:  # Check if score meets the auto-accept threshold
        return "auto_match"  # Return auto_match: high confidence, no human review needed
    if score >= REVIEW_THRESHOLD:  # Check if score meets the manual-review threshold
        return "manual_review"  # Return manual_review: moderate confidence, human should confirm
    return "no_match"  # Score is below both thresholds: usage record cannot be matched


def select_best_candidate(candidates: list[dict]) -> dict | None:  # Function to pick the top candidate from a list
    """
    Pick the highest-scoring candidate.

    Return None when there are no candidates. Raise ValueError when the top two
    candidates tie, because an ambiguous tie should not be auto-selected.
    """
    if not candidates:  # If the list is empty, there is nothing to select
        return None  # Return None: no candidates means no match is possible

    sorted_candidates = sorted(candidates, key=lambda c: c["score"], reverse=True)  # Sort candidates highest score first
    best = sorted_candidates[0]  # The first element after sorting is the highest-scoring candidate

    if len(sorted_candidates) > 1 and sorted_candidates[1]["score"] == best["score"]:  # Check if the second-best ties the best
        raise ValueError("ambiguous top match")  # Raise ValueError: a tie means ownership is uncertain and must not be auto-resolved

    enriched = best.copy()  # Shallow-copy the best candidate dict so we do not mutate the original input
    enriched["match_status"] = classify_match(best["score"])  # Add a match_status key based on the score
    return enriched  # Return the enriched candidate with its match_status attached


def build_audit_message(usage_record: dict, candidate: dict | None) -> str:  # Function to generate a human-readable audit note
    """Create a short human-readable audit note for match decisions."""
    isrc = usage_record.get("isrc", "unknown_isrc")  # Extract ISRC from usage record; fall back to a placeholder if missing
    title = usage_record.get("title", "unknown_title")  # Extract title from usage record; fall back to a placeholder if missing

    if candidate is None:  # If no candidate was returned (empty candidate list)
        return f"{isrc} / {title}: no candidates returned"  # Return a message explaining that no match attempt succeeded

    return (  # Otherwise build a full audit message that records the selected work and the decision details
        f"{isrc} / {title}: selected work_id={candidate['work_id']} "
        f"score={candidate['score']:.2f} status={candidate['match_status']}"  # Format score to 2 decimal places for readability
    )


# ─────────────────────────────────────────
# PYTEST TESTS
# ─────────────────────────────────────────

@pytest.mark.parametrize(  # Decorator: run the same test function with multiple sets of arguments
    "raw_title, expected",  # Names for the two parameters passed into each test case
    [
        ("Bohemian Rhapsody", "bohemian rhapsody"),          # Standard title: lowercase only
        ("  Bohemian   Rhapsody  ", "bohemian rhapsody"),    # Extra whitespace: should be collapsed and stripped
        ("Bohemian-Rhapsody!", "bohemian rhapsody"),         # Punctuation: hyphen and exclamation mark should become spaces
        ("SONG 2 (Live)", "song 2 live"),                    # Parentheses should be removed; digits preserved
    ],
)
def test_normalize_title(raw_title, expected):  # Test that normalize_title cleans titles correctly for each case
    assert normalize_title(raw_title) == expected  # Assert the normalized output matches the expected clean string


@pytest.mark.parametrize(  # Decorator: run classify_match with multiple score/status pairs
    "score, expected",  # Parameter names for score input and expected status string
    [
        (0.95, "auto_match"),    # Well above ACCEPT_THRESHOLD (0.90): should auto-match
        (0.90, "auto_match"),    # Exactly at ACCEPT_THRESHOLD: boundary — should auto-match
        (0.89, "manual_review"), # Just below ACCEPT_THRESHOLD but above REVIEW_THRESHOLD: manual review
        (0.70, "manual_review"), # Exactly at REVIEW_THRESHOLD: boundary — should be manual review
        (0.69, "no_match"),      # Just below REVIEW_THRESHOLD: should be no match
        (0.00, "no_match"),      # Minimum valid score: should be no match
    ],
)
def test_classify_match_thresholds(score, expected):  # Test that each score maps to the correct match status
    assert classify_match(score) == expected  # Assert classify_match returns the expected status string


@pytest.mark.parametrize("bad_score", [-0.01, 1.01])  # Test two invalid scores: one below 0 and one above 1
def test_classify_match_rejects_invalid_scores(bad_score):  # Test that out-of-range scores raise ValueError
    with pytest.raises(ValueError, match="between 0 and 1"):  # Expect a ValueError whose message contains "between 0 and 1"
        classify_match(bad_score)  # Call classify_match with the invalid score to trigger the error


def test_select_best_candidate_auto_match():  # Test that the highest-scoring candidate is selected and gets auto_match status
    candidates = [  # Set up three candidates with different scores
        {"work_id": "W1", "score": 0.68},   # Lowest score candidate
        {"work_id": "W2", "score": 0.94},   # Highest score candidate — should be selected
        {"work_id": "W3", "score": 0.81},   # Middle score candidate
    ]

    result = select_best_candidate(candidates)  # Call function to select best candidate

    assert result["work_id"] == "W2"             # Assert the highest-scoring work was selected
    assert result["match_status"] == "auto_match"  # Assert score 0.94 produces auto_match status


def test_select_best_candidate_manual_review():  # Test that a top score in the review band gets manual_review status
    candidates = [  # Set up two candidates both below ACCEPT_THRESHOLD
        {"work_id": "W1", "score": 0.72},   # Higher score — should be selected
        {"work_id": "W2", "score": 0.63},   # Lower score candidate
    ]

    result = select_best_candidate(candidates)  # Call function to select best candidate

    assert result["work_id"] == "W1"               # Assert the higher-scoring work was selected
    assert result["match_status"] == "manual_review"  # Assert score 0.72 produces manual_review status


def test_select_best_candidate_returns_none_for_no_candidates():  # Test that an empty candidate list returns None
    assert select_best_candidate([]) is None  # Assert None is returned when there are no candidates to evaluate


def test_select_best_candidate_rejects_ambiguous_tie():  # Test that two candidates with equal top scores raise ValueError
    candidates = [  # Set up two candidates with identical scores
        {"work_id": "W1", "score": 0.91},   # First candidate with top score
        {"work_id": "W2", "score": 0.91},   # Second candidate with identical score — creates an ambiguous tie
    ]

    with pytest.raises(ValueError, match="ambiguous"):  # Expect a ValueError whose message contains "ambiguous"
        select_best_candidate(candidates)  # Call function; it should raise because the tie cannot be auto-resolved


def test_build_audit_message_for_selected_candidate():  # Test that the audit message contains all key fields for a matched candidate
    usage_record = {"isrc": "US-S1Z-99-00001", "title": "Test Song"}  # Sample usage record with ISRC and title
    candidate = {"work_id": "W123", "score": 0.94, "match_status": "auto_match"}  # Sample matched candidate

    message = build_audit_message(usage_record, candidate)  # Build the audit message string

    assert "US-S1Z-99-00001" in message   # Assert the ISRC appears in the message so the record is identifiable
    assert "work_id=W123" in message      # Assert the selected work ID appears so reviewers know what was matched
    assert "score=0.94" in message        # Assert the score appears so confidence level is visible
    assert "status=auto_match" in message  # Assert the status appears so the decision type is recorded


def test_build_audit_message_for_no_candidates():  # Test that the audit message for a None candidate is informative
    usage_record = {"isrc": "US-S1Z-99-00002", "title": "Unknown Song"}  # Sample usage record that had no candidates

    assert build_audit_message(usage_record, None) == (  # Assert the exact message format for the no-candidates case
        "US-S1Z-99-00002 / Unknown Song: no candidates returned"  # Expected message: ISRC, title, and explanation
    )
