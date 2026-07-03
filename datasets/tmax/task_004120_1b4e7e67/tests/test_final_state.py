# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/opt/oracle/oracle_run_density.sh"
AGENT_PATH = "/home/user/run_density.sh"
NUM_TESTS = 50

def generate_random_fasta(filepath):
    num_sequences = random.randint(1, 20)
    with open(filepath, 'w') as f:
        for _ in range(num_sequences):
            seq_id_len = random.randint(5, 15)
            seq_id = ''.join(random.choices(string.ascii_letters + string.digits, k=seq_id_len))

            seq_len = random.randint(50, 1000)
            seq_body = ''.join(random.choices(['A', 'C', 'G', 'T', 'a', 'c', 'g', 't'], k=seq_len))

            f.write(f">{seq_id}\n")
            # Write sequence in chunks of 80 characters
            for i in range(0, len(seq_body), 80):
                f.write(f"{seq_body[i:i+80]}\n")

def test_wrapper_exists_and_executable():
    assert os.path.isfile(AGENT_PATH), f"Agent wrapper script not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent wrapper script at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle script not found at {ORACLE_PATH}"

    random.seed(42)

    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(NUM_TESTS):
            fasta_path = os.path.join(temp_dir, f"test_{i}.fasta")
            generate_random_fasta(fasta_path)

            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_PATH, fasta_path],
                capture_output=True,
                text=True
            )
            oracle_out = oracle_proc.stdout

            # Run agent
            agent_proc = subprocess.run(
                [AGENT_PATH, fasta_path],
                capture_output=True,
                text=True
            )
            agent_out = agent_proc.stdout

            if agent_proc.returncode != oracle_proc.returncode:
                pytest.fail(f"Return code mismatch on input {fasta_path}.\nOracle: {oracle_proc.returncode}\nAgent: {agent_proc.returncode}\nAgent stderr: {agent_proc.stderr}")

            if agent_out != oracle_out:
                with open(fasta_path, 'r') as f:
                    input_content = f.read()
                pytest.fail(f"Output mismatch on input {fasta_path}.\n\nInput FASTA:\n{input_content}\n\nOracle Output:\n{oracle_out}\n\nAgent Output:\n{agent_out}")