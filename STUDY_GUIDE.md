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

## Interview Talk Tracks

- "I write pytest tests with fixtures for shared setup, parametrize for data-driven cases, and pytest.raises for expected exceptions."

- "I validate APIs by checking status code, response structure, required fields, data types, and negative/error behavior."

- "For SQL testing, I prefer parameterized queries and in-memory SQLite for fast, isolated validation of schema, joins, filters, and aggregation logic."

- "For matching systems, I test threshold boundaries, false positives, false negatives, ambiguous ties, no-candidate cases, and audit evidence so a human can understand why the system made a decision."

- "My strongest QA value is not just writing scripts. It is deciding what should be automated, what should be manually reviewed, and where data quality creates release or payment risk."

## Suggested Practice Plan Before June 25

**Day 1:** Module 2 - pytest fixtures, raises, approx, batch processing.  
**Day 2:** Module 4 - parametrize, JSON/CSV data-driven cases.  
**Day 3:** Module 5 - SQLite schema, seed data, joins, group by, parameterized queries.  
**Day 4:** Module 6 - matching thresholds, ambiguity handling, audit messages.  
**Day 5:** Mock interview: explain how you would build QA from scratch for MLC's data/matching workflow.  
**Day 6:** Cold run: open only the practice files and write as much as you can in 60-90 minutes.

## What To Say If Asked About Python Depth

Use honest ramp language:

> My deepest production automation background is Selenium/Java, Cucumber/BDD, UFT, API testing, and SQL validation. I have been actively sharpening Python and pytest for this role because the QA problem maps well to my strengths: data validation, matching workflows, regression protection, and clear test evidence. I am comfortable explaining the tests I write and why each case matters.
