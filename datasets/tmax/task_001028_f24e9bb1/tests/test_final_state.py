# test_final_state.py

import os
import math
import sqlite3
import pytest

PROJECT_DIR = "/home/user/project"
DB_PATH = os.path.join(PROJECT_DIR, "db.sqlite3")
SOLUTION_FILE = os.path.join(PROJECT_DIR, "solution.txt")
WS_LOG = os.path.join(PROJECT_DIR, "ws_success.log")
SOLVER_EXE = os.path.join(PROJECT_DIR, "solver")

def get_expected_angle():
    V = 40.0
    g = 9.81
    best_angle = -1

    for theta in range(1, 90):
        rad = math.radians(theta)
        R = (V * V * math.sin(2 * rad)) / g
        H = (V * V * math.sin(rad) * math.sin(rad)) / (2 * g)

        if 99.0 <= R <= 101.0 and H <= 25.0:
            if theta > best_angle:
                best_angle = theta

    return best_angle

def test_solution_file():
    assert os.path.exists(SOLUTION_FILE), f"Solution file {SOLUTION_FILE} does not exist."
    with open(SOLUTION_FILE, "r") as f:
        content = f.read().strip()

    expected_angle = get_expected_angle()
    assert content == str(expected_angle), f"Expected solution file to contain {expected_angle}, but found '{content}'."

def test_database_updated():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if max_angle column exists
    cursor.execute("PRAGMA table_info(configurations);")
    columns = [col[1] for col in cursor.fetchall()]
    assert "max_angle" in columns, "The 'max_angle' column was not added to the 'configurations' table."

    # Check if the value is updated correctly
    cursor.execute("SELECT max_angle FROM configurations WHERE id=1;")
    row = cursor.fetchone()
    assert row is not None, "Row with id=1 does not exist in 'configurations' table."

    expected_angle = get_expected_angle()
    assert row[0] == expected_angle, f"Expected max_angle to be {expected_angle}, but got {row[0]}."

    conn.close()

def test_websocket_success():
    assert os.path.exists(WS_LOG), f"WebSocket success log {WS_LOG} does not exist. Did you send the correct JSON payload?"
    with open(WS_LOG, "r") as f:
        content = f.read().strip()

    expected_angle = get_expected_angle()
    expected_log = f"Received angle: {expected_angle}"
    assert content == expected_log, f"Expected websocket log to be '{expected_log}', but got '{content}'."

def test_c_executable_exists():
    assert os.path.exists(SOLVER_EXE), f"Compiled solver executable {SOLVER_EXE} does not exist."
    assert os.access(SOLVER_EXE, os.X_OK), f"The file {SOLVER_EXE} is not executable."