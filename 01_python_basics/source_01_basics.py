# MODULE 1 — Python Basics for QA Engineers
# Study this file. Then open practice_01_basics.py and reproduce it from memory.
# Return here to check your work. Repeat until it flows naturally.

# ─────────────────────────────────────────
# 1. VARIABLES AND DATA TYPES
# ─────────────────────────────────────────

song_title = "Bohemian Rhapsody"          # Assign a string value to the variable song_title
play_count = 1_500_000                    # Assign an integer (underscores aid readability, don't affect the value)
royalty_rate = 0.091                      # Assign a decimal (float) number
is_licensed = True                        # Assign a boolean True value
missing_value = None                      # Assign None (represents "no value" or missing data)

print(type(song_title))     # Display the data type of song_title → <class 'str'>
print(type(play_count))     # Display the data type of play_count → <class 'int'>


# ─────────────────────────────────────────
# 2. LISTS  (ordered, mutable)
# ─────────────────────────────────────────

services = ["Spotify", "Apple Music", "Amazon Music", "YouTube Music"]  # Create a list with 4 streaming service names

print(services[0])          # Print the first item in the list using index 0 → Spotify
print(services[-1])         # Print the last item using negative index -1 → YouTube Music
print(services[1:3])        # Print a slice from index 1 up to (not including) 3 → ['Apple Music', 'Amazon Music']

services.append("Tidal")    # Add "Tidal" to the end of the list
services.remove("Amazon Music")  # Remove "Amazon Music" from the list by its value
print(len(services))        # Print the number of items in the list → 4


# ─────────────────────────────────────────
# 3. DICTIONARIES  (key-value, mutable)
# ─────────────────────────────────────────

track = {  # Create a dictionary with 4 key-value pairs
    "isrc": "GBAYE0601498",  # Key "isrc" maps to the ISRC code
    "title": "Bohemian Rhapsody",  # Key "title" maps to the song title
    "artist": "Queen",  # Key "artist" maps to the artist name
    "plays": 1_500_000,  # Key "plays" maps to the play count
}

print(track["title"])                       # Access the value for key "title" and print it → Bohemian Rhapsody
print(track.get("label", "Unknown"))        # Safely access "label" key (returns "Unknown" if key doesn't exist, avoids KeyError)

track["plays"] += 500                       # Update the value for "plays" key by adding 500 to it
track["duration_sec"] = 354                 # Add a new key-value pair to the dictionary

print(track.keys())     # Print all keys in the dictionary → dict_keys([...])
print(track.values())   # Print all values in the dictionary → dict_values([...])
print(track.items())    # Print all key-value pairs as tuples → dict_items([...])  (useful for iteration)


# ─────────────────────────────────────────
# 4. CONTROL FLOW
# ─────────────────────────────────────────

# if / elif / else — conditional branching
plays = 1_500_000  # Assign a value to check

if plays > 1_000_000:  # Check if plays exceeds 1 million
    tier = "Platinum"  # Execute this if condition is True
elif plays > 500_000:  # Else-if: check if plays exceeds 500k
    tier = "Gold"  # Execute this if elif is True
else:  # Fallback when all above conditions are False
    tier = "Standard"  # Default assignment

print(tier)   # Print the tier variable → Platinum

# for loop over a list — iterate through each item
for service in services:  # Loop through each item in the services list
    print(f"  Checking {service}...")  # Print each service name (f-string embeds the variable)

# for loop over dict items — unpack key-value pairs
for key, value in track.items():  # Loop through dictionary, unpacking each key-value pair
    print(f"  {key}: {value}")  # Print the key and its value

# while loop — repeat while condition is True
attempts = 0  # Initialize counter at 0
while attempts < 3:  # Loop as long as attempts is less than 3 (runs 3 times)
    print(f"  Attempt {attempts + 1}")  # Print attempt number (1, 2, or 3)
    attempts += 1  # Increment counter (attempts = attempts + 1)


# ─────────────────────────────────────────
# 5. FUNCTIONS
# ─────────────────────────────────────────

