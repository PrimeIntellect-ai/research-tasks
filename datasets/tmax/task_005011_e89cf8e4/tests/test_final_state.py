# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

def generate_csv(num_lines):
    lines = []
    exp_ids = [f"exp{chr(65+i)}" for i in range(10)]
    for _ in range(num_lines):
        log_id = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 10)))
        exp_id = random.choice(exp_ids)
        inf_time = round(random.uniform(1.0, 100.0), 2)
        gt = random.choice([0, 1])
        if random.random() < 0.1:
            pred = ""
        else:
            pred = random.choice([0, 1])
        lines.append(f"{log_id},{exp_id},{inf_time},{gt},{pred}")
    return "\n".join(lines) + "\n"

def test_datamash_installed():
    """Verify that datamash has been successfully compiled and installed."""
    try:
        result = subprocess.run(["datamash", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert result.returncode == 0, f"datamash is not working correctly. Stderr: {result.stderr}"
    except FileNotFoundError:
        pytest.fail("datamash executable not found in PATH. Ensure it was installed correctly.")

def test_eval_tracker_fuzz_equivalence():
    """Fuzz the agent's script against the oracle script to ensure bit-exact equivalence."""
    agent_script = "/home/user/eval_tracker.sh"
    oracle_script = "/opt/oracle/eval_tracker_oracle.sh"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} does not exist."

    random.seed(42)

    for i in range(50):
        num_lines = random.randint(10, 1000)
        csv_content = generate_csv(num_lines)

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            oracle_proc = subprocess.run(["bash", oracle_script, tmp_path], capture_output=True, text=True)
            agent_proc = subprocess.run(["bash", agent_script, tmp_path], capture_output=True, text=True)

            assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}. Stderr: {oracle_proc.stderr}"
            assert agent_proc.returncode == 0, f"Agent script failed on iteration {i}.\nStderr: {agent_proc.stderr}"

            assert agent_proc.stdout == oracle_proc.stdout, (
                f"Mismatch on iteration {i} (CSV lines: {num_lines}).\n"
                f"Input CSV excerpt:\n{csv_content[:300]}...\n\n"
                f"Oracle Output:\n{oracle_proc.stdout}\n"
                f"Agent Output:\n{agent_proc.stdout}"
            )
        finally:
            os.remove(tmp_path)