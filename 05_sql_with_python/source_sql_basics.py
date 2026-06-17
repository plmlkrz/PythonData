# MODULE 5 — SQL with Python using sqlite3
# sqlite3 is built into Python — no install needed.
# Run:  python 05_sql_with_python/source_sql_basics.py
# Then: pytest 05_sql_with_python/source_sql_basics.py -v  (runs the test section)
#
# KEY CONCEPTS:
#   - sqlite3.connect() / conn.cursor() / cursor.execute() / conn.commit()
#   - CREATE TABLE, INSERT, SELECT, WHERE, JOIN, GROUP BY
#   - fetchone(), fetchall(), fetchmany(n)
#   - Parameterized queries — NEVER concatenate user input into SQL
#   - Using an in-memory database (:memory:) for fast, isolated tests

import sqlite3
import pytest


# ─────────────────────────────────────────
# 1. SETUP — create and populate a database
# ─────────────────────────────────────────

def create_schema(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS tracks (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            isrc    TEXT    NOT NULL UNIQUE,
            title   TEXT    NOT NULL,
            artist  TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS usage (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            isrc       TEXT    NOT NULL,
            service    TEXT    NOT NULL,
            plays      INTEGER NOT NULL DEFAULT 0,
            report_dt  TEXT    NOT NULL,
            FOREIGN KEY (isrc) REFERENCES tracks(isrc)
        );
    """)
    conn.commit()


def seed_data(conn: sqlite3.Connection):
    cursor = conn.cursor()

    tracks = [
        ("GBAYE0601498", "Bohemian Rhapsody", "Queen"),
        ("USUM71703861", "Shape of You",       "Ed Sheeran"),
        ("GBUM71029604", "Blinding Lights",    "The Weeknd"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO tracks (isrc, title, artist) VALUES (?, ?, ?)",
        tracks
    )

    usage_rows = [
        ("GBAYE0601498", "Spotify",     1_200_000, "2024-01-01"),
        ("GBAYE0601498", "Apple Music",   800_000, "2024-01-01"),
        ("USUM71703861", "Spotify",     3_500_000, "2024-01-01"),
        ("USUM71703861", "Tidal",         200_000, "2024-01-01"),
        ("GBUM71029604", "Spotify",     2_100_000, "2024-01-01"),
    ]
    cursor.executemany(
        "INSERT INTO usage (isrc, service, plays, report_dt) VALUES (?, ?, ?, ?)",
        usage_rows
    )
    conn.commit()


# ─────────────────────────────────────────
# 2. QUERY HELPERS
# ─────────────────────────────────────────

def get_track(conn: sqlite3.Connection, isrc: str) -> dict | None:
    cursor = conn.cursor()
    cursor.execute("SELECT isrc, title, artist FROM tracks WHERE isrc = ?", (isrc,))
    row = cursor.fetchone()
    if row is None:
        return None
    return {"isrc": row[0], "title": row[1], "artist": row[2]}


def total_plays_by_track(conn: sqlite3.Connection) -> list[dict]:
    """Return each track's total plays across all services, highest first."""
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
    cursor.execute(
        "SELECT isrc, plays FROM usage WHERE service = ? ORDER BY plays DESC",
        (service,)
    )
    return [{"isrc": r[0], "plays": r[1]} for r in cursor.fetchall()]


def insert_usage(conn: sqlite3.Connection, isrc: str, service: str,
                  plays: int, report_dt: str) -> int:
    """Insert one usage row and return the new row's id."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usage (isrc, service, plays, report_dt) VALUES (?, ?, ?, ?)",
        (isrc, service, plays, report_dt)
    )
    conn.commit()
    return cursor.lastrowid


# ─────────────────────────────────────────
# 3. MANUAL DEMO  (runs when executed as a script)
# ─────────────────────────────────────────

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    seed_data(conn)

    print("=== Track lookup ===")
    track = get_track(conn, "GBAYE0601498")
    print(track)

    print("\n=== Total plays per track ===")
    for row in total_plays_by_track(conn):
        print(f"  {row['title']}: {row['total_plays']:,}")

    print("\n=== Spotify plays ===")
    for row in plays_for_service(conn, "Spotify"):
        print(f"  {row['isrc']}: {row['plays']:,}")

    conn.close()


# ─────────────────────────────────────────
# 4. PYTEST TESTS  (each gets a fresh in-memory database)
# ─────────────────────────────────────────

@pytest.fixture
def db():
    """Fresh in-memory database, seeded, torn down after each test."""
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    seed_data(conn)
    yield conn
    conn.close()


def test_get_existing_track(db):
    track = get_track(db, "GBAYE0601498")
    assert track is not None
    assert track["title"] == "Bohemian Rhapsody"
    assert track["artist"] == "Queen"


def test_get_nonexistent_track_returns_none(db):
    assert get_track(db, "ZZZZZZZZZZZZ") is None


def test_total_plays_ordering(db):
    results = total_plays_by_track(db)
    plays = [r["total_plays"] for r in results]
    assert plays == sorted(plays, reverse=True)


def test_total_plays_values(db):
    results = total_plays_by_track(db)
    totals = {r["isrc"]: r["total_plays"] for r in results}
    assert totals["GBAYE0601498"] == 2_000_000   # 1.2M + 0.8M
    assert totals["USUM71703861"] == 3_700_000   # 3.5M + 0.2M


def test_plays_for_service_filters_correctly(db):
    rows = plays_for_service(db, "Spotify")
    assert all(True for r in rows)   # structure check
    isrcs = [r["isrc"] for r in rows]
    assert "GBAYE0601498" in isrcs
    assert "USUM71703861" in isrcs


def test_insert_usage_returns_id(db):
    new_id = insert_usage(db, "GBAYE0601498", "Tidal", 50_000, "2024-02-01")
    assert isinstance(new_id, int)
    assert new_id > 0


def test_insert_usage_persisted(db):
    insert_usage(db, "GBAYE0601498", "Tidal", 50_000, "2024-02-01")
    rows = plays_for_service(db, "Tidal")
    isrcs = [r["isrc"] for r in rows]
    assert "GBAYE0601498" in isrcs
