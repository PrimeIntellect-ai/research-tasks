# test_final_state.py
import os
import subprocess
import random
import csv
import io

def generate_csv_input(num_rows):
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["experiment_name", "metric_value"])
    for _ in range(num_rows):
        name_len = random.randint(5, 20)
        name = "".join(random.choices(charset, k=name_len))
        # Occasionally inject malformed values to test robustness
        if random.random() < 0.05:
            val = "invalid_float"
        else:
            val = random.uniform(-1000.0, 32000.0)
        writer.writerow([name, val])
    return output.getvalue()

def test_fuzz_equivalence():
    agent_path = "/home/user/metric_analyzer.py"
    oracle_path = "/opt/oracle/metric_analyzer_oracle.py"

    assert os.path.exists(agent_path), f"Agent program missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program at {agent_path} is not executable"

    assert os.path.exists(oracle_path), f"Oracle program missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle program at {oracle_path} is not executable"

    random.seed(42)

    for i in range(50):
        num_rows = random.randint(0, 1500)
        csv_input = generate_csv_input(num_rows)

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=csv_input,
            text=True,
            capture_output=True
        )

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=csv_input,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed with return code {agent_proc.returncode}\nStderr: {agent_proc.stderr}"
        assert oracle_proc.returncode == 0, f"Oracle script failed with return code {oracle_proc.returncode}\nStderr: {oracle_proc.stderr}"

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        if agent_out != oracle_out:
            error_msg = (
                f"Mismatch on iteration {i} with {num_rows} rows.\n"
                f"Input CSV (first 500 chars):\n{csv_input[:500]}...\n\n"
                f"Oracle Output:\n{oracle_out}\n\n"
                f"Agent Output:\n{agent_out}\n"
            )
            assert False, error_msg