# test_final_state.py

import os
import sqlite3

def test_analyze_c_exists():
    """Test that the C source code file exists."""
    assert os.path.isfile("/home/user/analyze.c"), "/home/user/analyze.c is missing."

def test_analyze_executable_exists():
    """Test that the compiled executable exists and is executable."""
    exe_path = "/home/user/analyze"
    assert os.path.isfile(exe_path), f"{exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_report_txt_exists():
    """Test that the report.txt file exists."""
    assert os.path.isfile("/home/user/report.txt"), "/home/user/report.txt is missing."

def test_report_txt_content():
    """Test that report.txt contains the correct output formatted as CSV."""
    expected_content = [
        "1,0,100,100",
        "2,1,50,150",
        "3,1,200,350",
        "4,2,30,380",
        "5,2,20,400",
        "6,2,10,410",
        "8,3,5,415"
    ]

    with open("/home/user/report.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_content), f"Expected {len(expected_content)} lines in report.txt, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_content)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."

def test_query_logic_in_db():
    """Test the logic independently in the database to ensure truth alignment."""
    db_path = "/home/user/research.db"
    assert os.path.isfile(db_path), f"{db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    WITH RECURSIVE tree AS (
        SELECT file_id, file_size, 0 as depth FROM files WHERE file_id = 1
        UNION ALL
        SELECT f.file_id, f.file_size, t.depth + 1
        FROM files f JOIN tree t ON f.parent_id = t.file_id
    )
    SELECT file_id, depth, file_size,
           SUM(file_size) OVER (ORDER BY depth ASC, file_id ASC) as running_total
    FROM tree;
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        expected_results = [
            (1, 0, 100, 100),
            (2, 1, 50, 150),
            (3, 1, 200, 350),
            (4, 2, 30, 380),
            (5, 2, 20, 400),
            (6, 2, 10, 410),
            (8, 3, 5, 415)
        ]
        assert results == expected_results, "Database state or query logic does not match the expected hierarchical data."
    finally:
        conn.close()