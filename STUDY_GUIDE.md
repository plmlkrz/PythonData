# Python QA Interview Study Guide - The MLC

## Setup

```powershell
pip install -r requirements.txt
```

## How To Use This Project

1. Open the `source_` file for a module. Read it carefully.
2. Close it or minimize it so you cannot peek.
3. Open the matching `practice_` file. Reproduce the code from memory.
4. Return to the source and compare. Note what you missed.
5. Repeat until you can explain the code and write the important parts cleanly.

## Modules

| # | Topic | Source file | Run with |
|---|---|---|---|
| 1 | Python basics | `01_python_basics/source_01_basics.py` | `python 01_python_basics/source_01_basics.py` |
| 2 | pytest + fixtures | `02_pytest_basics/source_test_royalty_calculator.py` | `pytest 02_pytest_basics/source_test_royalty_calculator.py -v` |
| 3 | API testing | `03_api_testing/source_api_tests.py` | `pytest 03_api_testing/source_api_tests.py -v` |
| 4 | Data-driven testing | `04_data_driven/source_data_driven.py` | `pytest 04_data_driven/source_data_driven.py -v` |
| 5 | SQL with Python | `05_sql_with_python/source_sql_basics.py` | `pytest 05_sql_with_python/source_sql_basics.py -v` |
| 6 | MLC-style matching | `06_mlc_matching/source_mlc_matching.py` | `pytest 06_mlc_matching/source_mlc_matching.py -v` |

## MLC JD Coverage

| JD signal | Covered in |
|---|---|
| Python proficiency | Modules 1-6 |
| Automated tests with pytest | Modules 2, 4, 5, 6 |
| API testing | Module 3 |
| Data-driven/workflow systems | Modules 4, 5, 6 |
| SQL proficiency | Module 5 |
| Testing frameworks from scratch | Module 2 |
| Matching/probabilistic systems | Module 6 |
| Edge-case thinking | All modules |

## Kalin's Interview Rubric

This next round is not just a Python syntax check. Abel Sayago and Matthew
Cintron are likely validating whether you have truly tested data-heavy systems
where correctness affects payment, ownership, or downstream business outcomes.

| Topic Kalin named | What to prove | Best prep module |
|---|---|---|
| Matching workflows | You understand exact matches, fuzzy matches, unmatched data, ambiguous candidates, and manual review routing. | Module 6 |
| Royalty-like data validation | You can explain financial/transactional correctness: the right amount, party, rule, state, and audit trail. | Modules 5, 6 |
| SQL validation and reconciliation | You can use SQL to compare expected vs actual records, investigate defects, and isolate source of error. | Module 5 |
| Business-rule testing | You test outcomes, not just screens: eligibility, thresholds, calculations, exceptions, and state changes. | Modules 4, 5, 6 |
| Manual testing of complex workflows | You know when exploratory/manual review is necessary before automation exists or when edge cases are subtle. | Module 6 |
| API testing | You validate status, schema, payload fields, negative paths, and downstream data impact. | Module 3 |
| Python and automation ownership | You can build clear pytest coverage and explain why each test exists. | Modules 2, 4, 6 |
| AWS/cloud exposure | You can speak to environment validation, logs, data movement, permissions, and release confidence without overselling cloud depth. | Talk track below |

## Primary Interview Thesis

Use this as the thread through the interview:

> My strength is testing systems where correctness is not just whether the UI
> works, but whether the data, business rules, workflows, and downstream
> outcomes are right.

For MLC, translate that into:

- Is the music usage record connected to the correct work?
- Is the confidence score handled correctly?
- Are uncertain matches routed to human review?
- Are unmatched records visible instead of silently lost?
- Can we explain why a royalty/payment outcome happened?
- Can SQL prove that the data landed in the right state?

## Story Bank

Prepare these stories before the interview. Keep each one to 60-90 seconds
unless they ask for detail.

