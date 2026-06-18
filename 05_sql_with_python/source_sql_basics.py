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

import sqlite3  # Import sqlite3 module for database operations
import pytest  # Import pytest testing framework


# ─────────────────────────────────────────
# 1. SETUP — create and populate a database
# ─────────────────────────────────────────

def create_schema(conn: sqlite3.Connection):  # Function to create database tables
    cursor = conn.cursor()  # Create a cursor object (used to execute SQL commands)
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
    conn.commit()  # Commit the transaction (save changes to database)


def seed_data(conn: sqlite3.Connection):  # Function to populate database with test data
    cursor = conn.cursor()  # Create cursor object

    tracks = [  # Create list of track data
        ("GBAYE0601498", "Bohemian Rhapsody", "Queen"),  # Track 1: Queen song
        ("USUM71703861", "Shape of You",       "Ed Sheeran"),  # Track 2: Ed Sheeran song
        ("GBUM71029604", "Blinding Lights",    "The Weeknd"),  # Track 3: The Weeknd song
    ]
    cursor.executemany(  # Execute INSERT statement multiple times (once per row)
        "INSERT OR IGNORE INTO tracks (isrc, title, artist) VALUES (?, ?, ?)",  # ? are placeholders for values
        tracks  # Pass list of data tuples
    )

    usage_rows = [  # Create list of usage data (plays per service)
        ("GBAYE0601498", "Spotify",     1_200_000, "2024-01-01"),  # 1.2M plays on Spotify
        ("GBAYE0601498", "Apple Music",   800_000, "2024-01-01"),  # 800k plays on Apple Music
        ("USUM71703861", "Spotify",     3_500_000, "2024-01-01"),  # 3.5M plays on Spotify
        ("USUM71703861", "Tidal",         200_000, "2024-01-01"),  # 200k plays on Tidal
        ("GBUM71029604", "Spotify",     2_100_000, "2024-01-01"),  # 2.1M plays on Spotify
    ]
    cursor.executemany(  # Execute INSERT statement multiple times
        "INSERT INTO usage (isrc, service, plays, report_dt) VALUES (?, ?, ?, ?)",  # ? are placeholders
        usage_rows  # Pass list of data tuples
    )
    conn.commit()  # Commit transaction (save changes)


# ─────────────────────────────────────────
# 2. QUERY HELPERS
# ─────────────────────────────────────────

def get_track(conn: sqlite3.Connection, isrc: str) -> dict | None:  # Function to fetch a single track by ISRC
    cursor = conn.cursor()  # Create cursor
    cursor.execute("SELECT isrc, title, artist FROM tracks WHERE isrc = ?", (isrc,))  # Execute SELECT with parameterized query (? prevents SQL injection)
    row = cursor.fetchone()  # Fetch first (and only) result
    if row is None:  # If no track found
        return None  # Return None
    return {"isrc": row[0], "title": row[1], "artist": row[2]}  # Return dict with track info


def total_plays_by_track(conn: sqlite3.Connection) -> list[dict]:  # Function to get total plays per track
    """Return each track's total plays across all services, highest first."""
    cursor = conn.cursor()  # Create cursor
    cursor.execute("""
        SELECT t.isrc, t.title, SUM(u.plays) AS total_plays
        FROM tracks t
        JOIN usage u ON t.isrc = u.isrc
        GROUP BY t.isrc, t.title
        ORDER BY total_plays DESC
    """)
    rows = cursor.fetchall()  # Fetch all results
    return [{"isrc": r[0], "title": r[1], "total_plays": r[2]} for r in rows]  # Convert rows to list of dicts


def plays_for_service(conn: sqlite3.Connection, service: str) -> list[dict]:  # Function to get plays for a specific service
    cursor = conn.cursor()  # Create cursor
    cursor.execute(  # Execute SELECT query
        "SELECT isrc, plays FROM usage WHERE service = ? ORDER BY plays DESC",  # Select isrc and plays where service matches
        (service,)  # Parameter for WHERE clause
    )
    return [{"isrc": r[0], "plays": r[1]} for r in cursor.fetchall()]  # Fetch all and convert to dicts


def insert_usage(conn: sqlite3.Connection, isrc: str, service: str,
                  plays: int, report_dt: str) -> int:  # Function to insert a usage record
    """Insert one usage row and return the new row's id."""
    cursor = conn.cursor()  # Create cursor
    cursor.execute(  # Execute INSERT query
        "INSERT INTO usage (isrc, service, plays, report_dt) VALUES (?, ?, ?, ?)",  # INSERT statement with placeholders
        (isrc, service, plays, report_dt)  # Parameters for INSERT
    )
    conn.commit()  # Commit transaction
    return cursor.lastrowid  # Return ID of newly inserted row


