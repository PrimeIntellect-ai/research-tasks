# test_final_state.py
import os
import sqlite3
import subprocess
import json
import stat

def test_database_exists():
    """Check if the SQLite database was created."""
    db_path = "/home/user/sensors.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

def test_database_table_exists():
    """Check if the readings table exists and has data."""
    db_path = "/home/user/sensors.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings';")
        table = cursor.fetchone()
        assert table is not None, "Table 'readings' does not exist in the database."

        cursor.execute("SELECT COUNT(*) FROM readings;")
        count = cursor.fetchone()[0]
        assert count > 0, "Table 'readings' is empty."
    finally:
        conn.close()

def test_script_exists_and_executable():
    """Check if the bash script exists and is executable."""
    script_path = "/home/user/get_latest.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_script_output_sens_02():
    """Check the output of the script for SENS-02."""
    script_path = "/home/user/get_latest.sh"

    result = subprocess.run([script_path, "SENS-02"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    assert output, "Script produced no output."

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        assert False, f"Script output is not valid JSON. Output: {output}"

    expected_data = {
        "id": "SENS-02",
        "latest_reading": {
            "time": "2023-10-01T12:00:00Z",
            "temp": 24,
            "hum": 42
        }
    }

    # We allow temp and hum to be floats or ints, as long as they are numerically equal
    assert data.get("id") == expected_data["id"], "Incorrect sensor ID in output."
    assert "latest_reading" in data, "Missing 'latest_reading' in output."
    assert data["latest_reading"].get("time") == expected_data["latest_reading"]["time"], "Incorrect time in output."
    assert float(data["latest_reading"].get("temp", 0)) == float(expected_data["latest_reading"]["temp"]), "Incorrect temperature in output."
    assert float(data["latest_reading"].get("hum", 0)) == float(expected_data["latest_reading"]["hum"]), "Incorrect humidity in output."

def test_script_output_sens_03():
    """Check the output of the script for SENS-03 to ensure it handles other sensors correctly."""
    script_path = "/home/user/get_latest.sh"

    result = subprocess.run([script_path, "SENS-03"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    assert output, "Script produced no output."

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        assert False, f"Script output is not valid JSON. Output: {output}"

    expected_data = {
        "id": "SENS-03",
        "latest_reading": {
            "time": "2023-10-02T08:00:00Z",
            "temp": 19,
            "hum": 55
        }
    }

    assert data.get("id") == expected_data["id"], "Incorrect sensor ID in output."
    assert "latest_reading" in data, "Missing 'latest_reading' in output."
    assert data["latest_reading"].get("time") == expected_data["latest_reading"]["time"], "Incorrect time in output."
    assert float(data["latest_reading"].get("temp", 0)) == float(expected_data["latest_reading"]["temp"]), "Incorrect temperature in output."
    assert float(data["latest_reading"].get("hum", 0)) == float(expected_data["latest_reading"]["hum"]), "Incorrect humidity in output."