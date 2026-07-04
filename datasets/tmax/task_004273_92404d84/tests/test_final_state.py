# test_final_state.py
import os
import random
import subprocess
import pytest

def generate_fuzz_input(num_lines=1000):
    random.seed(42)
    lines = []

    # Edge cases
    # 1. Single integer
    lines.append(str(random.randint(-50000, 50000)))
    # 2. All identical
    val = random.randint(-50000, 50000)
    lines.append(" ".join([str(val)] * 50))
    # 3. Only two values
    lines.append(f"{random.randint(-50000, 50000)} {random.randint(-50000, 50000)}")
    # 4. Empty line
    lines.append("")
    # 5. Extreme values
    lines.append(" ".join([str(random.choice([-50000, 50000])) for _ in range(10)]))

    for _ in range(num_lines - len(lines)):
        length = random.randint(1, 100)
        nums = [str(random.randint(-50000, 50000)) for _ in range(length)]
        lines.append(" ".join(nums))

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/app/cleaner_oracle"
    agent_path = "/home/user/cleaner"

    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    input_data = generate_fuzz_input(1000)

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_path], 
        input=input_data, 
        text=True, 
        capture_output=True, 
        check=True
    )
    oracle_out = oracle_proc.stdout

    # Run agent
    agent_proc = subprocess.run(
        [agent_path], 
        input=input_data, 
        text=True, 
        capture_output=True
    )
    assert agent_proc.returncode == 0, f"Agent program failed with return code {agent_proc.returncode}\nStderr: {agent_proc.stderr}"

    agent_out = agent_proc.stdout

    oracle_lines = oracle_out.splitlines()
    agent_lines = agent_out.splitlines()

    assert len(oracle_lines) == len(agent_lines), f"Output line count mismatch. Oracle: {len(oracle_lines)}, Agent: {len(agent_lines)}"

    input_lines = input_data.splitlines()
    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        assert o_line == a_line, f"Mismatch on line {i+1}.\nInput: {input_lines[i]}\nOracle: {o_line}\nAgent:  {a_line}"