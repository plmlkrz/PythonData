# MODULE 1 — Python Basics for QA Engineers
# Study this file. Then open practice_01_basics.py and reproduce it from memory.
# Return here to check your work. Repeat until it flows naturally.

# ─────────────────────────────────────────
# 1. VARIABLES AND DATA TYPES
# ─────────────────────────────────────────

song_title = "Bohemian Rhapsody"          # str
play_count = 1_500_000                    # int  (underscores aid readability)
royalty_rate = 0.091                      # float
is_licensed = True                        # bool
missing_value = None                      # NoneType

print(type(song_title))     # <class 'str'>
print(type(play_count))     # <class 'int'>


# ─────────────────────────────────────────
# 2. LISTS  (ordered, mutable)
# ─────────────────────────────────────────

services = ["Spotify", "Apple Music", "Amazon Music", "YouTube Music"]

print(services[0])          # Spotify     (first item)
print(services[-1])         # YouTube Music (last item)
print(services[1:3])        # ['Apple Music', 'Amazon Music']  (slice)

services.append("Tidal")    # add to end
services.remove("Amazon Music")  # remove by value
print(len(services))        # 4


# ─────────────────────────────────────────
# 3. DICTIONARIES  (key-value, mutable)
# ─────────────────────────────────────────

track = {
    "isrc": "GBAYE0601498",
    "title": "Bohemian Rhapsody",
    "artist": "Queen",
    "plays": 1_500_000,
}

print(track["title"])                       # Bohemian Rhapsody
print(track.get("label", "Unknown"))        # Unknown  (.get avoids KeyError)

track["plays"] += 500                       # update a value
track["duration_sec"] = 354                 # add a new key

print(track.keys())     # dict_keys([...])
print(track.values())   # dict_values([...])
print(track.items())    # dict_items([...])  ← useful for iteration


# ─────────────────────────────────────────
# 4. CONTROL FLOW
# ─────────────────────────────────────────

# if / elif / else
plays = 1_500_000

if plays > 1_000_000:
    tier = "Platinum"
elif plays > 500_000:
    tier = "Gold"
else:
    tier = "Standard"

print(tier)   # Platinum

# for loop over a list
for service in services:
    print(f"  Checking {service}...")

# for loop over dict items
for key, value in track.items():
    print(f"  {key}: {value}")

# while loop
attempts = 0
while attempts < 3:
    print(f"  Attempt {attempts + 1}")
    attempts += 1


# ─────────────────────────────────────────
# 5. FUNCTIONS
# ─────────────────────────────────────────

def calculate_royalty(plays: int, rate: float = 0.091) -> float:
    """Return total royalty amount for a given play count and rate."""
    return round(plays * rate, 2)


def parse_isrc(isrc: str) -> dict:
    """Split an ISRC into its component parts."""
    return {
        "country": isrc[:2],
        "registrant": isrc[2:5],
        "year": isrc[5:7],
        "designation": isrc[7:],
    }


print(calculate_royalty(1_500_000))             # 136500.0
print(calculate_royalty(1_500_000, rate=0.10))  # 150000.0
print(parse_isrc("GBAYE0601498"))


# ─────────────────────────────────────────
# 6. LIST COMPREHENSIONS
# ─────────────────────────────────────────

plays_list = [120_000, 850_000, 1_500_000, 300_000, 2_100_000]

# Build a list of royalties
royalties = [calculate_royalty(p) for p in plays_list]
print(royalties)

# Filter: only tracks with plays > 500k
high_plays = [p for p in plays_list if p > 500_000]
print(high_plays)   # [850000, 1500000, 2100000]


# ─────────────────────────────────────────
# 7. F-STRINGS  (formatted string literals)
# ─────────────────────────────────────────

artist = "Queen"
total = calculate_royalty(1_500_000)
print(f"{artist} earned ${total:,.2f} in royalties")   # comma-thousands, 2 decimals


# ─────────────────────────────────────────
# 8. EXCEPTION HANDLING
# ─────────────────────────────────────────

def safe_divide(numerator: float, denominator: float) -> float:
    try:
        return numerator / denominator
    except ZeroDivisionError:
        print("Cannot divide by zero — returning 0")
        return 0.0


print(safe_divide(100, 4))    # 25.0
print(safe_divide(100, 0))    # prints warning, returns 0.0


# ─────────────────────────────────────────
# 9. WORKING WITH LISTS OF DICTS  (common in QA data validation)
# ─────────────────────────────────────────

usage_records = [
    {"isrc": "US-S1Z-99-00001", "plays": 500, "service": "Spotify"},
    {"isrc": "US-S1Z-99-00002", "plays": 0,   "service": "Spotify"},
    {"isrc": "US-S1Z-99-00003", "plays": 1200, "service": "Apple Music"},
    {"isrc": "US-S1Z-99-00004", "plays": -5,  "service": "Tidal"},   # bad data
]

# Find records with invalid play counts
invalid = [r for r in usage_records if r["plays"] <= 0]
print(f"Invalid records: {len(invalid)}")   # 2

# Sort by plays descending
sorted_records = sorted(usage_records, key=lambda r: r["plays"], reverse=True)
for rec in sorted_records:
    print(f"  {rec['isrc']}: {rec['plays']} plays")
