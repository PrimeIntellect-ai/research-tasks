# test_final_state.py
import os
import random
import subprocess
import pytest

def test_detector_exists_and_executable():
    agent_path = "/home/user/detector.sh"
    assert os.path.isfile(agent_path), f"Agent script {agent_path} does not exist."
    assert os.access(agent_path, os.X_OK), f"Agent script {agent_path} is not executable."

def generate_random_csv():
    num_rows = random.randint(10, 200)
    rows = []
    for _ in range(num_rows):
        tx_id = random.randint(1, 1000)
        waits_on_tx_id = random.randint(1, 1000)
        wait_duration_ms = random.randint(1000, 10000)
        tx_priority = random.randint(1, 5)
        rows.append(f"{tx_id},{waits_on_tx_id},{wait_duration_ms},{tx_priority}")
    return "\n".join(rows) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/app/reference_detector"
    agent_path = "/home/user/detector.sh"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} does not exist."

    random.seed(42)
    N = 500

    for i in range(N):
        csv_input = generate_random_csv()

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=csv_input,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=csv_input,
            text=True,
            capture_output=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed (exit code {agent_proc.returncode}) on input:\n{csv_input}\nStderr: {agent_proc.stderr}")

        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input CSV:\n{csv_input}\n"
                f"Expected Output (Oracle):\n{oracle_out}\n"
                f"Actual Output (Agent):\n{agent_out}\n"
            )