def calculate_royalty(plays: int, rate: float = 0.091) -> float:  # Define function with type hints: takes int, float; returns float
    """Return total royalty amount for a given play count and rate."""  # Docstring explaining what function does
    return round(plays * rate, 2)  # Calculate plays × rate, round to 2 decimals, and return the result


def parse_isrc(isrc: str) -> dict:  # Define function that takes a string, returns a dictionary
    """Split an ISRC into its component parts."""  # Docstring explaining the function
    return {  # Return a dictionary with extracted parts
        "country": isrc[:2],  # Slice characters 0-2 (country code)
        "registrant": isrc[2:5],  # Slice characters 2-5 (registrant code)
        "year": isrc[5:7],  # Slice characters 5-7 (year code)
        "designation": isrc[7:],  # Slice characters 7 to end (designation code)
    }


print(calculate_royalty(1_500_000))             # Call function with default rate (0.091) → 136500.0
print(calculate_royalty(1_500_000, rate=0.10))  # Call function with custom rate argument (named argument) → 150000.0
print(parse_isrc("GBAYE0601498"))  # Call function and print the returned dictionary


# ─────────────────────────────────────────
# 6. LIST COMPREHENSIONS
# ─────────────────────────────────────────

plays_list = [120_000, 850_000, 1_500_000, 300_000, 2_100_000]  # Create a list of play counts

# Build a list of royalties — transform each item using a function
royalties = [calculate_royalty(p) for p in plays_list]  # Create new list by calling calculate_royalty on each item p
print(royalties)  # Print the resulting list of calculated royalties

# Filter: only tracks with plays > 500k — keep only items that meet a condition
high_plays = [p for p in plays_list if p > 500_000]  # Create new list with only items greater than 500,000
print(high_plays)   # Print the filtered list → [850000, 1500000, 2100000]


# ─────────────────────────────────────────
# 7. F-STRINGS  (formatted string literals)
# ─────────────────────────────────────────

artist = "Queen"  # Assign artist name to variable
total = calculate_royalty(1_500_000)  # Call function and store result in total
print(f"{artist} earned ${total:,.2f} in royalties")   # Print f-string with formatting: :, adds comma thousands separator, .2f rounds to 2 decimals


# ─────────────────────────────────────────
# 8. EXCEPTION HANDLING
# ─────────────────────────────────────────

def safe_divide(numerator: float, denominator: float) -> float:  # Define function to safely divide two numbers
    try:  # Start a try block — code that might cause an error
        return numerator / denominator  # Perform division (may raise ZeroDivisionError if denominator is 0)
    except ZeroDivisionError:  # Catch the ZeroDivisionError exception if it occurs
        print("Cannot divide by zero — returning 0")  # Print error message
        return 0.0  # Return 0 as fallback instead of crashing


print(safe_divide(100, 4))    # Call function with valid inputs → 25.0
print(safe_divide(100, 0))    # Call function with zero denominator (triggers except block, prints warning, returns 0.0)


# ─────────────────────────────────────────
# 9. WORKING WITH LISTS OF DICTS  (common in QA data validation)
# ─────────────────────────────────────────

usage_records = [  # Create a list of dictionaries (common in QA data validation)
    {"isrc": "US-S1Z-99-00001", "plays": 500, "service": "Spotify"},  # Dict 1: normal record
    {"isrc": "US-S1Z-99-00002", "plays": 0,   "service": "Spotify"},  # Dict 2: invalid (0 plays)
    {"isrc": "US-S1Z-99-00003", "plays": 1200, "service": "Apple Music"},  # Dict 3: normal record
    {"isrc": "US-S1Z-99-00004", "plays": -5,  "service": "Tidal"},   # Dict 4: invalid (negative plays)
]

# Find records with invalid play counts — filter using list comprehension
invalid = [r for r in usage_records if r["plays"] <= 0]  # Create list of records where plays is 0 or negative
print(f"Invalid records: {len(invalid)}")   # Print count of invalid records → 2

# Sort by plays descending — use sorted() with a custom key
sorted_records = sorted(usage_records, key=lambda r: r["plays"], reverse=True)  # Sort by "plays" value in descending order
for rec in sorted_records:  # Loop through each sorted record
    print(f"  {rec['isrc']}: {rec['plays']} plays")  # Print ISRC and play count for each record
