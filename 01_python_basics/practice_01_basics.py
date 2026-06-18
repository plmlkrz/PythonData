# MODULE 1 — PRACTICE FILE
# Close source_01_basics.py. Reproduce each section from memory.
# Open the source only to check, not to copy line-by-line.
#
# SECTIONS TO REPRODUCE:
#   1. Variables and data types
#   2. Lists (create, index, slice, append, remove, len)
#   3. Dictionaries (create, access, .get, update, add key, .keys/.values/.items)
#   4. Control flow (if/elif/else, for over list, for over dict.items, while)
#   5. Functions (with type hints and default arg)
#   6. List comprehensions (transform + filter)
#   7. f-strings with formatting
#   8. Exception handling (try/except)
#   9. Lists of dicts (filter invalid, sort by key)
#
# Write your code below this line.
# ─────────────────────────────────────────────────────────────────────────────

# Variables

song_title = "Bohemian Rhapsody"
play_count = 1_500_000
royalty_rate = 0.091
is_licensed = True
missing_value = None

print(type(song_title))
print(type(play_count))

# Lists

services = ["Spotify", "Apple Music", "Amazon Music", "Youtube Music"]

print(services[1])
print(services[-1])
print(services[1:3])

services.append("Tidal")
services.remove("Apple Music")
print(len(services))

# Dictionaries

track = {
"isrc": "GBAYE0601498",
"title": "Bohemian Rhapsody",
"artist": "Queen",
"plays": 1_500_000,
}

print(track["title"])
print(track.get("Label", "Unknown"))

track["plays"] += 500
track["duration_sec"] = 354

print(track.keys())
print(track.values())
print(track.items())

# Control Flow
plays = 1_500_000

if plays > 1_000_000:
    tier = "Platinum"
elif plays > 500_000:
    tier = "Gold"
else:
    tier = "Standard"

print(tier)

for services in services:
    print(f" Checking{services}...")

for key, value in track.items():
    print(f" {key}:{value}")

attempts = 0
while attempts < 3:
    print(f" Attempt{attempts + 1}")
    attempts += 1

# Functions

def calculate_royalty(plays: int, rate: float = 0.091) -> float:
    return round(plays * rate, 2)

def parse_isrc(isrc: str) -> dict:
    return {
        "Country": isrc[:2],
        "registrant": isrc[2:5],
        "year": isrc[5:7],
        "designation": isrc[7:]
    }
print(calculate_royalty(1_500_000))
print(calculate_royalty(1_500_000, rate=0.10))
print(parse_isrc("GBAYE0601498"))

# LIST COMPREHENSIONS

plays_list=[120_000, 850_000, 1_500_000, 300_000, 2_100_000]
royalties = [calculate_royalty(p) for p in plays_list]
print(royalties)

high_plays = [p for p in plays_list if p > 500_000]
print(high_plays)

# F-STRINGS  (formatted string literals)

artist = "Queen"
total = calculate_royalty(1_500_000)
print(f"{artist} earned ${total:,.2f} in royalties")

# Exception Handling

def safe_divide(numerator: float, denominator: float) -> float:
    try:
        return numerator / denominator
    except ZeroDivisionError:
        print("Cannot divide by zero - returning 0")
        return 0.0


print(safe_divide(100,4))
print(safe_divide(100, 0))

# WORKING WITH LISTS OF DICTS

usage_records = [
    {"isrc": "US-S1Z-99-00001", "plays": 500, "service": "Spotify"},
    {"isrc": "US-S1Z-99-00002", "plays": 0,   "service": "Spotify"},
    {"isrc": "US-S1Z-99-00003", "plays": 1200, "service": "Apple Music"},
    {"isrc": "US-S1Z-99-00004", "plays": -5,  "service": "Tidal"}
]

invalid = [r for r in usage_records if r["plays"] <= 0]
print(f"Invalid records: {len(invalid)}")

sorted_records = sorted(usage_records, key=lambda r: r["plays"], reverse=True)
for rec in sorted_records:
    print(f" {rec["isrc"]}: {rec["plays"]} plays")
