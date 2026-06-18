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
