# test_final_state.py

import os
import csv
import hashlib
import pytest

AUDIT_RESULTS_FILE = "/home/user/audit_results.csv"
WEBAPP_DIR = "/home/user/webapp"
INDEX_FILE = os.path.join(WEBAPP_DIR, "index.html")
DASHBOARD_FILE = os.path.join(WEBAPP_DIR, "dashboard.html")

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def test_audit_results_file_exists():
    assert os.path.isfile(AUDIT_RESULTS_FILE), f"The audit report {AUDIT_RESULTS_FILE} does not exist."

def test_audit_results_format_and_content():
    assert os.path.isfile(AUDIT_RESULTS_FILE), f"The audit report {AUDIT_RESULTS_FILE} does not exist."

    with open(AUDIT_RESULTS_FILE, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"The file {AUDIT_RESULTS_FILE} is empty."

    header = rows[0]
    expected_header = ["Filename", "Vulnerability", "Current_SHA256"]
    assert header == expected_header, f"Header is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]

    # Check sorting
    filenames = [row[0] for row in data_rows if len(row) > 0]
    assert filenames == sorted(filenames), "The CSV data rows are not sorted alphabetically by Filename."

    # Compute expected hashes dynamically
    index_hash = compute_sha256(INDEX_FILE)
    dashboard_hash = compute_sha256(DASHBOARD_FILE)

    assert index_hash is not None, f"Expected {INDEX_FILE} to exist to compute its hash."
    assert dashboard_hash is not None, f"Expected {DASHBOARD_FILE} to exist to compute its hash."

    expected_data = [
        ["dashboard.html", "CSP", dashboard_hash],
        ["index.html", "XSS", index_hash]
    ]

    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} data rows, but got {len(data_rows)}. Ensure you are filtering files correctly based on permissions, hash mismatch, and content."

    for i, expected_row in enumerate(expected_data):
        assert data_rows[i] == expected_row, f"Row {i+1} is incorrect. Expected {expected_row}, got {data_rows[i]}."