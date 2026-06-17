# Python QA Interview Study Guide — The MLC

## Setup (do this once)

```
pip install -r requirements.txt
```

---

## How to use this project

1. Open the `source_` file for a module. Read it carefully — don't rush.
2. Close it (or minimize the window so you can't peek).
3. Open the matching `practice_` file. Write everything from memory.
4. Return to the source and compare. Note what you missed or got wrong.
5. Repeat steps 2–4 until you can reproduce the whole file cleanly.

---

## Modules

| # | Topic | Source file | Run with |
|---|-------|-------------|----------|
| 1 | Python basics | `01_python_basics/source_01_basics.py` | `python source_01_basics.py` |
| 2 | pytest + fixtures | `02_pytest_basics/source_test_royalty_calculator.py` | `pytest 02_pytest_basics/ -v` |
| 3 | API testing | `03_api_testing/source_api_tests.py` | `pytest 03_api_testing/ -v` |
| 4 | Data-driven testing | `04_data_driven/source_data_driven.py` | `pytest 04_data_driven/ -v` |
| 5 | SQL with Python | `05_sql_with_python/source_sql_basics.py` | `pytest 05_sql_with_python/ -v` |

---

## Key things the MLC JD specifically asks about

| JD requirement | Covered in |
|----------------|-----------|
| Python proficiency | Modules 1–5 (all) |
| Automated tests (pytest) | Module 2 |
| API testing | Module 3 |
| Data-driven / workflow systems | Module 4 |
| SQL proficiency | Module 5 |
| Testing frameworks from scratch | Module 2 (RoyaltyCalculator + full suite) |
| Attention to edge cases | All modules (zero, negative, None, empty list) |

---

## Things to be ready to say in the interview

- "I write tests using pytest. I use fixtures for shared setup, parametrize for
  data-driven cases, and pytest.raises for expected exceptions."

- "I validate APIs by asserting status codes, response structure, and data
  types — not just the happy path."

- "For SQL, I always use parameterized queries to avoid injection.
  I use in-memory SQLite databases for fast, isolated test runs."

- "I test edge cases explicitly: zero, negative numbers, empty collections,
  missing fields, wrong types."

---

## Suggested daily practice order

**Day 1:** Module 1 — copy it 3 times until you can write it from scratch.  
**Day 2:** Module 2 — write the class, then write all the tests.  
**Day 3:** Module 3 — write all the API tests; run them (needs internet).  
**Day 4:** Module 4 — write validate_usage_record(), then all parametrize patterns.  
**Day 5:** Module 5 — write the schema, seed, queries, and tests.  
**Day 6+:** Mix and match — open a practice file cold and time yourself.
