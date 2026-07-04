# test_final_state.py

import os
import stat
import subprocess
import time
import urllib.request
import urllib.error
import json
import pytest

BASE_DIR = "/home/user/mobile_pipeline"
CI_RUN_SH = os.path.join(BASE_DIR, "ci_run.sh")
TEST_RESULTS = os.path.join(BASE_DIR, "test_results.log")
LIB_ENCODER = os.path.join(BASE_DIR, "libencoder.so")
APP_PY = os.path.join(BASE_DIR, "app.py")

@pytest.fixture(scope="session", autouse=True)
def run_ci_script():
    """Run the CI script if it exists and is executable, before tests."""
    if os.path.isfile(CI_RUN_SH) and os.access(CI_RUN_SH, os.X_OK):
        # Remove old log if exists
        if os.path.exists(TEST_RESULTS):
            os.remove(TEST_RESULTS)
        subprocess.run([CI_RUN_SH], cwd=BASE_DIR, timeout=30)
    yield

def test_ci_run_script_exists_and_executable():
    assert os.path.isfile(CI_RUN_SH), f"{CI_RUN_SH} does not exist."
    st = os.stat(CI_RUN_SH)
    assert bool(st.st_mode & stat.S_IXUSR), f"{CI_RUN_SH} is not executable."

def test_shared_library_compiled():
    assert os.path.isfile(LIB_ENCODER), f"{LIB_ENCODER} was not found in {BASE_DIR}."

    # Check if it's a shared object
    output = subprocess.check_output(["file", LIB_ENCODER]).decode("utf-8")
    assert "shared object" in output.lower(), f"{LIB_ENCODER} is not a valid shared object."

def test_test_results_log():
    assert os.path.isfile(TEST_RESULTS), f"{TEST_RESULTS} was not created."
    with open(TEST_RESULTS, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(lines) == 6, f"Expected exactly 6 lines in {TEST_RESULTS}, found {len(lines)}."

    expected = ["200", "200", "200", "200", "200", "429"]
    assert lines == expected, f"Expected statuses {expected}, but got {lines}."

def test_app_py_validation_and_rate_limiting():
    assert os.path.isfile(APP_PY), f"{APP_PY} does not exist."
    with open(APP_PY, "r") as f:
        content = f.read()

    # Check for some form of rate limiting mechanism (e.g. Flask-Limiter)
    assert "Limiter" in content or "429" in content, "Could not find rate limiting logic in app.py."

    # Check for validation logic (length < 50, ascii)
    assert "50" in content, "Could not find length validation (< 50) in app.py."
    assert "400" in content, "Could not find 400 Bad Request logic in app.py."

def test_app_py_behavior():
    """Start the Flask app temporarily to test the validation logic."""
    # Start the app
    proc = subprocess.Popen(["python3", APP_PY], cwd=BASE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) # Wait for server to start

    try:
        # Test 1: Valid request
        req = urllib.request.Request(
            "http://localhost:8080/encode",
            data=json.dumps({"text": "hello"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req) as response:
                assert response.getcode() == 200
                data = json.loads(response.read().decode("utf-8"))
                assert "encoded" in data
        except urllib.error.HTTPError as e:
            pytest.fail(f"Valid request failed with {e.code}")

        # Test 2: Invalid request (too long)
        long_text = "a" * 55
        req2 = urllib.request.Request(
            "http://localhost:8080/encode",
            data=json.dumps({"text": long_text}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            urllib.request.urlopen(req2)
            pytest.fail("Expected 400 Bad Request for text >= 50 chars")
        except urllib.error.HTTPError as e:
            assert e.code == 400, f"Expected 400 for long text, got {e.code}"

        # Test 3: Invalid request (non-ascii)
        req3 = urllib.request.Request(
            "http://localhost:8080/encode",
            data=json.dumps({"text": "hello\u2022"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            urllib.request.urlopen(req3)
            pytest.fail("Expected 400 Bad Request for non-ASCII text")
        except urllib.error.HTTPError as e:
            assert e.code == 400, f"Expected 400 for non-ASCII text, got {e.code}"

    finally:
        proc.terminate()
        proc.wait(timeout=5)