# MODULE 6 - MLC-style matching and probabilistic QA
# Run: pytest 06_mlc_matching/source_mlc_matching.py -v
#
# Why this matters for MLC:
# Matching systems often do not return a simple yes/no answer. They may return
# a best candidate with a confidence score. QA needs to test thresholds,
# ambiguous matches, false positives, false negatives, and audit evidence.

from __future__ import annotations

import re

import pytest


ACCEPT_THRESHOLD = 0.90
REVIEW_THRESHOLD = 0.70


def normalize_title(title: str) -> str:
    """Normalize titles so punctuation/case do not block obvious matches."""
    if not isinstance(title, str):
        raise TypeError("title must be a string")

    lowered = title.lower().strip()
    without_punctuation = re.sub(r"[^a-z0-9\s]", " ", lowered)
    collapsed_spaces = re.sub(r"\s+", " ", without_punctuation)
    return collapsed_spaces.strip()


def classify_match(score: float) -> str:
    """Classify a candidate match based on a confidence score."""
    if score < 0 or score > 1:
        raise ValueError("score must be between 0 and 1")

    if score >= ACCEPT_THRESHOLD:
        return "auto_match"
    if score >= REVIEW_THRESHOLD:
        return "manual_review"
    return "no_match"


def select_best_candidate(candidates: list[dict]) -> dict | None:
    """
    Pick the highest-scoring candidate.

    Return None when there are no candidates. Raise ValueError when the top two
    candidates tie, because an ambiguous tie should not be auto-selected.
    """
    if not candidates:
        return None

    sorted_candidates = sorted(candidates, key=lambda c: c["score"], reverse=True)
    best = sorted_candidates[0]

    if len(sorted_candidates) > 1 and sorted_candidates[1]["score"] == best["score"]:
        raise ValueError("ambiguous top match")

    enriched = best.copy()
    enriched["match_status"] = classify_match(best["score"])
    return enriched


def build_audit_message(usage_record: dict, candidate: dict | None) -> str:
    """Create a short human-readable audit note for match decisions."""
    isrc = usage_record.get("isrc", "unknown_isrc")
    title = usage_record.get("title", "unknown_title")

    if candidate is None:
        return f"{isrc} / {title}: no candidates returned"

    return (
        f"{isrc} / {title}: selected work_id={candidate['work_id']} "
        f"score={candidate['score']:.2f} status={candidate['match_status']}"
    )


@pytest.mark.parametrize(
    "raw_title, expected",
    [
        ("Bohemian Rhapsody", "bohemian rhapsody"),
        ("  Bohemian   Rhapsody  ", "bohemian rhapsody"),
        ("Bohemian-Rhapsody!", "bohemian rhapsody"),
        ("SONG 2 (Live)", "song 2 live"),
    ],
)
def test_normalize_title(raw_title, expected):
    assert normalize_title(raw_title) == expected


@pytest.mark.parametrize(
    "score, expected",
    [
        (0.95, "auto_match"),
        (0.90, "auto_match"),
        (0.89, "manual_review"),
        (0.70, "manual_review"),
        (0.69, "no_match"),
        (0.00, "no_match"),
    ],
)
def test_classify_match_thresholds(score, expected):
    assert classify_match(score) == expected


@pytest.mark.parametrize("bad_score", [-0.01, 1.01])
def test_classify_match_rejects_invalid_scores(bad_score):
    with pytest.raises(ValueError, match="between 0 and 1"):
        classify_match(bad_score)


def test_select_best_candidate_auto_match():
    candidates = [
        {"work_id": "W1", "score": 0.68},
        {"work_id": "W2", "score": 0.94},
        {"work_id": "W3", "score": 0.81},
    ]

    result = select_best_candidate(candidates)

    assert result["work_id"] == "W2"
    assert result["match_status"] == "auto_match"


def test_select_best_candidate_manual_review():
    candidates = [
        {"work_id": "W1", "score": 0.72},
        {"work_id": "W2", "score": 0.63},
    ]

    result = select_best_candidate(candidates)

    assert result["work_id"] == "W1"
    assert result["match_status"] == "manual_review"


def test_select_best_candidate_returns_none_for_no_candidates():
    assert select_best_candidate([]) is None


def test_select_best_candidate_rejects_ambiguous_tie():
    candidates = [
        {"work_id": "W1", "score": 0.91},
        {"work_id": "W2", "score": 0.91},
    ]

    with pytest.raises(ValueError, match="ambiguous"):
        select_best_candidate(candidates)


def test_build_audit_message_for_selected_candidate():
    usage_record = {"isrc": "US-S1Z-99-00001", "title": "Test Song"}
    candidate = {"work_id": "W123", "score": 0.94, "match_status": "auto_match"}

    message = build_audit_message(usage_record, candidate)

    assert "US-S1Z-99-00001" in message
    assert "work_id=W123" in message
    assert "score=0.94" in message
    assert "status=auto_match" in message


def test_build_audit_message_for_no_candidates():
    usage_record = {"isrc": "US-S1Z-99-00002", "title": "Unknown Song"}

    assert build_audit_message(usage_record, None) == (
        "US-S1Z-99-00002 / Unknown Song: no candidates returned"
    )
