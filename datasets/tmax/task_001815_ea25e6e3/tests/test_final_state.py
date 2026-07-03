# test_final_state.py

import os
import sqlite3
import re

DB_PATH = "/home/user/sensors.db"
REPORT_PATH = "/home/user/report.txt"

def test_database_exists_and_schema():
    assert os.path.exists(DB_PATH), f"Database not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cleaned_data'")
    table = cursor.fetchone()
    assert table is not None, "Table 'cleaned_data' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(cleaned_data)")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    assert 'timestamp' in columns, "Column 'timestamp' missing."
    assert 'temp_c' in columns, "Column 'temp_c' missing."
    assert 'humidity_pct' in columns, "Column 'humidity_pct' missing."

    conn.close()

def test_database_contents():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, temp_c, humidity_pct FROM cleaned_data ORDER BY timestamp")
    rows = cursor.fetchall()

    assert len(rows) == 13, f"Expected exactly 13 rows (10:00 to 11:00 inclusive at 5-min intervals), got {len(rows)}"

    timestamps = [row[0] for row in rows]
    assert timestamps[0] == "2023-10-01 10:00:00", "First timestamp should be '2023-10-01 10:00:00'"
    assert timestamps[-1] == "2023-10-01 11:00:00", "Last timestamp should be '2023-10-01 11:00:00'"

    # Check specific aggregated/interpolated values
    # 10:00 bin: 10:01 (20, 40) and 10:04:30 (21, 42) -> mean: Temp 20.5, Hum 41.0
    cursor.execute("SELECT temp_c, humidity_pct FROM cleaned_data WHERE timestamp='2023-10-01 10:00:00'")
    row_10_00 = cursor.fetchone()
    assert row_10_00 is not None
    assert abs(row_10_00[0] - 20.5) < 1e-5, f"Expected temp 20.5 at 10:00, got {row_10_00[0]}"
    assert abs(row_10_00[1] - 41.0) < 1e-5, f"Expected humidity 41.0 at 10:00, got {row_10_00[1]}"

    # 10:05 bin: interpolated
    cursor.execute("SELECT temp_c FROM cleaned_data WHERE timestamp='2023-10-01 10:05:00'")
    row_10_05 = cursor.fetchone()
    assert row_10_05 is not None
    assert abs(row_10_05[0] - 21.333) < 0.1, f"Expected interpolated temp ~21.33 at 10:05, got {row_10_05[0]}"

    # 10:25 bin: 10:26 (25.0, 50.0) -> mean: Temp 25.0, Hum 50.0
    cursor.execute("SELECT temp_c, humidity_pct FROM cleaned_data WHERE timestamp='2023-10-01 10:25:00'")
    row_10_25 = cursor.fetchone()
    assert row_10_25 is not None
    assert abs(row_10_25[0] - 25.0) < 1e-5, f"Expected temp 25.0 at 10:25, got {row_10_25[0]}"
    assert abs(row_10_25[1] - 50.0) < 1e-5, f"Expected humidity 50.0 at 10:25, got {row_10_25[1]}"

    conn.close()

def test_report_contents():
    assert os.path.exists(REPORT_PATH), f"Report not found at {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        content = f.read()

    assert "Server Room Environmental Report" in content, "Report title is missing."

    max_temp_match = re.search(r"Max Temperature:\s*([\d\.]+)\s*C", content)
    min_temp_match = re.search(r"Min Temperature:\s*([\d\.]+)\s*C", content)
    max_hum_match = re.search(r"Max Humidity:\s*([\d\.]+)\s*%", content)
    min_hum_match = re.search(r"Min Humidity:\s*([\d\.]+)\s*%", content)

    assert max_temp_match, "Max Temperature line missing or incorrectly formatted."
    assert min_temp_match, "Min Temperature line missing or incorrectly formatted."
    assert max_hum_match, "Max Humidity line missing or incorrectly formatted."
    assert min_hum_match, "Min Humidity line missing or incorrectly formatted."

    assert float(max_temp_match.group(1)) == 25.0, "Expected Max Temperature to be 25.0"
    assert float(min_temp_match.group(1)) == 20.5, "Expected Min Temperature to be 20.5"
    assert float(max_hum_match.group(1)) == 50.0, "Expected Max Humidity to be 50.0"
    assert float(min_hum_match.group(1)) == 41.0, "Expected Min Humidity to be 41.0"