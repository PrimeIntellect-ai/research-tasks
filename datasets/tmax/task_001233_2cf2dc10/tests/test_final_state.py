# test_final_state.py

import os
import sqlite3
import json
import pytest

PROFILER_DIR = "/home/user/profiler"
LOGS_DB = os.path.join(PROFILER_DIR, "logs.db")
LOGS_DB_WAL = os.path.join(PROFILER_DIR, "logs.db-wal")
PROCESS_PY = os.path.join(PROFILER_DIR, "process.py")
SUMMARY_JSON = os.path.join(PROFILER_DIR, "summary.json")
TRACE_LOG = os.path.join(PROFILER_DIR, "trace.log")

def test_db_recovery():
    assert not os.path.exists(LOGS_DB_WAL), "logs.db-wal still exists. The WAL was not properly checkpointed and removed."

    conn = sqlite3.connect(LOGS_DB)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode;")
    mode = cursor.fetchone()[0]
    conn.close()

    assert mode.lower() == "delete", f"Expected journal_mode to be 'delete', but got '{mode}'."

def test_process_py_fixed():
    assert os.path.isfile(PROCESS_PY), f"File {PROCESS_PY} is missing."
    with open(PROCESS_PY, "r") as f:
        content = f.read()

    assert "get_lock" in content, "process.py does not appear to use .get_lock() for safe concurrent updates."
    assert "'q'" in content or '"q"' in content, "process.py does not appear to use a 64-bit integer ('q') for multiprocessing.Value."
    assert "'i'" not in content and '"i"' not in content, "process.py still contains the 32-bit integer ('i') which causes OverflowError."

def test_summary_json():
    assert os.path.isfile(SUMMARY_JSON), f"File {SUMMARY_JSON} was not generated."

    with open(SUMMARY_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{SUMMARY_JSON} is not a valid JSON file.")

    assert data.get("total_records") == 1000, f"Expected total_records to be 1000, got {data.get('total_records')}."
    assert data.get("total_metric") == 2500000000, f"Expected total_metric to be 2500000000, got {data.get('total_metric')}."

def test_trace_log():
    assert os.path.isfile(TRACE_LOG), f"File {TRACE_LOG} was not created."

    with open(TRACE_LOG, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 10, f"Expected exactly 10 lines in trace.log, got {len(lines)}."

    try:
        ids = sorted([int(line.strip()) for line in lines])
    except ValueError:
        pytest.fail("trace.log contains non-integer values.")

    expected_ids = list(range(100, 1001, 100))
    assert ids == expected_ids, f"Expected traced IDs to be {expected_ids}, but got {ids}."