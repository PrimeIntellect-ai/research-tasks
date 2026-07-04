# test_final_state.py

import os
import csv
import sqlite3
import pytest

DB_PATH = '/home/user/network.db'
OUTPUT_CSV_PATH = '/home/user/top_nodes.csv'

def get_expected_results(db_path):
    """
    Recomputes the expected results from the SQLite database.
    This ensures we match the exact intent of the rubric.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Deduplicate Edges
    # 2. Calculate Total Degree
    # 3. Rank Nodes
    # 4. Extract Top Nodes

    query = """
    WITH DedupedEdges AS (
        SELECT src, dst
        FROM edges
        GROUP BY src, dst
        HAVING timestamp = MAX(timestamp)
    ),
    NodeDegrees AS (
        SELECT n.id AS node_id, n.department,
               (SELECT COUNT(*) FROM DedupedEdges e WHERE e.src = n.id) +
               (SELECT COUNT(*) FROM DedupedEdges e WHERE e.dst = n.id) AS total_degree
        FROM nodes n
    ),
    RankedNodes AS (
        SELECT department, node_id, total_degree,
               DENSE_RANK() OVER (PARTITION BY department ORDER BY total_degree DESC) AS rank
        FROM NodeDegrees
    )
    SELECT department, node_id, total_degree, rank
    FROM RankedNodes
    WHERE rank <= 3
    ORDER BY department ASC, rank ASC, node_id ASC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def test_csv_exists():
    """Test if the output CSV file exists."""
    assert os.path.isfile(OUTPUT_CSV_PATH), f"Output CSV file {OUTPUT_CSV_PATH} is missing."

def test_csv_content_and_format():
    """Test if the CSV content exactly matches the expected recomputed truth and format requirements."""
    assert os.path.isfile(OUTPUT_CSV_PATH), "Cannot test content: CSV file is missing."

    expected_data = get_expected_results(DB_PATH)

    with open(OUTPUT_CSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("CSV file is empty.")

        expected_header = ['department', 'node_id', 'total_degree', 'rank']
        assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}."

        student_data = []
        for row_num, row in enumerate(reader, start=2):
            assert len(row) == 4, f"Row {row_num} does not have exactly 4 columns: {row}"
            student_data.append({
                'department': row[0],
                'node_id': row[1],
                'total_degree': int(row[2]),
                'rank': int(row[3])
            })

    assert len(student_data) == len(expected_data), \
        f"Expected {len(expected_data)} rows in CSV, but found {len(student_data)}."

    for i, (student_row, expected_row) in enumerate(zip(student_data, expected_data)):
        assert student_row == expected_row, \
            f"Row {i+2} mismatch. Expected {expected_row}, got {student_row}."