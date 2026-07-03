# test_final_state.py
import os
import subprocess
import random

def test_executable_exists():
    agent_path = '/home/user/normalize_stream'
    assert os.path.isfile(agent_path), f"Agent program missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program at {agent_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = '/opt/oracle/normalize_stream_oracle'
    agent_path = '/home/user/normalize_stream'

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"

    random.seed(42)

    for i in range(100):
        num_lines = random.randint(10, 1000)
        input_lines = [f"{random.uniform(-100.0, 100.0):.6f}" for _ in range(num_lines)]
        input_data = "\n".join(input_lines) + "\n"

        oracle_proc = subprocess.run(
            [oracle_path], 
            input=input_data, 
            text=True, 
            capture_output=True
        )
        agent_proc = subprocess.run(
            [agent_path], 
            input=input_data, 
            text=True, 
            capture_output=True
        )

        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}. Stderr: {oracle_proc.stderr}"

        if agent_proc.returncode != 0:
            assert False, f"Agent program failed with return code {agent_proc.returncode} on iteration {i}\nStderr: {agent_proc.stderr}"

        if oracle_proc.stdout != agent_proc.stdout:
            oracle_out_lines = oracle_proc.stdout.splitlines()
            agent_out_lines = agent_proc.stdout.splitlines()

            # Find the first differing line
            diff_idx = -1
            for j, (o, a) in enumerate(zip(oracle_out_lines, agent_out_lines)):
                if o != a:
                    diff_idx = j
                    break

            if diff_idx == -1 and len(oracle_out_lines) != len(agent_out_lines):
                diff_idx = min(len(oracle_out_lines), len(agent_out_lines))

            error_msg = (
                f"Output mismatch on iteration {i}.\n"
                f"Mismatch at line {diff_idx + 1}.\n"
                f"Input value at this line: {input_lines[diff_idx] if diff_idx < len(input_lines) else 'N/A'}\n"
                f"Oracle output: {oracle_out_lines[diff_idx] if diff_idx < len(oracle_out_lines) else 'EOF'}\n"
                f"Agent output: {agent_out_lines[diff_idx] if diff_idx < len(agent_out_lines) else 'EOF'}\n"
            )
            assert False, error_msg