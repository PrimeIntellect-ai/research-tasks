# test_final_state.py

import os
import subprocess
import time

PROXY_SCRIPT = "/home/user/secure_proxy.sh"

def test_proxy_exists_and_executable():
    assert os.path.exists(PROXY_SCRIPT), f"The script {PROXY_SCRIPT} does not exist."
    assert os.path.isfile(PROXY_SCRIPT), f"{PROXY_SCRIPT} is not a file."
    assert os.access(PROXY_SCRIPT, os.X_OK), f"{PROXY_SCRIPT} is not executable."

def test_proxy_functionality():
    # Wait to ensure a fresh rate limit window
    time.sleep(1.1)

    input_data = (
        "PING\n"
        "EXEC short\n"
        "EXEC this_is_a_very_long_payload_that_will_crash\n"
        "EXEC a\n"
        "PING\n"
        "EXEC b\n"
        "EXEC c\n"
    )

    expected_output = (
        "PONG\n"
        "SUCCESS: short\n"
        "ERR: MEM_SAFETY\n"
        "ERR: RATE_LIMIT\n"
        "ERR: RATE_LIMIT\n"
        "ERR: RATE_LIMIT\n"
        "ERR: RATE_LIMIT\n"
    )

    process = subprocess.Popen(
        [PROXY_SCRIPT],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input=input_data)

    assert stdout == expected_output, f"Output mismatch.\nExpected:\n{expected_output}\nGot:\n{stdout}"

def test_proxy_invalid_and_edge_cases():
    # Wait to ensure a fresh rate limit window
    time.sleep(1.1)

    input_data = (
        "UNKNOWN\n"
        "EXEC 12345678901234567890\n"
        "EXEC 123456789012345678901\n"
    )

    expected_output = (
        "ERR: INVALID_REQ\n"
        "SUCCESS: 12345678901234567890\n"
        "ERR: MEM_SAFETY\n"
    )

    process = subprocess.Popen(
        [PROXY_SCRIPT],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input=input_data)

    assert stdout == expected_output, f"Output mismatch for edge cases.\nExpected:\n{expected_output}\nGot:\n{stdout}"