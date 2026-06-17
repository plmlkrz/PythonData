# MODULE 3 — PRACTICE: reproduce the API test file from memory.
#
# SETUP:
#   BASE_URL = "https://jsonplaceholder.typicode.com"
#
# FIXTURES:
#   - session()  — module-scoped requests.Session, closed on teardown
#
# TESTS TO WRITE:
#   GET /posts/1
#     - returns 200
#     - json has keys: id, title, body, userId
#     - id equals 1
#   GET /posts/99999
#     - returns 404
#   GET /posts
#     - returns list of 100
#     - filtering by userId works (all results share that userId)
#   POST /posts  (payload: title, body, userId)
#     - returns 201
#     - response contains an id (int)
#     - response echoes the payload values
#   Headers
#     - Content-Type contains "application/json"
#   Schema check
#     - every post in /posts has all required keys
#
# Write your code below.
# ─────────────────────────────────────────────────────────────────────────────
