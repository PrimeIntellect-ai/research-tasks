# test_final_state.py

import os
import subprocess
import pytest

@pytest.fixture(scope="session", autouse=True)
def execute_build_script():
    """Execute the build script as 'user' before running the checks."""
    script_path = "/home/user/build.sh"

    assert os.path.isfile(script_path), f"Script {script_path} does not exist. Did you create it?"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable. Did you run chmod +x?"

    # Execute as 'user' if running as root
    cmd = ["sudo", "-u", "user", script_path] if os.geteuid() == 0 else [script_path]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, (
            f"build.sh failed with exit code {result.returncode}.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    except subprocess.TimeoutExpired:
        pytest.fail("build.sh execution timed out after 30 seconds. Does it hang or fail to background the servers?")

def test_build_result_log():
    """Verify that build_result.log exists and contains the expected output."""
    log_path = "/home/user/build_result.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did the curl command run and save output?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "POLYGLOT_BACKEND_OK"
    assert expected_content in content, f"Expected '{expected_content}' in {log_path}, but got: '{content}'"

def test_c_server_executable():
    """Verify that the C server was compiled and is executable."""
    c_server_path = "/home/user/polyglot-build/c_src/c_server"
    assert os.path.isfile(c_server_path), f"C server binary {c_server_path} does not exist. Did compilation fail?"
    assert os.access(c_server_path, os.X_OK), f"C server binary {c_server_path} is not executable."

def test_go_proxy_executable():
    """Verify that the Go proxy was compiled and is executable."""
    go_proxy_path = "/home/user/polyglot-build/go_src/proxy_server"
    assert os.path.isfile(go_proxy_path), f"Go proxy binary {go_proxy_path} does not exist. Did compilation fail?"
    assert os.access(go_proxy_path, os.X_OK), f"Go proxy binary {go_proxy_path} is not executable."