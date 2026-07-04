# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

def test_extract_logs_script_exists():
    """Check if extract_logs.sh exists and is executable."""
    script_path = "/home/user/extract_logs.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_transactions_csv_exists():
    """Check if the user generated transactions.csv."""
    # It might be in /home/user/ or the current directory
    csv_path = "/home/user/transactions.csv"
    if not os.path.isfile(csv_path):
        # Fallback to check if it's in the current working directory
        csv_path = "transactions.csv"

    assert os.path.isfile(csv_path), "transactions.csv was not found. Did you run extract_logs.sh?"

    with open(csv_path, "r") as f:
        header = f.readline().strip()
        assert header == "timestamp,transaction_id,resource_id", f"Incorrect CSV header: {header}"

def test_detect_deadlocks_fuzz_equivalence():
    """Fuzz test detect_deadlocks.sh against the reference oracle."""
    agent_script = "/home/user/detect_deadlocks.sh"
    oracle_script = "/opt/verifier/reference_deadlock_detector.sh"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script is not executable: {agent_script}"

    random.seed(42)

    for i in range(100):
        num_rows = random.randint(10, 500)
        csv_lines = ["timestamp,transaction_id,resource_id"]

        # To ensure a good mix of cycles and no-cycles, we use a small pool of txs and resources
        num_txs = random.randint(5, 30)
        num_res = random.randint(5, 30)

        for t in range(num_rows):
            tx_id = random.randint(1, num_txs)
            res_id = random.randint(1, num_res)
            csv_lines.append(f"{t},{tx_id},{res_id}")

        csv_content = "\n".join(csv_lines) + "\n"

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            agent_proc = subprocess.run([agent_script, tmp_path], capture_output=True, text=True)
            oracle_proc = subprocess.run([oracle_script, tmp_path], capture_output=True, text=True)

            # The order of cycles (lines) might vary, but the cycles themselves are sorted internally.
            # We sort the lines to ensure a fair comparison.
            agent_out = sorted([line.strip() for line in agent_proc.stdout.strip().split('\n') if line.strip()])
            oracle_out = sorted([line.strip() for line in oracle_proc.stdout.strip().split('\n') if line.strip()])

            error_msg = (
                f"Mismatch on fuzz input {i} (rows: {num_rows}).\n"
                f"Oracle output:\n{oracle_proc.stdout}\n"
                f"Agent output:\n{agent_proc.stdout}\n"
                f"Agent stderr:\n{agent_proc.stderr}"
            )

            assert agent_out == oracle_out, error_msg

        finally:
            os.remove(tmp_path)