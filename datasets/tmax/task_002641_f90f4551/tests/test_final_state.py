# test_final_state.py

import os
import subprocess
import pytest

GATEWAY_DIR = "/home/user/gateway"
GATEWAY_EXEC = os.path.join(GATEWAY_DIR, "gateway")
RESPONSE_LOG = os.path.join(GATEWAY_DIR, "response.log")

def test_gateway_executable_exists():
    assert os.path.isfile(GATEWAY_EXEC), f"Executable {GATEWAY_EXEC} does not exist. Did you run make after fixing the Makefile?"
    assert os.access(GATEWAY_EXEC, os.X_OK), f"File {GATEWAY_EXEC} is not executable."

def test_gateway_rpath():
    try:
        result = subprocess.run(
            ["readelf", "-d", GATEWAY_EXEC],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run readelf on {GATEWAY_EXEC}. Error: {e.stderr}")
    except FileNotFoundError:
        pytest.fail("The 'readelf' command is not available.")

    output = result.stdout
    has_rpath = False
    for line in output.splitlines():
        if ("(RPATH)" in line or "(RUNPATH)" in line) and "[.]" in line:
            has_rpath = True
            break

    assert has_rpath, "The gateway executable does not have an RPATH or RUNPATH pointing to '.' ([.])."

def test_response_log_exists_and_content():
    assert os.path.isfile(RESPONSE_LOG), f"Log file {RESPONSE_LOG} does not exist. Did you redirect the output?"

    with open(RESPONSE_LOG, "r") as f:
        content = f.read().strip()

    expected_content = '{"status": 200, "message": "Request forwarded successfully"}'
    assert expected_content in content, f"The file {RESPONSE_LOG} does not contain the expected success message. Found: {content}"