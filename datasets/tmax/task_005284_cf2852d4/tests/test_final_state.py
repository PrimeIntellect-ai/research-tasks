# test_final_state.py

import os
import random
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/malware_oracle"
AGENT_SCRIPT_PATH = "/app/malware_score_clone-1.2.0/scorer.py"

def generate_log_file(filepath, num_lines):
    with open(filepath, 'w') as f:
        for _ in range(num_lines):
            # Sample from normal distribution: mean=10000000.0, std=0.05
            val = random.gauss(10000000.0, 0.05)
            f.write(f"[INFO] Container worker 03: Query execution finished in {val:.6f} ms\n")

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_SCRIPT_PATH), f"Agent script missing at {AGENT_SCRIPT_PATH}"

    random.seed(42)
    num_tests = 100

    for i in range(num_tests):
        num_lines = random.randint(50, 200)

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            generate_log_file(tmp.name, num_lines)
            tmp_path = tmp.name

        try:
            # Run oracle
            oracle_result = subprocess.run(
                [ORACLE_PATH, tmp_path],
                capture_output=True,
                text=True,
                check=False
            )

            # Run agent script
            agent_result = subprocess.run(
                ["python3", AGENT_SCRIPT_PATH, tmp_path],
                capture_output=True,
                text=True,
                check=False
            )

            oracle_out = oracle_result.stdout.strip()
            agent_out = agent_result.stdout.strip()

            if oracle_out != agent_out:
                with open(tmp_path, 'r') as f:
                    file_content = f.read()
                pytest.fail(
                    f"Mismatch on fuzz iteration {i + 1}/{num_tests}.\n"
                    f"Oracle output: {oracle_out!r}\n"
                    f"Agent output:  {agent_out!r}\n"
                    f"Input file content:\n{file_content}"
                )
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)