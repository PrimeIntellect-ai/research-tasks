# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

def generate_random_csv(path):
    """Generate a random CSV file according to the fuzz input distribution."""
    num_rows = random.randint(20, 100)
    with open(path, 'w') as f:
        for _ in range(num_rows):
            id_len = random.randint(5, 10)
            row_id = ''.join(random.choices(string.ascii_letters + string.digits, k=id_len))

            dim = random.randint(5, 10)
            vec_a = ':'.join(f"{random.uniform(-1.0, 1.0):.6f}" for _ in range(dim))
            vec_b = ':'.join(f"{random.uniform(-1.0, 1.0):.6f}" for _ in range(dim))

            f.write(f"{row_id},{vec_a},{vec_b}\n")

def test_cosine_sim_executable_exists():
    """Check if the vendored C utility was successfully compiled."""
    path = "/app/lib-embed-tools/bin/cosine_sim"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you fix the Makefile and run make?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_pipeline_script_exists():
    """Check if the pipeline Bash script exists and is executable."""
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"Script {path} is not executable. Did you run chmod +x?"

def test_fuzz_equivalence():
    """Test the agent's pipeline script against the oracle on N=20 random inputs."""
    random.seed(42)
    oracle_path = "/opt/oracle/pipeline_oracle.sh"
    agent_script = "/home/user/pipeline.sh"

    assert os.path.isfile(oracle_path), f"Oracle script {oracle_path} not found."

    for i in range(20):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            csv_path = tmp.name

        try:
            generate_random_csv(csv_path)

            oracle_cmd = ["/bin/bash", oracle_path, csv_path]
            agent_cmd = ["/bin/bash", agent_script, csv_path]

            oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
            agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)

            assert oracle_proc.returncode == 0, f"Oracle script failed on input {csv_path}:\n{oracle_proc.stderr}"
            assert agent_proc.returncode == 0, f"Agent script failed on input {csv_path}:\n{agent_proc.stderr}"

            oracle_out = oracle_proc.stdout.strip()
            agent_out = agent_proc.stdout.strip()

            if oracle_out != agent_out:
                with open(csv_path, 'r') as f:
                    csv_content = f.read()
                assert False, (
                    f"Mismatch on random input {i+1}/20.\n\n"
                    f"Input CSV content:\n{csv_content}\n"
                    f"Expected output (Oracle):\n{oracle_out}\n\n"
                    f"Actual output (Agent):\n{agent_out}\n"
                )
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)