| Story | Use it when they ask about | Core point |
|---|---|---|
| Oasys Mobile | Small company, no QA team, building QA from scratch, manual workflow coverage | You can create QA structure where none exists. |
| Credit Suisse / First Citizens | Financial systems, data correctness, reconciliation, SQL investigation | You understand accuracy, auditability, and transactional risk. |
| Kroger | Automation ownership, AI-assisted QA, improving regression coverage | You can modernize QA and reduce regression risk with measurable impact. |
| SQL defect investigation | SQL depth, data validation, proving root cause | You use queries to determine whether the defect is UI, API, database, or business logic. |
| Matching workflow design | MLC-specific quality thinking | You test false positives, false negatives, thresholds, ambiguous ties, unmatched records, and audit evidence. |

## Interview Talk Tracks

- "I write pytest tests with fixtures for shared setup, parametrize for data-driven cases, and pytest.raises for expected exceptions."

- "I validate APIs by checking status code, response structure, required fields, data types, and negative/error behavior."

- "For SQL testing, I validate source-to-target movement, joins, filters, aggregations, missing records, duplicates, and business-rule outcomes. SQL helps me prove whether the data is wrong, the workflow is wrong, or the display is wrong."

- "For matching systems, I test threshold boundaries, false positives, false negatives, ambiguous ties, no-candidate cases, and audit evidence so a human can understand why the system made a decision."

- "My strongest QA value is not just writing scripts. It is deciding what should be automated, what should be manually reviewed, and where data quality creates release or payment risk."

- "For royalty-like validation, I think in terms of right record, right owner or party, right rule, right amount or status, and right audit trail. The question is not only whether a test passes, but whether the business outcome is defensible."

- "For manual testing of complex workflows, I start by mapping the key states and handoffs, then identify the cases most likely to break: missing data, duplicates, boundary conditions, exception handling, and downstream reconciliation."

- "For AWS, I would be honest that I am not positioning myself as a cloud engineer. My QA concern is whether the cloud-hosted system is testable and observable: environment configuration, data movement, permissions, logs, repeatable deployments, and evidence when something fails."

## Likely Interview Questions

| Question | What they are testing | Answer angle |
|---|---|---|
| What do you mean by royalty-like data validation? | Whether your resume phrase is real experience or just wording. | Explain financial/transactional correctness: right record, right party, right calculation/status, right audit trail. |
| How have you used SQL in QA? | Hands-on depth. | Talk about reconciliation, joins, missing/duplicate records, defect isolation, and proving expected vs actual. |
| How would you test a matching workflow? | MLC fit. | Exact match, fuzzy match, no match, duplicate candidates, threshold boundaries, false positives/negatives, manual review, audit message. |
| When would you choose manual testing over automation? | Judgment. | Early workflow discovery, complex exception paths, low-stability areas, and human-review behavior before automating repeatable checks. |
| Tell us about owning automation. | Whether you can work solo. | Use Oasys/Kroger: start with risk, define coverage, build maintainable tests, show results. |
| How deep is your Python? | Gap validation. | Be honest: deepest production is Java/Selenium/API/SQL; actively sharpening Python/pytest for this data QA role. |
| How would you investigate a data correctness defect? | Debugging mindset. | Reproduce, identify source record, trace API/workflow/database state, query expected vs actual, isolate rule or data issue, document evidence. |

## Suggested Practice Plan Before June 25

**Day 1:** Module 2 - pytest fixtures, raises, approx, batch processing.  
**Day 2:** Module 4 - parametrize, JSON/CSV data-driven cases.  
**Day 3:** Module 5 - SQLite schema, seed data, joins, group by, parameterized queries.  
**Day 4:** Module 6 - matching thresholds, ambiguity handling, audit messages.  
**Day 5:** Mock interview: answer Kalin's eight topics out loud using the story bank.  
**Day 6:** Cold run: open only the practice files and write as much as you can in 60-90 minutes. Then do a 15-minute verbal walkthrough of how you would test MLC's matching workflow.

## What To Say If Asked About Python Depth

Use honest ramp language:

> My deepest production automation background is Selenium/Java, Cucumber/BDD, UFT, API testing, and SQL validation. I have been actively sharpening Python and pytest for this role because the QA problem maps well to my strengths: data validation, matching workflows, regression protection, and clear test evidence. I am comfortable explaining the tests I write and why each case matters.
