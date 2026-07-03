# test_final_state.py

import os
import subprocess
import pytest

def test_client_c_fixed():
    client_path = "/home/user/src/client.c"
    assert os.path.isfile(client_path), f"{client_path} is missing."
    with open(client_path, "r") as f:
        content = f.read()
    assert "127.0.0.1" in content, "client.c does not contain the correct IP address (127.0.0.1)."
    assert "8080" in content, "client.c does not contain the correct port (8080)."
    assert "192.168.1.100" not in content, "client.c still contains the old incorrect IP address."
    assert "9090" not in content, "client.c still contains the old incorrect port."

def test_preflight_c_exists_and_checks():
    preflight_path = "/home/user/src/preflight.c"
    assert os.path.isfile(preflight_path), f"{preflight_path} is missing."
    with open(preflight_path, "r") as f:
        content = f.read()

    # Check for required system calls and strings
    assert "statvfs" in content, "preflight.c does not use the statvfs system call."
    assert "deployers" in content, "preflight.c does not check for the 'deployers' group."
    assert "PREFLIGHT OK" in content, "preflight.c does not print 'PREFLIGHT OK'."

def test_pipeline_sh_executable():
    pipeline_path = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_path), f"{pipeline_path} is missing."
    assert os.access(pipeline_path, os.X_OK), f"{pipeline_path} is not executable."

def test_pipeline_execution_and_result():
    pipeline_path = "/home/user/pipeline.sh"

    # Run the pipeline script
    try:
        result = subprocess.run(
            [pipeline_path],
            capture_output=True,
            text=True,
            timeout=10,
            cwd="/home/user"
        )
    except subprocess.TimeoutExpired:
        pytest.fail("pipeline.sh timed out. The server process might not be backgrounded or terminated cleanly.")

    assert result.returncode == 0, f"pipeline.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Check the result.log
    result_log_path = "/home/user/deploy/result.log"
    assert os.path.isfile(result_log_path), f"{result_log_path} was not created by the pipeline."

    with open(result_log_path, "r") as f:
        log_content = f.read()

    assert log_content == "CONNECTION_SUCCESSFUL\n", f"result.log contains unexpected content: {repr(log_content)}"

def test_server_process_terminated():
    # Check if any server process is still running
    try:
        output = subprocess.check_output(["pgrep", "-f", "/home/user/deploy/server"], text=True)
        pytest.fail(f"Server process was not terminated cleanly. PIDs found: {output.strip()}")
    except subprocess.CalledProcessError:
        # pgrep returns non-zero if no processes matched, which is the expected state
        pass