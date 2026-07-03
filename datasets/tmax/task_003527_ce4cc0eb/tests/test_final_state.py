# test_final_state.py
import os
import subprocess
import random
import pytest

def test_executable_exists():
    assert os.path.isfile("/home/user/simulator"), "The compiled executable /home/user/simulator is missing."
    assert os.access("/home/user/simulator", os.X_OK), "The file /home/user/simulator is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_simulator"
    agent_path = "/home/user/simulator"

    assert os.path.isfile(oracle_path), f"Oracle program missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent program missing at {agent_path}"

    random.seed(42)

    for i in range(50):
        c = random.uniform(100.0, 400.0)
        dt = random.uniform(0.0001, 0.001)
        dx = random.uniform(0.1, 1.0)
        steps = random.randint(10, 100)

        args = [f"{c:.6f}", f"{dt:.6f}", f"{dx:.6f}", str(steps)]

        oracle_cmd = [oracle_path] + args
        agent_cmd = [agent_path] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on inputs {args}:\n{oracle_res.stderr}"
        assert agent_res.returncode == 0, f"Agent program failed on inputs {args}:\n{agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        if oracle_out != agent_out:
            # Show a snippet of the difference if it's too long
            oracle_lines = oracle_out.splitlines()
            agent_lines = agent_out.splitlines()

            diff_idx = -1
            for j, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
                if o_line != a_line:
                    diff_idx = j
                    break

            if diff_idx == -1 and len(oracle_lines) != len(agent_lines):
                diff_idx = min(len(oracle_lines), len(agent_lines))

            error_msg = f"Mismatch on inputs {args} (c={c}, dt={dt}, dx={dx}, steps={steps}).\n"
            if diff_idx != -1:
                error_msg += f"First difference at line {diff_idx + 1}:\n"
                error_msg += f"Oracle: {oracle_lines[diff_idx] if diff_idx < len(oracle_lines) else 'EOF'}\n"
                error_msg += f"Agent : {agent_lines[diff_idx] if diff_idx < len(agent_lines) else 'EOF'}\n"
            else:
                error_msg += "Outputs differ in length or content."

            pytest.fail(error_msg)