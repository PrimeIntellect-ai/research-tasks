# test_final_state.py

import os
import subprocess
import random
import pytest

def test_tap_interface():
    res = subprocess.run(["ip", "addr", "show", "tap0"], capture_output=True, text=True)
    assert res.returncode == 0, "tap0 interface does not exist. Did you create it?"
    assert "10.0.0.1/24" in res.stdout, "tap0 does not have the expected IP address 10.0.0.1/24."

def test_parser_fuzz_equivalence():
    agent_parser = "/home/user/parser"
    oracle_parser = "/app/oracle_parser"

    assert os.path.isfile(agent_parser), f"Missing compiled parser at {agent_parser}"
    assert os.access(agent_parser, os.X_OK), f"Parser at {agent_parser} is not executable"

    random.seed(42)
    for i in range(1000):
        length = random.randint(0, 500)
        input_data = bytes(random.getrandbits(8) for _ in range(length))

        oracle_proc = subprocess.run([oracle_parser], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_parser], input=input_data, capture_output=True)

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(f"Output mismatch on fuzz input {i} (length {length}).\nInput hex: {input_data.hex()}\nOracle output: {oracle_proc.stdout}\nAgent output: {agent_proc.stdout}")

        if oracle_proc.returncode != agent_proc.returncode:
            pytest.fail(f"Return code mismatch on fuzz input {i} (length {length}).\nOracle RC: {oracle_proc.returncode}\nAgent RC: {agent_proc.returncode}")

def test_sync_script_end_to_end():
    sync_script = "/home/user/sync.sh"
    assert os.path.isfile(sync_script), f"Missing sync script at {sync_script}"
    assert os.access(sync_script, os.X_OK), f"Sync script at {sync_script} is not executable"

    log_path = "/tmp/api_received.log"
    if os.path.exists(log_path):
        os.remove(log_path)

    # Execute the sync script
    res = subprocess.run([sync_script], capture_output=True, text=True)
    assert res.returncode == 0, f"sync.sh failed with return code {res.returncode}. Stderr: {res.stderr}"

    assert os.path.exists(log_path), f"The API log file {log_path} was not created. Did the script successfully POST to the API?"

    with open(log_path, "rb") as f:
        api_received = f.read()

    # Fetch the original payload from the VM to determine the expected output
    nc_res = subprocess.run(["nc", "10.0.0.2", "9999"], capture_output=True)
    assert nc_res.returncode == 0, "Failed to connect to the VM at 10.0.0.2:9999 to fetch the payload."
    vm_payload = nc_res.stdout

    oracle_proc = subprocess.run(["/app/oracle_parser"], input=vm_payload, capture_output=True)
    expected_output = oracle_proc.stdout

    assert api_received == expected_output, "The data received by the API does not match the expected parsed output from the VM payload."