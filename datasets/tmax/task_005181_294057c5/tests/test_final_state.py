# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_log_analyzer.py"
AGENT_PATH = "/home/user/log_analyzer.py"

def generate_random_utf8_line(length):
    chars = []
    for _ in range(length):
        choice = random.random()
        if choice < 0.6:
            # ASCII
            chars.append(chr(random.randint(0x20, 0x7E)))
        elif choice < 0.8:
            # Latin-1
            chars.append(chr(random.randint(0xA0, 0xFF)))
        else:
            # Emoji (Emoticons block)
            chars.append(chr(random.randint(0x1F600, 0x1F64F)))
    return "".join(chars)

def generate_fuzz_input(num_lines=10000):
    lines = []
    for _ in range(num_lines):
        length = random.randint(10, 200)
        lines.append(generate_random_utf8_line(length))
    return "\n".join(lines) + "\n"

def test_agent_script_exists():
    assert os.path.exists(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"

@pytest.mark.parametrize("seed", range(10))  # N=10 to avoid timeout, but large enough for fuzzing
def test_fuzz_equivalence(seed):
    random.seed(seed)
    fuzz_input = generate_fuzz_input(num_lines=2000)
    input_bytes = fuzz_input.encode('utf-8')

    # Run oracle
    oracle_cmd = ["python3", ORACLE_PATH]
    try:
        oracle_proc = subprocess.run(
            oracle_cmd,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        oracle_out = oracle_proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle timed out")

    # Run agent
    agent_cmd = ["python3", AGENT_PATH]
    try:
        agent_proc = subprocess.run(
            agent_cmd,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        agent_out = agent_proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Agent script timed out on fuzz input")

    if agent_proc.returncode != 0:
        pytest.fail(f"Agent script failed with return code {agent_proc.returncode}\nStderr: {agent_proc.stderr.decode('utf-8', errors='replace')}")

    if oracle_out != agent_out:
        # Find first differing line
        oracle_lines = oracle_out.decode('utf-8', errors='replace').splitlines()
        agent_lines = agent_out.decode('utf-8', errors='replace').splitlines()

        diff_msg = "Outputs differ.\n"
        diff_msg += f"Oracle output lines: {len(oracle_lines)}\n"
        diff_msg += f"Agent output lines: {len(agent_lines)}\n"

        for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
            if o_line != a_line:
                diff_msg += f"First difference at output line {i+1}:\n"
                diff_msg += f"Oracle: {o_line!r}\n"
                diff_msg += f"Agent:  {a_line!r}\n"
                break

        pytest.fail(diff_msg)