# ─────────────────────────────────────────
# 3. MANUAL DEMO  (runs when executed as a script)
# ─────────────────────────────────────────

if __name__ == "__main__":  # Check if script is run directly (not imported)
    conn = sqlite3.connect(":memory:")  # Create in-memory database (exists only during this run)
    create_schema(conn)  # Create tables
    seed_data(conn)  # Populate with test data

    print("=== Track lookup ===")  # Print section header
    track = get_track(conn, "GBAYE0601498")  # Look up Bohemian Rhapsody
    print(track)  # Print track info

    print("\n=== Total plays per track ===")  # Print section header
    for row in total_plays_by_track(conn):  # Get all tracks with total plays
        print(f"  {row['title']}: {row['total_plays']:,}")  # Print title and formatted play count

    print("\n=== Spotify plays ===")  # Print section header
    for row in plays_for_service(conn, "Spotify"):  # Get all Spotify plays
        print(f"  {row['isrc']}: {row['plays']:,}")  # Print ISRC and formatted play count

    conn.close()  # Close database connection


# ─────────────────────────────────────────
# 4. PYTEST TESTS  (each gets a fresh in-memory database)
# ─────────────────────────────────────────

@pytest.fixture  # Decorator: mark as pytest fixture
def db():  # Fixture function: provides database for tests
    """Fresh in-memory database, seeded, torn down after each test."""
    conn = sqlite3.connect(":memory:")  # Create fresh in-memory database
    create_schema(conn)  # Create tables
    seed_data(conn)  # Populate with test data
    yield conn  # Provide connection to test (test runs here)
    conn.close()  # Teardown: close connection after test completes


def test_get_existing_track(db):  # Test function receives db fixture
    track = get_track(db, "GBAYE0601498")  # Look up Bohemian Rhapsody
    assert track is not None  # Assert track was found
    assert track["title"] == "Bohemian Rhapsody"  # Assert title is correct
    assert track["artist"] == "Queen"  # Assert artist is correct


def test_get_nonexistent_track_returns_none(db):  # Test that querying non-existent track returns None
    assert get_track(db, "ZZZZZZZZZZZZ") is None  # Assert returns None for invalid ISRC


def test_total_plays_ordering(db):  # Test that total_plays_by_track returns results in correct order
    results = total_plays_by_track(db)  # Get all tracks with totals
    plays = [r["total_plays"] for r in results]  # Extract play counts into list
    assert plays == sorted(plays, reverse=True)  # Assert list is sorted descending


def test_total_plays_values(db):  # Test that total_plays_by_track calculates correct sums
    results = total_plays_by_track(db)  # Get all tracks with totals
    totals = {r["isrc"]: r["total_plays"] for r in results}  # Create dict of ISRC → total_plays
    assert totals["GBAYE0601498"] == 2_000_000   # Assert sum: 1.2M (Spotify) + 0.8M (Apple Music)
    assert totals["USUM71703861"] == 3_700_000   # Assert sum: 3.5M (Spotify) + 0.2M (Tidal)


def test_plays_for_service_filters_correctly(db):  # Test that plays_for_service filters by service
    rows = plays_for_service(db, "Spotify")  # Get Spotify plays
    assert all(True for r in rows)   # Simple structure check
    isrcs = [r["isrc"] for r in rows]  # Extract ISRCs
    assert "GBAYE0601498" in isrcs  # Assert Bohemian Rhapsody is in results
    assert "USUM71703861" in isrcs  # Assert Shape of You is in results


def test_insert_usage_returns_id(db):  # Test that insert_usage returns the new row's ID
    new_id = insert_usage(db, "GBAYE0601498", "Tidal", 50_000, "2024-02-01")  # Insert new usage record
    assert isinstance(new_id, int)  # Assert returned ID is an integer
    assert new_id > 0  # Assert ID is positive


def test_insert_usage_persisted(db):  # Test that newly inserted row is queryable
    insert_usage(db, "GBAYE0601498", "Tidal", 50_000, "2024-02-01")  # Insert new usage record
    rows = plays_for_service(db, "Tidal")  # Query Tidal plays
    isrcs = [r["isrc"] for r in rows]  # Extract ISRCs from results
    assert "GBAYE0601498" in isrcs  # Assert newly inserted record is in results
