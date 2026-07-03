# test_final_state.py

import os
import sqlite3
import pytest

def test_c_file_exists_and_includes_sqlite():
    """Check if resolver.c exists and includes sqlite3.h."""
    c_file_path = "/home/user/resolver.c"
    assert os.path.exists(c_file_path), f"C source file {c_file_path} does not exist."

    with open(c_file_path, "r") as f:
        content = f.read()

    assert "#include" in content and "sqlite3.h" in content, "resolver.c does not seem to include sqlite3.h."

def test_executable_exists():
    """Check if the compiled executable exists."""
    exe_path = "/home/user/resolver"
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_index_created():
    """Check if an index was created on the dependencies table."""
    db_path = "/home/user/backup_graph.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='dependencies';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No index was created on the 'dependencies' table."

def test_output_file_correct():
    """Check if the backup_plan.log matches the expected output."""
    log_path = "/home/user/backup_plan.log"
    assert os.path.exists(log_path), f"Output file {log_path} does not exist."

    expected_lines = [
        "Phase 0: storage-array",
        "Phase 1: db-primary",
        "Phase 2: cache-node",
        "Phase 2: db-replica",
        "Phase 3: app-server-1",
        "Phase 3: app-server-2",
        "Phase 4: load-balancer"
    ]

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."