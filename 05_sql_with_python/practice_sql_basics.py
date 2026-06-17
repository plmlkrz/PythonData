# MODULE 5 — PRACTICE: reproduce the SQL + pytest file from memory.
#
# SCHEMA:
#   tracks  (id AUTOINCREMENT, isrc UNIQUE, title, artist)
#   usage   (id AUTOINCREMENT, isrc FK, service, plays, report_dt)
#
# FUNCTIONS TO REPRODUCE:
#   create_schema(conn)       — executescript with both CREATE TABLE statements
#   seed_data(conn)           — 3 tracks, 5 usage rows via executemany
#   get_track(conn, isrc)     — SELECT one track, return dict or None
#   total_plays_by_track(conn) — JOIN + GROUP BY + ORDER BY DESC
#   plays_for_service(conn, service) — filter by service, ORDER BY plays DESC
#   insert_usage(conn, ...)   — INSERT one row, return cursor.lastrowid
#
# FIXTURE:
#   db()  — in-memory DB, create_schema + seed_data, yield conn, close on teardown
#
# TESTS TO WRITE:
#   - test_get_existing_track            (check title and artist)
#   - test_get_nonexistent_track_returns_none
#   - test_total_plays_ordering          (verify descending sort)
#   - test_total_plays_values            (spot-check two ISRCs)
#   - test_plays_for_service_filters_correctly
#   - test_insert_usage_returns_id       (int, > 0)
#   - test_insert_usage_persisted        (re-query to confirm)
#
# IMPORTANT: use parameterized queries — placeholders (?) not f-strings.
#
# Write your code below.
# ─────────────────────────────────────────────────────────────────────────────
