"""
FDA Drug Recall Tracker
------------------------
This script does three things, in plain English:

1. FETCH   -> Calls the openFDA public API and downloads recent drug recall
              records (no API key needed for light usage).
2. CLEAN   -> Loads the raw data into a table (using pandas) and keeps only
              the columns that matter, renaming them so they're readable.
3. REPORT  -> Saves a clean CSV file, plus a short text summary showing
              recall counts by classification (how serious the recall is)
              and the most common reasons for recall.

Run it with:  python fetch_fda_recalls.py

Every time you run it, it creates a new timestamped file in /output so you
build up a small history of snapshots over time.
"""

import requests
import pandas as pd
from datetime import datetime
import os

# ---------------------------------------------------------------------------
# STEP 1: FETCH DATA FROM THE OPENFDA API
# ---------------------------------------------------------------------------
# openFDA is a free, public API run by the U.S. Food and Drug Administration.
# This endpoint returns recent drug recall ("enforcement") records.
# Docs: https://open.fda.gov/apis/drug/enforcement/

API_URL = "https://api.fda.gov/drug/enforcement.json"

def fetch_recalls(limit=100):
    """Fetch the most recent `limit` drug recall records from openFDA."""
    params = {
        "sort": "report_date:desc",  # newest first
        "limit": limit               # how many records to grab
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()  # stops the script if the request failed
    data = response.json()
    return data["results"]  # this is a list of dictionaries (one per recall)


# ---------------------------------------------------------------------------
# STEP 2: CLEAN THE DATA
# ---------------------------------------------------------------------------

def clean_recalls(raw_records):
    """Turn the raw API records into a tidy, readable table."""
    df = pd.DataFrame(raw_records)

    # Keep only the columns useful for a recruiter/reader to understand
    columns_to_keep = [
        "report_date",
        "recalling_firm",
        "product_description",
        "reason_for_recall",
        "classification",
        "status",
        "state",
    ]
    df = df[[c for c in columns_to_keep if c in df.columns]]

    # Rename to friendlier headers
    df = df.rename(columns={
        "report_date": "Date Reported",
        "recalling_firm": "Company",
        "product_description": "Product",
        "reason_for_recall": "Reason",
        "classification": "Severity Class",
        "status": "Status",
        "state": "State",
    })

    return df


# ---------------------------------------------------------------------------
# STEP 3: SAVE CSV + WRITE A SUMMARY REPORT
# ---------------------------------------------------------------------------

def save_report(df):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    # Save the full cleaned table
    csv_path = f"output/fda_recalls_{timestamp}.csv"
    df.to_csv(csv_path, index=False)

    # Build a short plain-text summary
    summary_lines = []
    summary_lines.append(f"FDA Drug Recall Summary — generated {timestamp}\n")
    summary_lines.append(f"Total recalls pulled: {len(df)}\n")

    summary_lines.append("Recalls by severity class:")
    summary_lines.append(df["Severity Class"].value_counts().to_string())
    summary_lines.append("")

    summary_lines.append("Top 5 most common recall reasons:")
    summary_lines.append(df["Reason"].value_counts().head(5).to_string())

    summary_path = f"output/summary_{timestamp}.txt"
    with open(summary_path, "w") as f:
        f.write("\n".join(summary_lines))

    print(f"Saved data to: {csv_path}")
    print(f"Saved summary to: {summary_path}")
    print("\n--- Quick preview ---")
    print(df.head(5).to_string(index=False))


# ---------------------------------------------------------------------------
# MAIN — this runs when you execute the script
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Fetching latest FDA drug recall data...")
    raw = fetch_recalls(limit=100)

    print("Cleaning data...")
    clean_df = clean_recalls(raw)

    print("Saving report...")
    save_report(clean_df)

    print("\nDone! Check the /output folder for your files.")
