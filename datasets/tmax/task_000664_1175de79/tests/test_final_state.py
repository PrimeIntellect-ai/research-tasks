# test_final_state.py

import os
import subprocess
import hashlib
import pytest

def test_exploit_script_exists_and_executable():
    exploit_path = "/home/user/exploit.sh"
    assert os.path.isfile(exploit_path), f"Exploit script {exploit_path} does not exist."
    assert os.access(exploit_path, os.X_OK), f"Exploit script {exploit_path} is not executable."

def test_exploit_execution_and_result():
    exploit_path = "/home/user/exploit.sh"
    target_hash_path = "/home/user/target_hash.txt"
    hosts_path = "/etc/hosts"

    # Ensure /etc/hosts exists to calculate expected hash
    assert os.path.isfile(hosts_path), f"System file {hosts_path} is missing."

    # Remove target_hash.txt if it exists from previous runs to ensure exploit.sh creates it
    if os.path.exists(target_hash_path):
        os.remove(target_hash_path)

    # Run the exploit script
    try:
        subprocess.run([exploit_path], check=True, timeout=10)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {exploit_path} failed with return code {e.returncode}.")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {exploit_path} timed out.")

    # Check if target_hash.txt was created
    assert os.path.isfile(target_hash_path), f"The file {target_hash_path} was not created after running the exploit."

    # Calculate expected hash
    with open(hosts_path, "rb") as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()

    # Read the actual hash
    with open(target_hash_path, "r") as f:
        actual_content = f.read()

    actual_hash = actual_content.strip()

    assert actual_hash == expected_hash, f"The hash in {target_hash_path} ({actual_hash}) does not match the expected SHA-256 hash of {hosts_path} ({expected_hash})."

    # Ensure it contains exactly the 64-character hash and a newline (or just the 64 chars)
    # The constraint says "exactly the 64-character SHA-256 hash and a newline."
    # Let's check the length of the stripped string.
    assert len(actual_hash) == 64, f"The content of {target_hash_path} should be exactly a 64-character hex string."