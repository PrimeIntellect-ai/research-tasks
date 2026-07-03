# test_final_state.py

import os
import subprocess
import sqlite3
import pytest

PROJECT_DIR = "/home/user/project"
SETUP_SCRIPT = os.path.join(PROJECT_DIR, "setup_and_run.sh")
RUN_CALC_SCRIPT = os.path.join(PROJECT_DIR, "run_calc.sh")
API_HANDLER_SCRIPT = os.path.join(PROJECT_DIR, "api_handler.sh")
DB_PATH = os.path.join(PROJECT_DIR, "data.db")

@pytest.fixture(scope="session", autouse=True)
def run_setup_script():
    """Ensure the setup script exists, is executable, and run it."""
    assert os.path.isfile(SETUP_SCRIPT), f"Setup script missing: {SETUP_SCRIPT}"
    assert os.access(SETUP_SCRIPT, os.X_OK), f"Setup script is not executable: {SETUP_SCRIPT}"

    result = subprocess.run([SETUP_SCRIPT], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Setup script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_db_migration():
    """Test that the database migrations were applied correctly."""
    assert os.path.isfile(DB_PATH), f"Database file missing: {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT factor FROM settings;")
        row = cursor.fetchone()
        assert row is not None, "No data found in 'settings' table."
        assert row[0] == 7, f"Expected factor to be 7, got {row[0]}."
    except sqlite3.OperationalError as e:
        pytest.fail(f"Database query failed, migrations might not be applied correctly: {e}")
    finally:
        conn.close()

def test_run_calc_wrapper():
    """Test that run_calc.sh correctly sets the environment and runs the calculator with v1 lib."""
    assert os.path.isfile(RUN_CALC_SCRIPT), f"Wrapper script missing: {RUN_CALC_SCRIPT}"
    assert os.access(RUN_CALC_SCRIPT, os.X_OK), f"Wrapper script is not executable: {RUN_CALC_SCRIPT}"

    result = subprocess.run([RUN_CALC_SCRIPT, "5"], capture_output=True, text=True)
    assert result.returncode == 0, f"run_calc.sh failed with return code {result.returncode}."

    output = result.stdout.strip()
    assert output == "10", f"Expected output '10' from run_calc.sh 5, got '{output}'."

def test_api_handler_valid_request():
    """Test that api_handler.sh correctly processes a valid GET /calculate request."""
    assert os.path.isfile(API_HANDLER_SCRIPT), f"API handler script missing: {API_HANDLER_SCRIPT}"
    assert os.access(API_HANDLER_SCRIPT, os.X_OK), f"API handler script is not executable: {API_HANDLER_SCRIPT}"

    http_request = "GET /calculate HTTP/1.1\r\nHost: localhost\r\n\r\n"

    result = subprocess.run(
        [API_HANDLER_SCRIPT], 
        input=http_request, 
        capture_output=True, 
        text=True
    )

    assert result.returncode == 0, f"api_handler.sh failed with return code {result.returncode}."

    output = result.stdout
    assert "HTTP/1.1 200 OK" in output, "Expected HTTP/1.1 200 OK in response."

    # The output should contain the JSON result
    # factor is 7, v1 doubles it -> 14
    expected_json = '{"result": 14}'
    # Remove all whitespace to make the check robust against formatting differences
    output_no_space = "".join(output.split())
    expected_no_space = "".join(expected_json.split())

    assert expected_no_space in output_no_space, f"Expected JSON body '{expected_json}' in response. Got: {output}"

def test_api_handler_invalid_request():
    """Test that api_handler.sh correctly returns 404 for an invalid request."""
    assert os.path.isfile(API_HANDLER_SCRIPT), f"API handler script missing: {API_HANDLER_SCRIPT}"

    http_request = "GET /other HTTP/1.1\r\nHost: localhost\r\n\r\n"

    result = subprocess.run(
        [API_HANDLER_SCRIPT], 
        input=http_request, 
        capture_output=True, 
        text=True
    )

    output = result.stdout
    assert "HTTP/1.1 404 Not Found" in output, f"Expected HTTP/1.1 404 Not Found in response. Got: {output}"