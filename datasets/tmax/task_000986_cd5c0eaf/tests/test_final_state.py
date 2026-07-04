# test_final_state.py
import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_parser"
AGENT_SCRIPT = "/home/user/telemetry_parser.py"
NUM_LINES = 5000

def generate_fuzz_data(n: int, seed: int = 42) -> bytes:
    random.seed(seed)
    lines = []

    def rand_string(min_len, max_len, chars=string.ascii_letters + string.digits + "_"):
        length = random.randint(min_len, max_len)
        return "".join(random.choice(chars) for _ in range(length))

    for _ in range(n):
        is_corrupted = random.random() < 0.3

        timestamp = f"{random.uniform(1000000000.0, 2000000000.0):.6f}"
        device = rand_string(1, 10)
        voltage = f"{random.uniform(0.0, 100.0):.{random.randint(1, 8)}f}"
        status = rand_string(0, 5)

        line = f"[{timestamp}] {device}: {voltage} | {status}"

        if is_corrupted:
            corruption_type = random.choice(['null_byte', 'drop_bracket', 'truncate', 'garbage'])
            if corruption_type == 'null_byte':
                idx = random.randint(0, len(line))
                line = line[:idx] + '\x00' + line[idx:]
            elif corruption_type == 'drop_bracket':
                line = line.replace('[', '', 1)
            elif corruption_type == 'truncate':
                line = line[:random.randint(1, len(line)//2)]
            elif corruption_type == 'garbage':
                line = rand_string(5, 20)

        lines.append(line.encode('utf-8'))

    return b"\n".join(lines) + b"\n"

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing: {AGENT_SCRIPT}"
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing: {ORACLE_PATH}"

    input_data = generate_fuzz_data(NUM_LINES)

    # Run oracle
    oracle_proc = subprocess.run(
        [ORACLE_PATH],
        input=input_data,
        capture_output=True,
        timeout=10
    )
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr.decode('utf-8', errors='replace')}"
    oracle_out = oracle_proc.stdout

    # Run agent
    agent_proc = subprocess.run(
        ["python3", AGENT_SCRIPT],
        input=input_data,
        capture_output=True,
        timeout=10
    )
    assert agent_proc.returncode == 0, f"Agent script failed or crashed: {agent_proc.stderr.decode('utf-8', errors='replace')}"
    agent_out = agent_proc.stdout

    # Compare outputs line by line to give better error messages
    oracle_lines = oracle_out.splitlines()
    agent_lines = agent_out.splitlines()
    input_lines = input_data.splitlines()

    assert len(agent_lines) == len(oracle_lines), f"Line count mismatch: Oracle produced {len(oracle_lines)}, Agent produced {len(agent_lines)}"

    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        if o_line != a_line:
            inp = input_lines[i].decode('utf-8', errors='replace')
            o_str = o_line.decode('utf-8', errors='replace')
            a_str = a_line.decode('utf-8', errors='replace')
            pytest.fail(f"Mismatch on line {i+1}.\nInput: {inp!r}\nOracle: {o_str}\nAgent : {a_str}")