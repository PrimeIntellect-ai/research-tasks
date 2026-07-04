# test_final_state.py

import os
import sqlite3

APP_DIR = "/home/user/app"
RESULT_FILE = os.path.join(APP_DIR, "result.txt")
DB_GO_FILE = os.path.join(APP_DIR, "db.go")
AGGREGATOR_GO_FILE = os.path.join(APP_DIR, "aggregator.go")

def test_result_file_exists_and_correct():
    assert os.path.isfile(RESULT_FILE), f"Expected result file {RESULT_FILE} does not exist. Did you run the service and redirect output?"

    with open(RESULT_FILE, "r") as f:
        content = f.read().strip()

    assert content == "Total: 1501.50", f"Expected exact output 'Total: 1501.50', but got '{content}'. Check your precision, cycle detection, and SETTLED filtering."

def test_db_go_filtering():
    assert os.path.isfile(DB_GO_FILE), f"File {DB_GO_FILE} is missing."
    with open(DB_GO_FILE, "r") as f:
        content = f.read()

    assert "SETTLED" in content, "db.go does not appear to filter transactions by the 'SETTLED' status."

def test_aggregator_go_precision_fix():
    assert os.path.isfile(AGGREGATOR_GO_FILE), f"File {AGGREGATOR_GO_FILE} is missing."
    with open(AGGREGATOR_GO_FILE, "r") as f:
        content = f.read()

    assert "float32" not in content, "aggregator.go still contains 'float32'. You must use exact integer arithmetic (cents) for accumulation to prevent precision loss."