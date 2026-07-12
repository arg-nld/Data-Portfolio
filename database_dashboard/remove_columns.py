import pandas as pd
import json

# Input and output files
input_file = "games_march2025_cleaned.csv"
output_file = "games_march2025_small.csv"

# Columns to remove
columns_to_remove = [
    "detailed_description", "about_the_game", "short_description", "reviews", "notes",
    "header_image", "website", "support_url", "support_email", "metacritic_url",
    "screenshots", "movies", "required_age", "windows", "mac", "linux",
    "supported_languages", "full_audio_languages", "packages", "achievements",
    "dlc_count", "average_playtime_2weeks", "median_playtime_2weeks",
    "pct_pos_recent", "num_reviews_recent", "discount", "metacritic_score",
    "user_score", "score_rank", "recommendations"
]

# --- Helper Functions for Data Cleaning ---
def clean_string_list(val):
    """Converts a stringified list like \"['Action', 'Indie']\" into a clean string 'Action, Indie'"""
    if pd.isna(val) or not isinstance(val, str):
        return val
    try:
        val_clean = val.replace("'", '"')
        parsed = json.loads(val_clean)
        if isinstance(parsed, list):
            return ", ".join(parsed)
    except:
        return val.replace("[", "").replace("]", "").replace("'", "").replace('"', "").strip()
    return val

def clean_owners_to_midpoint(val):
    """
    Converts text ranges into a single midpoint integer.
    Handles '100000 - 200000', '100000-200000', and '100,000 .. 200,000'
    """
    if pd.isna(val):
        return 0
    try:
        # Strip all commas and spaces first to normalize the string
        clean_str = str(val).replace(",", "").replace(" ", "")
        
        # Split by whichever delimiter is present
        if ".." in clean_str:
            parts = clean_str.split("..")
        elif "-" in clean_str:
            parts = clean_str.split("-")
        else:
            return int(float(clean_str))
            
        # Calculate the midpoint
        low = float(parts[0])
        high = float(parts[1])
        return int((low + high) / 2)
    except:
        return 0

# --- Process Data in Chunks ---
chunksize = 100000
first_chunk = True

for chunk in pd.read_csv(input_file, chunksize=chunksize):
    if first_chunk:
        print("Starting processing. Original columns count:", len(chunk.columns))

    # 1. Remove unwanted columns
    chunk = chunk.drop(columns=columns_to_remove, errors="ignore")

    # 2. Format Data Types & Clean Internal Values
    for col in ["developers", "publishers", "categories", "genres"]:
        if col in chunk.columns:
            chunk[col] = chunk[col].apply(clean_string_list)
            
    # CRITICAL FIX: Convert estimated_owners text range into numeric format
    if "estimated_owners" in chunk.columns:
        # Overwrite the original column with the new numeric data
        chunk["estimated_owners"] = chunk["estimated_owners"].apply(clean_owners_to_midpoint)
        
    # Fix the missing review scores flag (-1) by setting them to 0
    if "pct_pos_total" in chunk.columns:
        chunk["pct_pos_total"] = chunk["pct_pos_total"].replace(-1, 0)
    if "num_reviews_total" in chunk.columns:
        chunk["num_reviews_total"] = chunk["num_reviews_total"].replace(-1, 0)

    # 3. Save to the new clean CSV
    chunk.to_csv(
        output_file,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    first_chunk = False

print(f"\nDone! Completely cleaned, formatted, and saved CSV as '{output_file}'")