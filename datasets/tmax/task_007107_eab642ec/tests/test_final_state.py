# test_final_state.py
import os
import subprocess
import time
import pytest

PROJECT_DIR = "/home/user/project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "build_and_test.sh")
LOG_PATH = os.path.join(PROJECT_DIR, "result.log")
SO_PATH = os.path.join(PROJECT_DIR, "libmathops.so")

@pytest.fixture(scope="session", autouse=True)
def run_script():
    """
    Run the build_and_test.sh script to generate the final state.
    We remove previous artifacts to ensure the script actually works.
    """
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)
    if os.path.exists(SO_PATH):
        os.remove(SO_PATH)

    start_time = time.time()
    result = subprocess.run(
        [SCRIPT_PATH], 
        cwd=PROJECT_DIR, 
        capture_output=True, 
        text=True
    )
    duration = time.time() - start_time

    return {"result": result, "duration": duration}

def test_script_execution(run_script):
    assert run_script["result"].returncode == 0, f"Script failed to execute properly. Stderr: {run_script['result'].stderr}"

def test_sleep_in_script_and_duration(run_script):
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "sleep 2" in content, "The script does not contain 'sleep 2' to pause for the server."
    assert run_script["duration"] >= 2.0, "The script finished in less than 2 seconds, indicating it did not actually pause."

def test_libmathops_linked_libm():
    assert os.path.isfile(SO_PATH), f"{SO_PATH} was not created."
    result = subprocess.run(["ldd", SO_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"ldd failed on {SO_PATH}"
    assert "libm.so" in result.stdout, "libmathops.so is not linked against the math library (libm.so)."

def test_result_log_success():
    assert os.path.isfile(LOG_PATH), f"{LOG_PATH} was not created."
    with open(LOG_PATH, "r") as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"Expected exact string 'SUCCESS' in result.log, got '{content}'"

def test_server_process_terminated():
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    running_servers = [
        line for line in result.stdout.splitlines() 
        if "server.py" in line and "grep" not in line and "pytest" not in line
    ]
    assert len(running_servers) == 0, f"The server.py process is still running in the background: {running_servers}"