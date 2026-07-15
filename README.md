# FDA Drug Recall Tracker

A small Python automation that pulls recent U.S. FDA drug recall data, cleans it, and generates a readable summary report — automatically, on a daily schedule.

## What it does

1. **Fetches** the most recent drug recall records from the [openFDA API](https://open.fda.gov/apis/drug/enforcement/), a free, public data source maintained by the U.S. Food and Drug Administration.
2. **Cleans** the raw data into a readable table: company, product, reason for recall, severity classification, and status.
3. **Generates a report**: a CSV of the full data plus a plain-text summary showing recall counts by severity and the most common recall reasons.
4. **Runs automatically**: a GitHub Actions workflow (`.github/workflows/daily-run.yml`) runs this script every day and commits the new report back into the repo — no manual work required.

## Why I built this

Recall data is scattered and easy to miss. This script turns a public but hard-to-parse API into a lightweight, always-up-to-date report — the kind of small, practical data pipeline useful in a healthcare or compliance-adjacent setting.

## How to run it yourself

```bash
# 1. Clone this repo
git clone https://github.com/<your-username>/fda-recall-tracker.git
cd fda-recall-tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the script
python fetch_fda_recalls.py
```

Output files are saved to the `/output` folder as timestamped `.csv` and `.txt` files.

## Tech used

- Python
- `requests` (API calls)
- `pandas` (data cleaning)
- GitHub Actions (scheduled automation)

## Sample output

See the `/output` folder for the most recent auto-generated report.
