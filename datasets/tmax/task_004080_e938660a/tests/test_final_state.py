# test_final_state.py

import os
import sqlite3
import statistics
import subprocess

PIPELINE_DIR = '/home/user/pipeline'
DB_PATH = os.path.join(PIPELINE_DIR, 'sensor.db')
EXEC_PATH = os.path.join(PIPELINE_DIR, 'variance')
RESULT_PATH = os.path.join(PIPELINE_DIR, 'final_result.txt')

def get_db_values():
    assert os.path.isfile(DB_PATH), f"Database not found at {DB_PATH}"
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT value FROM readings")
        rows = c.fetchall()
        conn.close()
        return [r[0] for r in rows]
    except sqlite3.Error as e:
        raise AssertionError(f"Failed to read from SQLite database at {DB_PATH}: {e}")

def test_database_restored():
    vals = get_db_values()
    assert len(vals) >= 5, f"Expected at least 5 readings in the database, found {len(vals)}"

def test_variance_executable_exists():
    assert os.path.isfile(EXEC_PATH), f"Executable not found at {EXEC_PATH}"
    assert os.access(EXEC_PATH, os.X_OK), f"File at {EXEC_PATH} is not executable"

def test_regression_script_exists():
    sh_path = os.path.join(PIPELINE_DIR, 'test_variance.sh')
    py_path = os.path.join(PIPELINE_DIR, 'test_variance.py')

    has_sh = os.path.isfile(sh_path)
    has_py = os.path.isfile(py_path)

    assert has_sh or has_py, "Neither test_variance.sh nor test_variance.py was found"

    if has_sh:
        assert os.access(sh_path, os.X_OK), f"{sh_path} is not executable"
    if has_py:
        assert os.access(py_path, os.X_OK), f"{py_path} is not executable"

def test_final_result_correct():
    assert os.path.isfile(RESULT_PATH), f"Final result file not found at {RESULT_PATH}"

    vals = get_db_values()
    expected_variance = statistics.variance(vals)
    expected_str = f"{expected_variance:.6f}"

    with open(RESULT_PATH, 'r') as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected final_result.txt to contain '{expected_str}', but found '{actual_str}'"

def test_variance_program_correctness():
    assert os.path.isfile(EXEC_PATH), "Executable missing"
    vals = get_db_values()

    input_data = "\n".join(str(v) for v in vals) + "\n"

    try:
        proc = subprocess.run([EXEC_PATH], input=input_data.encode('utf-8'), capture_output=True, check=True, timeout=2)
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"Running {EXEC_PATH} failed with exit code {e.returncode}")
    except subprocess.TimeoutExpired:
        raise AssertionError(f"Running {EXEC_PATH} timed out")

    output = proc.stdout.decode('utf-8').strip()

    expected_variance = statistics.variance(vals)
    expected_str = f"{expected_variance:.6f}"

    assert output == expected_str, f"Expected C program to output '{expected_str}', but got '{output}'"