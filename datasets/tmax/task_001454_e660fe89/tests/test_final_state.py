# test_final_state.py

import os
import subprocess
import random
import string
import tempfile
import pytest

def test_batch_scorer_fuzz_equivalence():
    """
    Fuzz-equivalence test to verify that the agent's script exactly matches the oracle's output.
    """
    agent_script = "/home/user/batch_scorer.sh"
    oracle_bin = "/app/sim_scorer"

    assert os.path.exists(agent_script), f"Agent script {agent_script} not found."
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable."
    assert os.path.exists(oracle_bin), f"Oracle binary {oracle_bin} not found."

    random.seed(42)
    charset = string.ascii_letters + " "

    # Run 5 iterations of fuzzing with 20-50 rows each to keep execution time reasonable
    # while calling the oracle binary for each row.
    for i in range(5):
        num_rows = random.randint(20, 50)
        csv_lines = []
        oracle_outputs = []

        for _ in range(num_rows):
            len1 = random.randint(1, 100)
            len2 = random.randint(1, 100)
            # Avoid commas in the random strings to not break simple CSV parsing
            str1 = "".join(random.choices(charset, k=len1))
            str2 = "".join(random.choices(charset, k=len2))

            csv_lines.append(f"{str1},{str2}")

            # Run oracle to get the ground truth
            res = subprocess.run([oracle_bin, str1, str2], capture_output=True, text=True)
            assert res.returncode == 0, f"Oracle failed on inputs: '{str1}', '{str2}'"
            oracle_outputs.append(res.stdout.strip())

        # Write the fuzzed CSV
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".csv") as tmp:
            tmp.write("\n".join(csv_lines) + "\n")
            tmp_path = tmp.name

        try:
            # Run the agent's batch scorer
            res_agent = subprocess.run([agent_script, tmp_path], capture_output=True, text=True, timeout=15)
            assert res_agent.returncode == 0, f"Agent script failed with error: {res_agent.stderr}"

            agent_outputs = res_agent.stdout.strip().split('\n')

            # Filter out any empty lines from agent output
            agent_outputs = [out for out in agent_outputs if out.strip()]

            assert len(agent_outputs) == num_rows, \
                f"Expected {num_rows} outputs from agent script, but got {len(agent_outputs)}."

            # Compare bit-exact outputs
            for row_idx, (expected, actual) in enumerate(zip(oracle_outputs, agent_outputs)):
                assert expected == actual.strip(), \
                    f"Mismatch at row {row_idx+1} in fuzz iteration {i+1}.\n" \
                    f"Input row: {csv_lines[row_idx]}\n" \
                    f"Oracle output: {expected}\n" \
                    f"Agent output: {actual.strip()}"
        finally:
            os.remove(tmp_path)