# test_final_state.py

import os
import sqlite3
import pytest

OUTPUT_PATH = '/home/user/report_output.txt'
DB_PATH = '/home/user/backups.db'

def get_expected_output():
    if not os.path.exists(DB_PATH):
        pytest.fail(f"Database {DB_PATH} is missing, cannot compute truth.")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Total Size Per Region
    cur.execute("""
        SELECT n.region, SUM(b.size_gb) 
        FROM nodes n 
        JOIN backups b ON n.node_id = b.node_id 
        GROUP BY n.region 
        ORDER BY n.region
    """)
    totals = cur.fetchall()

    # 2. Top 2 Backups Per Region
    cur.execute("""
        WITH Ranked AS (
            SELECT n.region, b.backup_id, b.size_gb,
                   ROW_NUMBER() OVER(PARTITION BY n.region ORDER BY b.size_gb DESC, b.backup_id ASC) as rn
            FROM nodes n
            JOIN backups b ON n.node_id = b.node_id
        )
        SELECT region, backup_id, size_gb
        FROM Ranked
        WHERE rn <= 2
        ORDER BY region ASC, size_gb DESC
    """)
    top_backups = cur.fetchall()

    # 3. Shortest Path A to F
    cur.execute("""
        WITH RECURSIVE paths(target, total_latency) AS (
            SELECT target, latency_ms FROM network_links WHERE source = 'A'
            UNION ALL
            SELECT nl.target, p.total_latency + nl.latency_ms
            FROM paths p
            JOIN network_links nl ON p.target = nl.source
        )
        SELECT MIN(total_latency) FROM paths WHERE target = 'F'
    """)
    shortest_path = cur.fetchone()[0]

    conn.close()

    lines = []
    lines.append("--- Total Size Per Region ---")
    for region, total in totals:
        lines.append(f"{region}: {total} GB")

    lines.append("--- Top 2 Backups Per Region ---")
    for region, backup_id, size_gb in top_backups:
        lines.append(f"{region} - {backup_id}: {size_gb} GB")

    lines.append("--- Shortest Path A to F ---")
    lines.append(f"Total Latency: {shortest_path} ms")

    return "\n".join(lines) + "\n"

def test_output_file_exists():
    """Check if the report output file was generated."""
    assert os.path.isfile(OUTPUT_PATH), f"Expected output file not found at {OUTPUT_PATH}. Did the script run?"

def test_output_contents():
    """Verify the contents of the report output file match the expected metrics and format."""
    expected_content = get_expected_output().strip()

    with open(OUTPUT_PATH, 'r') as f:
        actual_content = f.read().strip()

    # Split into lines for better error reporting
    expected_lines = expected_content.splitlines()
    actual_lines = actual_content.splitlines()

    assert len(actual_lines) == len(expected_lines), (
        f"Output line count mismatch. Expected {len(expected_lines)} lines, got {len(actual_lines)}."
    )

    for i, (expected_line, actual_line) in enumerate(zip(expected_lines, actual_lines)):
        assert actual_line == expected_line, (
            f"Mismatch on line {i+1}.\nExpected: '{expected_line}'\nActual:   '{actual_line}'"
        )