# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_safe_extraction():
    extracted_dir = "/home/user/extracted_dataset"
    assert os.path.exists(extracted_dir), f"Directory {extracted_dir} does not exist."
    assert os.path.isdir(extracted_dir), f"{extracted_dir} is not a directory."

    # Check that valid files were extracted
    assert os.path.exists(os.path.join(extracted_dir, "valid_data_1.txt")), "valid_data_1.txt was not extracted."
    assert os.path.exists(os.path.join(extracted_dir, "valid_data_2.txt")), "valid_data_2.txt was not extracted."

    # Check that malicious files were NOT extracted to their target locations
    assert not os.path.exists("/tmp/malicious.sh"), "Zip slip vulnerability! /tmp/malicious.sh was extracted."
    assert not os.path.exists("/home/user/escape.txt"), "Zip slip vulnerability! /home/user/escape.txt was extracted."

def test_filter_dataset_script_exists_and_executable():
    script_path = "/home/user/filter_dataset.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_filter_dataset_uses_flock():
    script_path = "/home/user/filter_dataset.sh"
    with open(script_path, "r") as f:
        content = f.read()
    assert "flock" in content, "The script does not appear to use 'flock'."
    assert "/tmp/filter.lock" in content, "The script does not appear to lock '/tmp/filter.lock'."

def test_fuzz_equivalence_filter_dataset():
    agent_script = "/home/user/filter_dataset.sh"
    oracle_script = "/app/oracle_filter_dataset.sh"

    random.seed(42)
    N = 5000

    for _ in range(N):
        timestamp = f"{random.randint(0, 99999999):08d}"
        status_code = random.randint(100, 599)
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        log_entry = f"[{timestamp}] {status_code} /path/to/{random_str}.dat"

        agent_proc = subprocess.run([agent_script, log_entry], capture_output=True, text=True)
        oracle_proc = subprocess.run([oracle_script, log_entry], capture_output=True, text=True)

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on input: '{log_entry}'. Expected {oracle_proc.returncode}, got {agent_proc.returncode}."
        assert agent_out == oracle_out, f"Output mismatch on input: '{log_entry}'.\nOracle:\n{oracle_out}\nAgent:\n{agent_out}"