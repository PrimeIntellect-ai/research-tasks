# test_final_state.py
import os
import sqlite3
import subprocess
import tempfile
import json
import urllib.request
import urllib.error
import time
import pytest

def test_schema_migration():
    db_path = "/home/user/builds.db"
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if legacy_builds is dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='legacy_builds';")
    assert cursor.fetchone() is None, "Table 'legacy_builds' was not dropped."

    # Check if active_builds exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='active_builds';")
    assert cursor.fetchone() is not None, "Table 'active_builds' was not created."

    # Check data
    cursor.execute("SELECT repository, lang, build_cmd FROM active_builds ORDER BY repository;")
    rows = cursor.fetchall()

    expected_rows = [
        ('github.com/org/repo1', 'node', 'npm run build'),
        ('github.com/org/repo2', 'python', 'pip install -r req.txt && pytest')
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in active_builds, got {len(rows)}."
    for row, expected in zip(rows, expected_rows):
        assert row == expected, f"Row mismatch: expected {expected}, got {row}."

    conn.close()

def test_generate_env_script():
    script_path = "/home/user/generate_env.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    test_data = {
        "project": "example",
        "env": {
            "NODE_ENV": "production",
            "PORT": "3000",
            "API_KEY": "secret123"
        }
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tf:
        json.dump(test_data, tf)
        temp_path = tf.name

    try:
        result = subprocess.run([script_path, temp_path], capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        expected_output = 'export API_KEY="secret123"\nexport NODE_ENV="production"\nexport PORT="3000"'
        assert output == expected_output, f"Output of generate_env.sh is incorrect.\nExpected:\n{expected_output}\nGot:\n{output}"
    finally:
        os.remove(temp_path)

def test_nginx_running_and_header():
    # Verify custom header
    req = urllib.request.Request("http://127.0.0.1:8080/trigger", method="HEAD")
    try:
        with urllib.request.urlopen(req) as response:
            headers = response.headers
    except urllib.error.HTTPError as e:
        headers = e.headers
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to Nginx on port 8080: {e}")

    proxy_header = headers.get("X-Build-Proxy")
    assert proxy_header == "active", f"Expected X-Build-Proxy: active, got {proxy_header}"

def test_nginx_rate_limiting():
    url = "http://127.0.0.1:8080/trigger"

    # Send a request to ensure we are at the limit
    try:
        urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        pass
    except urllib.error.URLError:
        pass

    # Send another request immediately, it should be rate limited (503)
    try:
        urllib.request.urlopen(url)
        pytest.fail("Second request was not rate limited (expected 503).")
    except urllib.error.HTTPError as e:
        assert e.code == 503, f"Expected HTTP 503 for rate limit, got {e.code}."
    except urllib.error.URLError as e:
        pytest.fail(f"Unexpected error when testing rate limiting: {e}")