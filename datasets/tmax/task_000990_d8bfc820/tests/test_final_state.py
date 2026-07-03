# test_final_state.py
import os
import subprocess
import urllib.request
import urllib.error
import time
import sqlite3
import pytest

def test_recovered_database_exists_and_valid():
    recovered_db_path = "/home/user/app/data/recovered_cache.db"
    assert os.path.isfile(recovered_db_path), f"Recovered database not found at {recovered_db_path}"

    # Check if it's a valid SQLite database
    try:
        conn = sqlite3.connect(recovered_db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()
        conn.close()
        assert result and result[0] == "ok", "Recovered database failed integrity check."
    except sqlite3.Error as e:
        pytest.fail(f"Failed to open recovered database or run integrity check: {e}")

def test_services_are_running():
    # Check if port 8000 (Flask) is listening
    flask_up = False
    for _ in range(5):
        try:
            urllib.request.urlopen("http://localhost:8000/", timeout=1)
            flask_up = True
            break
        except urllib.error.URLError as e:
            # If it's a 404 or 500, the server is up. If it's connection refused, it's down.
            if hasattr(e, 'code'):
                flask_up = True
                break
            time.sleep(1)

    assert flask_up, "Flask API Gateway is not responding on port 8000."

def test_pricing_accuracy_mse():
    verify_script = "/home/user/verify_metric.py"

    if os.path.isfile(verify_script):
        # Run the provided verification script
        result = subprocess.run(["python3", verify_script], capture_output=True, text=True)
        assert result.returncode == 0, f"Verification script failed: {result.stderr}"

        # Parse MSE from stdout
        output = result.stdout.strip()
        try:
            # Assuming the script prints the MSE as a float somewhere in the output
            # We'll look for the last float in the output
            words = output.split()
            mse_val = None
            for word in reversed(words):
                try:
                    mse_val = float(word)
                    break
                except ValueError:
                    continue

            assert mse_val is not None, f"Could not parse MSE from output: {output}"

            threshold = 1e-8
            assert mse_val <= threshold, f"MSE {mse_val} is greater than threshold {threshold}"
        except Exception as e:
            pytest.fail(f"Failed to evaluate MSE: {e}. Output was: {output}")
    else:
        # Fallback if the script isn't available, try to hit the API directly to ensure it works
        try:
            req = urllib.request.urlopen("http://localhost:8000/price?id=1", timeout=2)
            assert req.getcode() == 200, "API did not return 200 OK for /price?id=1"
        except Exception as e:
            pytest.fail(f"API request failed: {e}")