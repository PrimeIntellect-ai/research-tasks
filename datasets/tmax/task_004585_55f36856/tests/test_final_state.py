# test_final_state.py

import os
import sys
import subprocess
import tempfile
import random
import numpy as np
import pytest

def test_fisher_package_installed():
    """Verify that the fisher package is successfully installed and importable."""
    try:
        import fisher
    except ImportError as e:
        pytest.fail(f"The 'fisher' package is not installed or failed to import. Error: {e}")

def test_fuzz_equivalence():
    """
    Fuzz-equivalence test: Generate 100 random CSV files and ensure the agent's
    script produces the exact same output as the oracle script.
    """
    oracle_path = "/app/oracle_summarize.py"
    agent_path = "/home/user/process_dataset.py"

    assert os.path.exists(oracle_path), f"Oracle program not found at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent program not found at {agent_path}"

    np.random.seed(42)
    random.seed(42)

    num_tests = 100
    for i in range(num_tests):
        num_rows = random.randint(10, 100)

        cat1 = np.random.choice([0, 1], size=num_rows)
        cat2 = np.random.choice([0, 1], size=num_rows)
        val1 = np.random.uniform(-100.0, 100.0, size=num_rows)
        val2 = np.random.uniform(-100.0, 100.0, size=num_rows)
        val3 = np.random.uniform(-100.0, 100.0, size=num_rows)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("cat1,cat2,val1,val2,val3\n")
            for j in range(num_rows):
                f.write(f"{cat1[j]},{cat2[j]},{val1[j]},{val2[j]},{val3[j]}\n")
            csv_path = f.name

        try:
            oracle_res = subprocess.run([sys.executable, oracle_path, csv_path], capture_output=True, text=True)
            agent_res = subprocess.run([sys.executable, agent_path, csv_path], capture_output=True, text=True)

            if agent_res.returncode != 0:
                with open(csv_path, 'r') as f_csv:
                    csv_content = f_csv.read()
                pytest.fail(f"Agent script failed on fuzz input {i+1}/{num_tests}.\n"
                            f"Input CSV:\n{csv_content}\n"
                            f"Error output:\n{agent_res.stderr}")

            if oracle_res.returncode != 0:
                pytest.fail(f"Oracle script failed on fuzz input {i+1}/{num_tests}. Error: {oracle_res.stderr}")

            oracle_out = oracle_res.stdout.strip()
            agent_out = agent_res.stdout.strip()

            if agent_out != oracle_out:
                with open(csv_path, 'r') as f_csv:
                    csv_content = f_csv.read()
                pytest.fail(f"Output mismatch on fuzz input {i+1}/{num_tests}.\n"
                            f"Input CSV:\n{csv_content}\n"
                            f"Oracle output: {oracle_out}\n"
                            f"Agent output:  {agent_out}")
        finally:
            os.remove(csv_path)