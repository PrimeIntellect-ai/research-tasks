# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/graph.db"
RANK_FILE = "/home/user/rank.txt"
ERROR_FILE = "/home/user/error.txt"
CPP_FILE = "/home/user/pipeline.cpp"
SH_FILE = "/home/user/run.sh"

def test_files_exist():
    """Verify that the required source and output files exist."""
    assert os.path.isfile(CPP_FILE), f"Source file {CPP_FILE} is missing."
    assert os.path.isfile(SH_FILE), f"Bash script {SH_FILE} is missing."
    assert os.path.isfile(RANK_FILE), f"Output file {RANK_FILE} is missing."
    assert os.path.isfile(ERROR_FILE), f"Output file {ERROR_FILE} is missing."

def test_database_index_exists():
    """Verify that the composite index idx_edges_src_dst was created."""
    assert os.path.isfile(DB_PATH), f"Database {DB_PATH} is missing."
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_edges_src_dst';"
        )
        result = cursor.fetchone()
        assert result is not None, "Index 'idx_edges_src_dst' was not found in the database."
        assert result[0] == "idx_edges_src_dst"

def test_database_inserted_edge():
    """Verify that the new edge (100, 200, 1.5) was inserted."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT weight FROM edges WHERE src=100 AND dst=200;")
        result = cursor.fetchone()
        assert result is not None, "The edge with src=100 and dst=200 was not found."
        assert abs(result[0] - 1.5) < 1e-5, f"Expected weight 1.5, but got {result[0]}."

def test_rank_output():
    """Verify that the DENSE_RANK of node 200 is correct in rank.txt."""
    with open(RANK_FILE, "r") as f:
        content = f.read().strip()

    # Based on the initial data and the new insertion:
    # dst 300: 10.0
    # dst 200: 5.0 + 2.0 + 1.5 = 8.5
    # dst 400: 8.0
    # Dense ranks descending: 1 -> 10.0, 2 -> 8.5, 3 -> 8.0
    # So node 200 has rank 2.
    assert content == "2", f"Expected rank.txt to contain '2', but got '{content}'."

def test_error_output():
    """Verify that the SQLITE_BUSY error code (5) is captured in error.txt."""
    with open(ERROR_FILE, "r") as f:
        content = f.read().strip()

    assert content == "5", f"Expected error.txt to contain '5' (SQLITE_BUSY), but got '{content}'."