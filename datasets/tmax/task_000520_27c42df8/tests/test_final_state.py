# test_final_state.py

import os
import subprocess
import pytest

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def get_expected_data():
    input_file = "/home/user/etl_data.tsv"
    if not os.path.exists(input_file):
        return [], 0, 0, 0

    records = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 4:
                records.append({
                    'id': parts[0],
                    'category': parts[1],
                    'timestamp': int(parts[2]),
                    'message': parts[3],
                    'original': line
                })

    total_input = len(records)

    # Group by category
    categories = {}
    for r in records:
        categories.setdefault(r['category'], []).append(r)

    kept_records = []
    for cat in sorted(categories.keys()):
        # Sort by timestamp
        cat_records = sorted(categories[cat], key=lambda x: x['timestamp'])
        kept_for_cat = []
        for r in cat_records:
            is_duplicate = False
            for kept in kept_for_cat:
                if levenshtein(r['message'], kept['message']) <= 3:
                    is_duplicate = True
                    break
            if not is_duplicate:
                kept_for_cat.append(r)
                kept_records.append(r)

    total_cleaned = len(kept_records)
    total_dropped = total_input - total_cleaned

    return kept_records, total_input, total_cleaned, total_dropped

def test_cleaned_data():
    """Check that cleaned_data.tsv contains the correctly deduplicated records."""
    cleaned_file = "/home/user/cleaned_data.tsv"
    assert os.path.exists(cleaned_file), f"{cleaned_file} does not exist."

    expected_records, _, _, _ = get_expected_data()
    expected_ids = {r['id'] for r in expected_records}

    actual_ids = []
    with open(cleaned_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                actual_ids.append(line.split('\t')[0])

    assert set(actual_ids) == expected_ids, f"Cleaned data IDs {set(actual_ids)} do not match expected {expected_ids}."
    assert len(actual_ids) == len(expected_ids), "Cleaned data contains duplicates or incorrect number of records."

def test_report_content():
    """Check that report.txt contains the correct summary."""
    report_file = "/home/user/report.txt"
    assert os.path.exists(report_file), f"{report_file} does not exist."

    _, total_input, total_cleaned, total_dropped = get_expected_data()
    expected_report = f"""=== ETL Deduplication Report ===
Total Input Records: {total_input}
Total Cleaned Records: {total_cleaned}
Total Duplicates Dropped: {total_dropped}
================================"""

    with open(report_file, 'r') as f:
        actual_report = f.read().strip()

    assert actual_report == expected_report, "Report content does not match the expected template and counts."

def test_cron_scheduling():
    """Check that the script is scheduled in crontab to run at 3:15 AM every day."""
    try:
        # Check crontab for the current user
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        crontab_content = ""

    # Also check /var/spool/cron/crontabs/user if running as root
    if not crontab_content and os.path.exists('/var/spool/cron/crontabs/user'):
        with open('/var/spool/cron/crontabs/user', 'r') as f:
            crontab_content = f.read()

    assert "15 3 * * *" in crontab_content, "Cron schedule '15 3 * * *' not found in crontab."
    assert "clean_pipeline.sh" in crontab_content, "Script 'clean_pipeline.sh' not found in crontab."