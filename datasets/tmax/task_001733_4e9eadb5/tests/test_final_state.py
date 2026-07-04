# test_final_state.py

import os
import stat
import sqlite3
import json
from collections import defaultdict

SCRIPT_PATH = "/home/user/generate_report.sh"
REPORT_PATH = "/home/user/report.csv"
DB_PATH = "/home/user/app.db"

def test_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable by the owner."

def test_report_exists():
    """Test that the report CSV file was generated."""
    assert os.path.isfile(REPORT_PATH), f"Report {REPORT_PATH} does not exist."

def get_expected_report():
    """Helper to recompute the expected report directly from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Build account hierarchy
    cursor.execute("SELECT account_id, parent_account_id FROM accounts")
    accounts = cursor.fetchall()
    parent_map = {acc[0]: acc[1] for acc in accounts}

    def get_root(acc_id):
        curr = acc_id
        while parent_map.get(curr) is not None:
            curr = parent_map[curr]
        return curr

    roots = {acc[0]: get_root(acc[0]) for acc in accounts}

    # Process logs
    cursor.execute("SELECT account_id, data, created_at FROM logs")
    logs = cursor.fetchall()
    conn.close()

    account_logs = defaultdict(list)
    for acc_id, data_str, created_at in logs:
        try:
            data = json.loads(data_str)
            qt = data.get("query_time_ms", 0)
        except Exception:
            qt = 0
        account_logs[acc_id].append((created_at, qt))

    results = []
    for acc_id, log_entries in account_logs.items():
        # Sort by created_at
        log_entries.sort(key=lambda x: x[0])
        max_rolling = 0
        for i in range(len(log_entries)):
            if i == 0:
                rolling = log_entries[i][1]
            else:
                rolling = log_entries[i][1] + log_entries[i-1][1]
            if rolling > max_rolling:
                max_rolling = rolling

        if max_rolling > 100:
            results.append((acc_id, roots[acc_id], max_rolling))

    # Sort by max_rolling_query_time DESC, then account_id ASC
    results.sort(key=lambda x: (-x[2], x[0]))

    # Paginate to top 5
    results = results[:5]

    return [f"{r[0]},{r[1]},{r[2]}" for r in results]

def test_report_content():
    """Test that the report CSV contains exactly the expected data."""
    with open(REPORT_PATH, "r") as f:
        content = f.read().strip()

    expected_lines = get_expected_report()
    actual_lines = [line.strip() for line in content.split("\n") if line.strip()]

    assert actual_lines == expected_lines, (
        f"Report content is incorrect.\n"
        f"Expected:\n{expected_lines}\n\n"
        f"Got:\n{actual_lines}"
    )