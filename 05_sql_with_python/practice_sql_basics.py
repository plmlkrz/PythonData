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
import sqlite3
from typing import Dict

import pytest


# 1. SETUP — create and populate a database
def create_schema(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.executescript("""
                         CREATE TABLE IF NOT EXISTS tracks
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             isrc
                             TEXT
                             NOT
                             NULL
                             UNIQUE,
                             title
                             TEXT
                             NOT
                             NULL,
                             artist
                             TEXT
                             NOT
                             NULL
                         );

                         CREATE TABLE IF NOT EXISTS usage
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             isrc
                             TEXT
                             NOT
                             NULL,
                             service
                             TEXT
                             NOT
                             NULL,
                             plays
                             INTEGER
                             NOT
                             NULL
                             DEFAULT
                             0,
                             report_dt
                             TEXT
                             NOT
                             NULL,
                             FOREIGN
                             KEY
                         (
                             isrc
                         ) REFERENCES tracks
                         (
                             isrc
                         )
                             );
                         """)
    conn.commit()


def seed_data(conn: sqlite3.Connection):
    cursor = conn.cursor()
    tracks = [
        ("GBAYE0601498", "Bohemian Rhapsody", "Queen"),
        ("USUM71703861", "Shape of You", "Ed Sheeran"),
        ("GBUM71029604", "Blinding Lights", "The Weeknd"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO tracks (isrc, title, artist) VALUES (?, ?, ?)", tracks)

    usage_rows = [
        ("GBAYE0601498", "Spotify", 1_200_000, "2024-01-01"),
        ("GBAYE0601498", "Apple Music", 800_000, "2024-01-01"),
        ("USUM71703861", "Spotify", 3_500_000, "2024-01-01"),
        ("USUM71703861", "Tidal", 200_000, "2024-01-01"),
        ("GBUM71029604", "Spotify", 2_100_000, "2024-01-01"),
    ]
    cursor.executemany("INSERT INTO usage (isrc, service, plays, report_dt) VALUES (?, ?, ?, ?)", usage_rows)
    conn.commit()


# 2. QUERY HELPERS

def get_track(conn: sqlite3.Connection, isrc: str) -> dict | None:
    cursor = conn.cursor()
    cursor.execute("SELECT isrc, title, artist FROM tracks WHERE isrc = ?", (isrc,))
    row = cursor.fetchone()
    if row is None:
        return None
    return {"isrc": row[0], "title": row[1], "artist": row[2]}


def total_plays_by_track(conn: sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT t.isrc, t.title, SUM(u.plays) AS total_plays
                   FROM tracks t
                            JOIN usage u ON t.isrc = u.isrc
                   GROUP BY t.isrc, t.title
                   ORDER BY total_plays DESC
                   """)
    rows = cursor.fetchall()
    return [{"isrc": r[0], "title": r[1], "total_plays": r[2]} for r in rows]


def plays_for_service(conn: sqlite3.Connection, service: str) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT isrc, plays FROM usage WHERE service = ? ORDER BY plays DESC", (service,))
    return [{"isrc": r[0], "plays": r[1]} for r in cursor.fetchall()]


def insert_usage(conn: sqlite3.Connection, isrc: str, service: str, plays: int, report_dt: str) -> int:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usage (isrc, service, plays, report_dt) VALUES (?, ?, ?, ?)",
                   (isrc, service, plays, report_dt))
    conn.commit()
    return cursor.lastrowid

# 3. MANUAL DEMO  (runs when executed as a script)
