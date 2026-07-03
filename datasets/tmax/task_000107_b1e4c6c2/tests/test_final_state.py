# test_final_state.py

import os
import struct
import subprocess
import tempfile
import random
import pytest

def test_dataset_bin_exists_and_valid():
    dataset_path = "/home/user/dataset.bin"
    assert os.path.isfile(dataset_path), f"Dataset file missing at {dataset_path}"

    file_size = os.path.getsize(dataset_path)
    assert file_size > 0, "Dataset file is empty"
    assert file_size % (256 * 4) == 0, "Dataset file size is not a multiple of 256 float32 values (1024 bytes)"

def test_signature_txt_matches_oracle():
    dataset_path = "/home/user/dataset.bin"
    signature_path = "/home/user/signature.txt"
    oracle_path = "/app/oracle_model"

    assert os.path.isfile(signature_path), f"Signature file missing at {signature_path}"

    with open(signature_path, "r") as f:
        agent_signature = f.read().strip()

    oracle_proc = subprocess.run([oracle_path, dataset_path], capture_output=True, text=True)
    assert oracle_proc.returncode == 0, "Oracle failed to run on the dataset"
    oracle_signature = oracle_proc.stdout.strip()

    assert agent_signature == oracle_signature, "Signature in signature.txt does not match oracle output for dataset.bin"

def test_model_exec_fuzz_equivalence():
    agent_exec = "/home/user/model_exec"
    oracle_exec = "/app/oracle_model"

    assert os.path.isfile(agent_exec), f"Agent executable missing at {agent_exec}"
    assert os.access(agent_exec, os.X_OK), f"Agent executable at {agent_exec} is not executable"

    random.seed(42)

    for i in range(50):
        n_records = random.randint(10, 150)

        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as tmp:
            # Generate n_records * 256 random float32 values
            total_floats = n_records * 256
            floats = [random.uniform(0.0, 1.0) for _ in range(total_floats)]
            tmp.write(struct.pack(f'{total_floats}f', *floats))
            tmp_path = tmp.name

        try:
            oracle_proc = subprocess.run([oracle_exec, tmp_path], capture_output=True, text=True)
            agent_proc = subprocess.run([agent_exec, tmp_path], capture_output=True, text=True)

            assert oracle_proc.returncode == 0, "Oracle failed on fuzzed input"
            assert agent_proc.returncode == 0, "Agent executable failed on fuzzed input"

            oracle_out = oracle_proc.stdout.strip()
            agent_out = agent_proc.stdout.strip()

            if oracle_out != agent_out:
                pytest.fail(f"Mismatch on fuzz case {i+1} with {n_records} records.\nOracle: {oracle_out[:100]}...\nAgent: {agent_out[:100]}...")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)