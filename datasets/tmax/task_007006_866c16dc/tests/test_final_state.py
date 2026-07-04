# test_final_state.py
import os
import json
import stat
import time
import subprocess
import pytest

APP_DIR = "/home/user/app"
USERS_JSON = os.path.join(APP_DIR, "users.json")
AUTH_SERVICE = os.path.join(APP_DIR, "auth_service.py")
DATA_SERVICE = os.path.join(APP_DIR, "data_service.py")
PIPELINE_SCRIPT = "/home/user/run_pipeline.sh"
BUILD_RESULT = "/home/user/build_result.txt"

def test_users_json_fixed():
    assert os.path.isfile(USERS_JSON), f"{USERS_JSON} is missing."
    try:
        with open(USERS_JSON, 'r') as f:
            users = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{USERS_JSON} is not valid JSON. Syntax error was not fixed.")

    assert "ci_worker" in users, "User 'ci_worker' is missing from users.json."
    ci_worker = users["ci_worker"]
    assert ci_worker.get("password") == "ci_secure_pass", "Incorrect password for 'ci_worker'."
    assert ci_worker.get("role") == "builder", "Incorrect role for 'ci_worker'."

def test_auth_service_communication_fixed():
    assert os.path.isfile(AUTH_SERVICE), f"{AUTH_SERVICE} is missing."
    with open(AUTH_SERVICE, 'r') as f:
        content = f.read()

    assert "X-Internal-User" in content, "auth_service.py is not using 'X-Internal-User' header."
    assert "X-Forwarded-User" not in content, "auth_service.py is still using 'X-Forwarded-User' header."

def test_auth_service_log_rotation_configured():
    assert os.path.isfile(AUTH_SERVICE), f"{AUTH_SERVICE} is missing."
    with open(AUTH_SERVICE, 'r') as f:
        content = f.read()

    assert "TimedRotatingFileHandler" in content, "TimedRotatingFileHandler not found in auth_service.py."
    assert "midnight" in content or "'midnight'" in content or '"midnight"' in content, "Log rotation when='midnight' not found."
    assert "backupCount=5" in content.replace(" ", ""), "Log rotation backupCount=5 not found."

def test_pipeline_script_exists_and_executable():
    assert os.path.isfile(PIPELINE_SCRIPT), f"{PIPELINE_SCRIPT} is missing."
    st = os.stat(PIPELINE_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{PIPELINE_SCRIPT} is not executable."

def test_pipeline_execution():
    # Remove result file if it exists
    if os.path.exists(BUILD_RESULT):
        os.remove(BUILD_RESULT)

    # Start services
    auth_proc = subprocess.Popen(["python3", AUTH_SERVICE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    data_proc = subprocess.Popen(["python3", DATA_SERVICE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Give services a moment to start
        time.sleep(2)

        # Run pipeline script
        result = subprocess.run([PIPELINE_SCRIPT], capture_output=True, text=True)
        assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}"

        # Check result file
        assert os.path.isfile(BUILD_RESULT), f"{BUILD_RESULT} was not created by the pipeline script."
        with open(BUILD_RESULT, 'r') as f:
            result_content = f.read().strip()

        try:
            result_json = json.loads(result_content)
        except json.JSONDecodeError:
            pytest.fail(f"Content of {BUILD_RESULT} is not valid JSON: {result_content}")

        assert result_json.get("status") == "success", f"Expected status 'success', got {result_json.get('status')}"
        assert result_json.get("build_id") == "build_for_ci_worker", f"Expected build_id 'build_for_ci_worker', got {result_json.get('build_id')}"

    finally:
        # Cleanup processes
        auth_proc.terminate()
        data_proc.terminate()
        auth_proc.wait()
        data_proc.wait()