# test_final_state.py
import os
import sqlite3

def get_expected_cycles(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT c1.source_id, c2.source_id, c3.source_id
    FROM citations c1
    JOIN citations c2 ON c1.target_id = c2.source_id
    JOIN citations c3 ON c2.target_id = c3.source_id AND c3.target_id = c1.source_id
    JOIN papers p1 ON c1.source_id = p1.id
    JOIN papers p2 ON c2.source_id = p2.id
    JOIN papers p3 ON c3.source_id = p3.id
    WHERE p1.year >= 2020 AND p2.year >= 2020 AND p3.year >= 2020
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    cycles = set()
    for row in rows:
        normalized = tuple(sorted(row))
        cycles.add(normalized)

    sorted_cycles = sorted(list(cycles))
    return sorted_cycles

def test_cpp_source_exists():
    assert os.path.exists("/home/user/extract_pattern.cpp"), "C++ source file /home/user/extract_pattern.cpp is missing."

def test_executable_exists():
    exe_path = "/home/user/extract_pattern"
    assert os.path.exists(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_cycles_tsv_output():
    tsv_path = "/home/user/cycles.tsv"
    db_path = "/home/user/research_data.db"

    assert os.path.exists(tsv_path), f"Output file {tsv_path} is missing."

    expected_cycles = get_expected_cycles(db_path)

    with open(tsv_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    actual_cycles = []
    for i, line in enumerate(lines):
        parts = line.split('\t')
        assert len(parts) == 3, f"Line {i+1} in {tsv_path} does not contain exactly 3 tab-separated values: '{line}'"
        try:
            ids = tuple(int(p) for p in parts)
        except ValueError:
            assert False, f"Line {i+1} in {tsv_path} contains non-integer values: '{line}'"
        actual_cycles.append(ids)

    assert actual_cycles == expected_cycles, f"Contents of {tsv_path} do not match the expected cycles. Expected: {expected_cycles}, Actual: {actual_cycles}"