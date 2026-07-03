# test_final_state.py

import os
import stat
import subprocess
import random
import pytest

def generate_random_ip():
    """Generates a random IP address, weighted towards the specific subnets in the oracle logic."""
    choice = random.random()
    if choice < 0.33:
        # 10.x.x.x subnet
        return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    elif choice < 0.66:
        # 192.168.x.x subnet
        return f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
    else:
        # Other random subnets
        return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_random_port():
    """Generates a random port, ensuring both <1024 and >=1024 are well represented."""
    if random.random() < 0.5:
        return random.randint(1, 1023)
    return random.randint(1024, 65535)

def generate_fuzz_input():
    """Generates a semicolon-separated list of 1 to 5 IP:PORT pairs."""
    num_pairs = random.randint(1, 5)
    pairs = [f"{generate_random_ip()}:{generate_random_port()}" for _ in range(num_pairs)]
    return ";".join(pairs)

def test_oracle_extracted_and_executable():
    """Check if the oracle binary was extracted from the vault and made executable."""
    oracle_path = "/home/user/fw_policy_oracle"
    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} is missing. Did you extract the vault?"

    st = os.stat(oracle_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Oracle binary {oracle_path} is not executable by the user."

def test_evasion_payload_exists():
    """Check if the evasion payload script exists."""
    payload_path = "/home/user/evasion_payload.py"
    assert os.path.isfile(payload_path), f"Evasion payload {payload_path} is missing."

def test_fuzz_equivalence():
    """Fuzz both the oracle and the student's payload to ensure bit-exact behavioral equivalence."""
    oracle_path = "/home/user/fw_policy_oracle"
    payload_path = "/home/user/evasion_payload.py"

    # Ensure prerequisites for this test are met to avoid confusing errors
    if not os.path.isfile(oracle_path) or not os.path.isfile(payload_path):
        pytest.skip("Prerequisite files are missing.")

    random.seed(42) # Fixed seed for reproducible fuzzing
    inputs = [generate_fuzz_input() for _ in range(200)]

    for inp in inputs:
        # Run the reference oracle
        oracle_proc = subprocess.run(
            [oracle_path, inp], 
            capture_output=True, 
            text=True
        )
        oracle_out = oracle_proc.stdout

        # Run the student's payload
        payload_proc = subprocess.run(
            ["python3", payload_path, inp], 
            capture_output=True, 
            text=True
        )
        payload_out = payload_proc.stdout

        assert oracle_out == payload_out, (
            f"Output mismatch on input: '{inp}'\n\n"
            f"=== Oracle Output ===\n{oracle_out}\n"
            f"=== Payload Output ===\n{payload_out}\n"
            f"Payload must exactly match the oracle's standard output, including newlines."
        )