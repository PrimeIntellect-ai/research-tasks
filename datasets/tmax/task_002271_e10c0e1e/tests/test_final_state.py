# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

def test_recovered_db_exists_and_valid():
    """Verify that /home/user/recovered.db exists and is a valid SQLite database with the expected schema."""
    db_path = '/home/user/recovered.db'
    assert os.path.exists(db_path), f"File {db_path} does not exist."
    assert os.path.isfile(db_path), f"{db_path} is not a file."

    # Check if it's a valid SQLite database by querying it
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(value) FROM measurements;")
        result = cursor.fetchone()[0]
        conn.close()
        assert result is not None, "The measurements table is empty or missing."
    except sqlite3.Error as e:
        pytest.fail(f"Failed to open or query {db_path} as a SQLite database: {e}")

def test_result_txt_content():
    """Verify that /home/user/result.txt contains exactly the expected rounded sum."""
    result_path = '/home/user/result.txt'
    assert os.path.exists(result_path), f"File {result_path} does not exist."
    assert os.path.isfile(result_path), f"{result_path} is not a file."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content == "60.60", f"Expected result.txt to contain '60.60', but found '{content}'"

def test_run_sensor_process_still_running():
    """Verify that run_sensor.sh is still running in the background (was not killed)."""
    try:
        output = subprocess.check_output(['pgrep', '-f', 'run_sensor.sh'], text=True)
        assert output.strip() != "", "run_sensor.sh process was killed, but the instructions said not to kill it."
    except subprocess.CalledProcessError:
        pytest.fail("run_sensor.sh process was killed, but the instructions said not to kill it.")