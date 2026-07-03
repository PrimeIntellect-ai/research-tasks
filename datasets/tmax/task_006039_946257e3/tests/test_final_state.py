# test_final_state.py
import os
import sqlite3
import csv

def test_longest_chain():
    chain_file = '/home/user/longest_chain.txt'
    assert os.path.exists(chain_file), f"File {chain_file} is missing."

    with open(chain_file, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"Content of {chain_file} is not an integer: {content}"
    assert int(content) == 5, f"Expected longest chain to be 5, but got {content}."

def test_index_exists():
    db_path = '/home/user/backup_meta.db'
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='index' AND name='idx_backup_perf'")
    row = cur.fetchone()

    conn.close()

    assert row is not None, "Index 'idx_backup_perf' was not found in the database."
    assert row[0] == 'backups', f"Index 'idx_backup_perf' should be on table 'backups', but is on '{row[0]}'."

def test_report_output():
    report_file = '/home/user/report_output.csv'
    assert os.path.exists(report_file), f"Report output file {report_file} is missing."

    with open(report_file, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"Report file {report_file} is empty."

    header = rows[0]
    expected_header = ['cluster_name', 'backup_id', 'size_bytes', 'rolling_avg_size']
    assert header == expected_header, f"Expected header {expected_header}, got {header}."

    # Recompute the expected results from the database to be robust
    db_path = '/home/user/backup_meta.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = """
        SELECT 
            c.name as cluster_name, 
            b.id as backup_id, 
            b.size_bytes,
            AVG(b.size_bytes) OVER (
                PARTITION BY c.name 
                ORDER BY b.timestamp ASC 
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) as rolling_avg_size
        FROM backups b
        JOIN storage_nodes s ON b.storage_node_id = s.id
        JOIN clusters c ON s.cluster_id = c.id
        WHERE b.status = 'SUCCESS'
    """

    cur.execute(query)
    db_rows = cur.fetchall()
    conn.close()

    # Format expected rows to match CSV string outputs
    expected_data = set()
    for row in db_rows:
        cluster_name = row[0]
        backup_id = str(row[1])
        size_bytes = str(row[2])
        rolling_avg = float(row[3])
        # Round to 2 decimal places as required
        rolling_avg_str = str(round(rolling_avg, 2))
        expected_data.add((cluster_name, backup_id, size_bytes, rolling_avg_str))

    actual_data = set()
    for row in rows[1:]:
        assert len(row) == 4, f"Row {row} does not have exactly 4 columns."
        cluster_name, backup_id, size_bytes, rolling_avg_str = row
        # Normalize float representation for comparison
        rolling_avg_float = float(rolling_avg_str)
        actual_data.add((cluster_name, backup_id, size_bytes, str(round(rolling_avg_float, 2))))

    assert actual_data == expected_data, f"Report data does not match expected output.\nExpected: {expected_data}\nActual: {actual_data}"