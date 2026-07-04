# test_final_state.py

import os
import subprocess
import random
import string
import csv
import io
import pytest

AGENT_BIN = "/app/log-processor/target/release/log-processor"
ORACLE_BIN = "/opt/oracle/log_processor_oracle"

def generate_csv_data(seed):
    random.seed(seed)
    num_rows = random.randint(50, 500)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["timestamp", "ip", "message", "cpu_temp", "gpu_temp"])

    emojis = ["🚨", "📊", "🔥", "❄️", "💻"]

    for _ in range(num_rows):
        timestamp = f"2023-10-01T{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}Z"
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

        msg_len = random.randint(5, 50)
        msg_chars = random.choices(string.ascii_letters + string.digits + " ", k=msg_len)
        if random.random() < 0.3:
            msg_chars.insert(random.randint(0, len(msg_chars)), "\n")
        if random.random() < 0.2:
            msg_chars.append(random.choice(emojis))
        message = "".join(msg_chars)

        cpu_temp = "" if random.random() < 0.15 else f"{random.uniform(30.0, 90.0):.2f}"
        gpu_temp = "" if random.random() < 0.15 else f"{random.uniform(40.0, 100.0):.2f}"

        writer.writerow([timestamp, ip, message, cpu_temp, gpu_temp])

    return output.getvalue().encode('utf-8')

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}. Did you build in release mode?"
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary at {AGENT_BIN} is not executable."

def test_oracle_binary_exists():
    assert os.path.isfile(ORACLE_BIN), f"Oracle binary not found at {ORACLE_BIN}."
    assert os.access(ORACLE_BIN, os.X_OK), f"Oracle binary at {ORACLE_BIN} is not executable."

@pytest.mark.parametrize("seed", range(200))
def test_fuzz_equivalence(seed):
    csv_data = generate_csv_data(seed)

    # Run Oracle
    oracle_proc = subprocess.run(
        [ORACLE_BIN],
        input=csv_data,
        capture_output=True,
        check=False
    )
    assert oracle_proc.returncode == 0, f"Oracle failed on seed {seed} with stderr: {oracle_proc.stderr.decode(errors='replace')}"

    # Run Agent
    agent_proc = subprocess.run(
        [AGENT_BIN],
        input=csv_data,
        capture_output=True,
        check=False
    )
    assert agent_proc.returncode == 0, f"Agent failed on seed {seed} with stderr: {agent_proc.stderr.decode(errors='replace')}"

    # Compare outputs
    oracle_stdout = oracle_proc.stdout
    agent_stdout = agent_proc.stdout

    if oracle_stdout != agent_stdout:
        # Show a snippet of the difference
        oracle_lines = oracle_stdout.decode(errors='replace').splitlines()
        agent_lines = agent_stdout.decode(errors='replace').splitlines()

        diff_idx = -1
        for i, (ol, al) in enumerate(zip(oracle_lines, agent_lines)):
            if ol != al:
                diff_idx = i
                break
        if diff_idx == -1 and len(oracle_lines) != len(agent_lines):
            diff_idx = min(len(oracle_lines), len(agent_lines))

        error_msg = f"Mismatch on seed {seed}.\n"
        if diff_idx != -1:
            error_msg += f"First diff at line {diff_idx + 1}:\n"
            error_msg += f"Oracle: {oracle_lines[diff_idx] if diff_idx < len(oracle_lines) else 'EOF'}\n"
            error_msg += f"Agent : {agent_lines[diff_idx] if diff_idx < len(agent_lines) else 'EOF'}\n"

        pytest.fail(error_msg)