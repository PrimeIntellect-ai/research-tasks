# test_final_state.py

import os
import re
import random
import subprocess
import pytest

def test_recovered_records_exist_and_valid():
    path = "/home/user/recovered_records.txt"
    assert os.path.isfile(path), f"File {path} does not exist. You must extract valid records."

    with open(path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, "Recovered records file is empty."

    # Valid record format: [TIMESTAMP] (ID) DATA_VALUE
    # Assuming TIMESTAMP and ID are digits, and DATA_VALUE is a number (possibly negative)
    valid_record_pattern = re.compile(r"^\[\d+\] \(\d+\) -?\d+$")

    for line in lines:
        assert valid_record_pattern.match(line), f"Invalid or corrupted record found in recovered_records.txt: '{line}'"

def test_robust_checksum_fuzz_equivalence():
    agent_script = "/home/user/robust_checksum.sh"
    oracle_bin = "/opt/oracle/reference_checksum_calc"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} does not exist."

    random.seed(42)
    # Fuzz-input distribution: 1000 random integers between 0 and 1000000
    fuzz_inputs = [random.randint(0, 1000000) for _ in range(1000)]

    for val in fuzz_inputs:
        val_str = str(val)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin, val_str],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle binary failed on input {val_str}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent script
        agent_proc = subprocess.run(
            ["bash", agent_script, val_str],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input {val_str}. Stderr: {agent_proc.stderr.strip()}"
        agent_out = agent_proc.stdout.strip()

        # Assert exact equivalence
        assert oracle_out == agent_out, (
            f"Output mismatch on input {val_str}.\n"
            f"Oracle expected: '{oracle_out}'\n"
            f"Agent produced : '{agent_out}'"
        )