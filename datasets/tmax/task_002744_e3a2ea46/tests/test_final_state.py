# test_final_state.py

import os
import subprocess
import sqlite3
import pytest

SCRIPT_PATH = "/home/user/analyze_risk.sh"
REPORT_PATH = "/home/user/risk_report.csv"
DB_PATH = "/home/user/financials.db"

def test_script_exists_and_executable():
    """Verify the bash script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert content.startswith("#!/bin/bash"), "Script must start with #!/bin/bash"
    assert "ACC1" not in content, "The account ID must not be hardcoded in the script"

def test_script_execution_and_output():
    """Run the script with ACC1 and verify the generated CSV report."""
    # Ensure any previous report is removed
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    # Run the script
    result = subprocess.run([SCRIPT_PATH, "ACC1"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with exit code {result.returncode}. Stderr: {result.stderr}"

    # Verify report exists
    assert os.path.exists(REPORT_PATH), f"Report not generated at {REPORT_PATH}"

    # Read and verify report content
    with open(REPORT_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "rank,path,total_amount",
        "1,ACC1->ACC5->ACC6->ACC7,560.0",
        "2,ACC1->ACC2->ACC3->ACC8,550.0",
        "3,ACC1->ACC2->ACC3->ACC4,450.0"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in CSV, got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}. Expected '{expected}', got '{actual}'"

def test_dynamic_argument_handling():
    """Run the script with a different argument to ensure it is handled dynamically."""
    # Insert a dummy path of length 3 for ACC99
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO transfers (source, target, amount) VALUES (?, ?, ?)", [
        ('ACC99', 'ACC100', 10.0),
        ('ACC100', 'ACC101', 20.0),
        ('ACC101', 'ACC102', 30.0)
    ])
    conn.commit()
    conn.close()

    try:
        # Run the script with ACC99
        result = subprocess.run([SCRIPT_PATH, "ACC99"], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed with exit code {result.returncode} for dynamic argument."

        assert os.path.exists(REPORT_PATH), "Report not generated for ACC99"

        with open(REPORT_PATH, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        expected_lines = [
            "rank,path,total_amount",
            "1,ACC99->ACC100->ACC101->ACC102,60.0"
        ]

        assert len(lines) == len(expected_lines), "Dynamic argument handling failed. Output does not match expected for ACC99."
        for actual, expected in zip(lines, expected_lines):
            assert actual == expected, f"Dynamic test mismatch. Expected '{expected}', got '{actual}'"
    finally:
        # Cleanup dummy data
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transfers WHERE source IN ('ACC99', 'ACC100', 'ACC101')")
        conn.commit()
        conn.close()