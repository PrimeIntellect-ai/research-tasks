# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/legacy_scorer"
AGENT_SCRIPT = "/home/user/scorer.sh"
NUM_ITERATIONS = 50

def generate_random_csv(file_path, num_rows):
    with open(file_path, "w") as f:
        for _ in range(num_rows):
            artifact_id = "".join(random.choices(string.ascii_letters + string.digits, k=8))
            metric_a = f"{random.uniform(0.01, 0.99):.4f}"
            metric_b = f"{random.uniform(0.01, 0.99):.4f}"
            metric_c = f"{random.uniform(0.01, 0.99):.4f}"
            f.write(f"{artifact_id},{metric_a},{metric_b},{metric_c}\n")

def test_scorer_script_exists_and_executable():
    assert os.path.exists(AGENT_SCRIPT), f"The script {AGENT_SCRIPT} does not exist."
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"{AGENT_SCRIPT} is not executable."

def test_scorer_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"

    random.seed(42)

    for i in range(NUM_ITERATIONS):
        prior = f"{random.uniform(0.100, 0.900):.3f}"
        num_rows = random.randint(10, 50)

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
            csv_path = tmp.name

        try:
            generate_random_csv(csv_path, num_rows)

            # Run oracle
            oracle_cmd = [ORACLE_PATH, "--prior", prior, csv_path]
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
            assert oracle_res.returncode == 0, f"Oracle failed on iteration {i} with error: {oracle_res.stderr}"
            oracle_output = oracle_res.stdout

            # Run agent script
            agent_cmd = ["/bin/bash", AGENT_SCRIPT, "--prior", prior, csv_path]
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
            assert agent_res.returncode == 0, f"Agent script failed on iteration {i} with error: {agent_res.stderr}"
            agent_output = agent_res.stdout

            # Compare outputs
            if oracle_output != agent_output:
                with open(csv_path, "r") as f:
                    input_data = f.read()
                pytest.fail(
                    f"Mismatch on iteration {i}.\n"
                    f"Prior: {prior}\n"
                    f"Input CSV:\n{input_data}\n"
                    f"Oracle Output:\n{oracle_output}\n"
                    f"Agent Output:\n{agent_output}"
                )
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)