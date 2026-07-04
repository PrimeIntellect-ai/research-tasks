# test_final_state.py

import os
import subprocess
import random
import time
import pytest

ORACLE_PATH = "/app/oracle_sanitizer"
AGENT_PATH = "/home/user/sanitizer"

def test_sanitizer_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), "Agent binary is not executable"

    random.seed(42)
    # Using a smaller N to prevent test timeouts, while still providing robust fuzzing
    N = 500

    for i in range(N):
        length = random.randint(0, 5000)
        input_data = bytearray(random.getrandbits(8) for _ in range(length))

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_data, capture_output=True)

        assert oracle_proc.returncode == 0, "Oracle failed"

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(f"Mismatch on fuzz iteration {i}.\n"
                        f"Input length: {length}\n"
                        f"Oracle output length: {len(oracle_proc.stdout)}\n"
                        f"Agent output length: {len(agent_proc.stdout)}\n"
                        f"Oracle output: {oracle_proc.stdout[:100]}...\n"
                        f"Agent output: {agent_proc.stdout[:100]}...")

def test_vm_script_port_forwarding():
    script_path = "/home/user/vm/start_vm.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"
    with open(script_path, "r") as f:
        content = f.read()

    # Check if hostfwd is present in the script
    assert "hostfwd" in content, "start_vm.sh is missing hostfwd configuration"
    assert "8080" in content and "9000" in content, "start_vm.sh missing correct port forwarding (8080 to 9000)"

def test_wrapper_script_and_end_to_end_flow():
    wrapper_path = "/home/user/healthcheck/wrapper.sh"
    raw_metrics_path = "/home/user/healthcheck/raw_metrics.txt"
    last_result_path = "/home/user/healthcheck/last_result.txt"

    assert os.path.isfile(wrapper_path), f"Missing {wrapper_path}"

    # Prepare a test payload
    test_payload = b"Test!!!  PAYLOAD---123\n"
    with open(raw_metrics_path, "wb") as f:
        f.write(test_payload)

    # Get the expected sanitized output using the oracle
    oracle_proc = subprocess.run([ORACLE_PATH], input=test_payload, capture_output=True)
    expected_output = oracle_proc.stdout

    # Run the wrapper script in a clean environment to simulate cron
    env = {"PATH": "/usr/bin:/bin"}
    proc = subprocess.run(["sh", wrapper_path], env=env, capture_output=True)

    # Give it a tiny bit of time to write the file if it was backgrounded (though it shouldn't be)
    time.sleep(0.5)

    assert os.path.isfile(last_result_path), f"Wrapper script did not create {last_result_path}"

    with open(last_result_path, "rb") as f:
        actual_output = f.read()

    assert actual_output == expected_output, (
        f"End-to-end flow failed. Expected {expected_output}, got {actual_output}. "
        "Check if the VM is running and port forwarding is correct."
    )