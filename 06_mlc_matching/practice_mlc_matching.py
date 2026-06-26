# MODULE 6 - PRACTICE: reproduce the MLC-style matching module from memory.
#
# FUNCTIONS TO REPRODUCE:
#   normalize_title(title)
#     - lowercases
#     - trims whitespace
#     - removes punctuation
#     - collapses repeated spaces
#
#   classify_match(score)
#     - score >= 0.90 -> "auto_match"
#     - score >= 0.70 -> "manual_review"
#     - otherwise     -> "no_match"
#     - reject scores outside 0..1
#
#   select_best_candidate(candidates)
#     - return None for empty list
#     - sort candidates by score descending
#     - reject a tie for highest score as ambiguous
#     - add "match_status" to the returned best candidate
#
#   build_audit_message(usage_record, candidate)
#     - produce a short message showing ISRC, title, selected work_id, score,
#       and match status
#     - produce a separate message when no candidates were returned
#
# TESTS TO WRITE:
#   - normalization handles case, punctuation, and extra spaces
#   - threshold boundaries: 0.90, 0.89, 0.70, 0.69
#   - invalid scores raise ValueError
#   - best candidate is selected by score
#   - manual review is not auto-matched
#   - empty candidate list returns None
#   - tied top candidates raise ValueError
#   - audit messages include useful debugging evidence
#
# MLC INTERVIEW PREP:
#   Kalin specifically said Abel and Matthew may probe:
#     - matching workflows
#     - royalty-like data validation
#     - SQL reconciliation and defect investigation
#     - business-rule testing
#     - manual testing of complex workflows
#     - API testing
#     - Python ownership
#     - AWS/cloud exposure
#
#   As you write the tests, say out loud what business risk each test protects:
#     - A false positive can pay the wrong rightsholder.
#     - A false negative can leave valid usage unmatched and unpaid.
#     - A duplicate top score should not be auto-matched because ownership is
#       ambiguous.
#     - A manual_review result is not a failure; it is a controlled workflow
#       state for uncertain data.
#     - An audit message matters because QA, support, data science, and business
#       users need to understand why a matching outcome happened.
#
# INTERVIEW TALK TRACK:
#   "For a matching system, I would not only test the happy path. I would test
#   false positives, false negatives, threshold boundaries, ambiguous ties,
#   unmatched records, and whether the result leaves enough audit evidence for
#   a human to understand why the system made that decision."
#
# STRONGER VERSION FOR ABEL/MATTHEW:
#   "In a matching workflow, I would separate technical correctness from business
#   correctness. Technical correctness means the algorithm returns a score and a
#   candidate. Business correctness means the right usage record is connected to
#   the right work, uncertain matches are routed to review, no records disappear,
#   and there is enough evidence to explain the royalty outcome later."
#
# Write your code below.
from __future__ import annotations


import re


import pytest
#from pip._internal.models import candidate

ACCEPT_THRESHOLD = 0.90
REVIEW_THRESHOLD = 0.70


def normalize_title(title: str) -> str:
    if not isinstance(title, str):
        raise TypeError("Title must be a string")
    lowered = title.lower().strip()
    without_punctuation = re.sub(r"[^a-z0-9\s]", " ", lowered)
    collapsed_spaces = re.sub(r"\s+", " ", without_punctuation)
    return collapsed_spaces.strip()


def classify_match(score: float) -> str:
    if score < 0 or score > 1:
        raise ValueError("Score must be between 0 and 1")
    if score >= ACCEPT_THRESHOLD:
        return "auto-match"
    if score >= REVIEW_THRESHOLD:
        return "manual review"
    return "no match"


def select_best_candidate(candidates: list[dict]) -> dict | None:
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
    isrc = usage_record.get("isrc", "unknown_isrc")
    title = usage_record.get("title", "unknown title")

    if candidate is None:
        return f"{isrc} / {title}: no candidates returned"
    return (f"{isrc} / {title}: selected work_id={candidate['work_id']} "
            f"score={candidate['score']:.2f} status={candidate['match_status']}"
            )


# PYTEST TESTS

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
    assert result["match_status"] == "auto-match"


def test_select_best_candidate_manual_review():
    candidates = [
        {"work_id": "W1", "score": 0.72},
        {"work_id": "W2", "score": 0.63},
    ]
    result = select_best_candidate(candidates)
    assert result["work_id"] == "W1"
    assert result["match_status"] == "manual review"


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
    usage_records = {"isrc": "US-S1Z-99-00001", "title": "Test Song"}
    candidate = {"work_id": "W123", "score": 0.94, "match_status": "auto_match"}

    message = build_audit_message(usage_records, candidate)
    assert "US-S1Z-99-00001" in message
    assert "work_id=W123" in message
    assert "score=0.94" in message
    assert "status=auto_match" in message


def test_build_audit_message_for_no_candidates():
    usage_record = {"isrc": "US-S1Z-99-00002", "title": "Unknown Song"}
    assert build_audit_message(usage_record, None) == ("US-S1Z-99-00002 / Unknown Song: no candidates returned")
