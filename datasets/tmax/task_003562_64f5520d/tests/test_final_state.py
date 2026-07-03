# test_final_state.py

import os
import sys
import time
import sqlite3
import multiprocessing
import pytest

def worker():
    """Worker function for the benchmark."""
    sys.path.insert(0, '/home/user')
    try:
        from query_api import get_customer_summary
    except ImportError:
        sys.exit(1)

    for _ in range(500):
        get_customer_summary('/home/user/analytics.db', 'CUST_001', 1, 10)

def test_database_and_api_exist():
    """Check if the database and API module have been created."""
    assert os.path.exists('/home/user/analytics.db'), "Database /home/user/analytics.db not found."
    assert os.path.exists('/home/user/query_api.py'), "API module /home/user/query_api.py not found."

def test_pragmas_and_indexes():
    """Verify that the correct PRAGMAs and indexes were applied."""
    conn = sqlite3.connect('/home/user/analytics.db')
    cursor = conn.cursor()

    # Check WAL mode
    cursor.execute("PRAGMA journal_mode;")
    journal_mode = cursor.fetchone()[0].upper()
    assert journal_mode == 'WAL', f"Expected journal_mode WAL, got {journal_mode}"

    # Check synchronous mode (1 corresponds to NORMAL)
    cursor.execute("PRAGMA synchronous;")
    synchronous = cursor.fetchone()[0]
    assert str(synchronous) in ('1', 'NORMAL'), f"Expected synchronous NORMAL (1), got {synchronous}"

    # Check indexes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
    indexes = [row[0] for row in cursor.fetchall() if row[0] is not None]
    assert 'idx_cust_date' in indexes, "Index 'idx_cust_date' is missing."
    assert 'idx_cust_amount' in indexes, "Index 'idx_cust_amount' is missing."

    conn.close()

def test_performance_metric():
    """Benchmark the query API under concurrency and verify execution time is within the threshold."""
    sys.path.insert(0, '/home/user')
    try:
        import query_api
    except ImportError:
        pytest.fail("Could not import query_api.py from /home/user")

    start = time.time()
    processes = [multiprocessing.Process(target=worker) for _ in range(4)]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    duration = time.time() - start

    # Check if any process failed (e.g., due to an exception in the worker)
    for p in processes:
        assert p.exitcode == 0, f"A worker process failed with exit code {p.exitcode}"

    assert duration <= 2.0, f"Performance metric failed: execution time {duration:.3f}s > 2.0s threshold."