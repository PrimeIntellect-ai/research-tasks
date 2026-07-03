# test_final_state.py

import os
import subprocess
import time
import pytest

def test_beacon_compiled():
    path = "/home/user/beacon"
    assert os.path.isfile(path), f"Compiled binary {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_test_script_exists():
    path = "/home/user/test_beacon.py"
    assert os.path.isfile(path), f"Test script {path} does not exist."

def test_beacon_functionality():
    beacon_path = "/home/user/beacon"
    test_script = "/home/user/test_beacon.py"
    proof_file = "/home/user/proof.txt"

    # Remove proof file if it exists to ensure a fresh test
    if os.path.exists(proof_file):
        os.remove(proof_file)

    # Start beacon in the background
    beacon_proc = subprocess.Popen([beacon_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Wait for beacon to bind and listen
        time.sleep(1)

        # Run the test script
        result = subprocess.run(["python3", test_script], capture_output=True, text=True)
        assert result.returncode == 0, f"Test script failed with return code {result.returncode}. Error: {result.stderr}"

        # Wait for command execution
        time.sleep(1)

        # Check proof file
        assert os.path.isfile(proof_file), f"Proof file {proof_file} was not created."

        with open(proof_file, "r") as f:
            content = f.read()

        assert content.strip() == "SPACE TEST", f"Proof file content is incorrect. Expected 'SPACE TEST', got '{content.strip()}'"

    finally:
        # Clean up the beacon process
        beacon_proc.terminate()
        beacon_proc.wait(timeout=2)