# test_final_state.py

import os
import random
import subprocess
import pytest

def test_ci_test_sh_exists():
    path = "/home/user/ci_test.sh"
    assert os.path.exists(path), f"CI script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK) or "bash" in open(path).read(), f"{path} should be an executable bash script."

def test_linreg_fuzz_equivalence():
    agent_cmd = ["python3", "/home/user/linreg.py"]
    oracle_cmd = ["/app/linreg_ref"]

    assert os.path.exists(oracle_cmd[0]), f"Oracle {oracle_cmd[0]} missing."
    assert os.path.exists(agent_cmd[1]), f"Agent script {agent_cmd[1]} missing."

    random.seed(42)

    for i in range(100):
        num_commands = random.randint(1000, 5000)
        commands = []
        for _ in range(num_commands):
            r = random.random()
            if r < 0.5:
                x = random.randint(-10000, 10000)
                y = random.randint(-10000, 10000)
                commands.append(f"ADD {x} {y}")
            elif r < 0.75:
                commands.append("REMOVE_OLDEST")
            else:
                x = random.randint(-10000, 10000)
                commands.append(f"PREDICT {x}")

        input_data = "\n".join(commands) + "\n"

        oracle_proc = subprocess.run(oracle_cmd, input=input_data, text=True, capture_output=True)
        agent_proc = subprocess.run(agent_cmd, input=input_data, text=True, capture_output=True)

        if oracle_proc.stdout != agent_proc.stdout:
            oracle_lines = oracle_proc.stdout.splitlines()
            agent_lines = agent_proc.stdout.splitlines()

            diff_idx = -1
            for idx, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
                if o_line != a_line:
                    diff_idx = idx
                    break
            if diff_idx == -1:
                diff_idx = min(len(oracle_lines), len(agent_lines))

            error_msg = (
                f"Mismatch on iteration {i}.\n"
                f"Number of commands: {num_commands}\n"
                f"First differing output line index: {diff_idx}\n"
                f"Oracle output at line {diff_idx}: {oracle_lines[diff_idx] if diff_idx < len(oracle_lines) else 'EOF'}\n"
                f"Agent output at line {diff_idx}: {agent_lines[diff_idx] if diff_idx < len(agent_lines) else 'EOF'}\n"
            )
            pytest.fail(error_msg)