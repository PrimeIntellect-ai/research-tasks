# test_final_state.py

import os
import random
import string
import subprocess
import json
import uuid
import pytest

def generate_csv_lines(n):
    random.seed(42)
    lines = []
    chars = string.ascii_letters + string.digits + string.punctuation + " "
    for _ in range(n):
        id_str = str(uuid.UUID(int=random.getrandbits(128), version=4))
        length = random.randint(10, 500)
        text = "".join(random.choices(chars, k=length))
        # Ensure no newlines in text itself to maintain simple CSV format
        text = text.replace('\n', ' ').replace('\r', ' ')
        lines.append(f"{id_str},{text}\n")
    return "".join(lines)

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_cleaner"
    agent_path = "/home/user/cleaner"

    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    # Generate 10,000 lines as per truth description
    num_lines = 10000
    input_data = generate_csv_lines(num_lines)
    input_data_bytes = input_data.encode('utf-8')

    # Run oracle
    try:
        oracle_proc = subprocess.run([oracle_path], input=input_data_bytes, capture_output=True, timeout=30)
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle timed out")
    assert oracle_proc.returncode == 0, f"Oracle failed with error: {oracle_proc.stderr.decode('utf-8')}"
    oracle_lines = oracle_proc.stdout.decode('utf-8').strip().split('\n')

    # Run agent
    try:
        agent_proc = subprocess.run([agent_path], input=input_data_bytes, capture_output=True, timeout=30)
    except subprocess.TimeoutExpired:
        pytest.fail("Agent binary timed out")
    assert agent_proc.returncode == 0, f"Agent binary failed with error: {agent_proc.stderr.decode('utf-8')}"
    agent_lines = agent_proc.stdout.decode('utf-8').strip().split('\n')

    # Handle case where output is empty but shouldn't be
    if oracle_lines == [''] and num_lines > 0:
        oracle_lines = []
    if agent_lines == [''] and num_lines > 0:
        agent_lines = []

    assert len(oracle_lines) == len(agent_lines), f"Output line counts differ. Oracle: {len(oracle_lines)}, Agent: {len(agent_lines)}"

    # Compare JSON outputs
    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        try:
            o_json = json.loads(o_line)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle produced invalid JSON at line {i+1}: {o_line}")

        try:
            a_json = json.loads(a_line)
        except json.JSONDecodeError:
            pytest.fail(f"Agent produced invalid JSON at line {i+1}: {a_line}")

        assert o_json == a_json, f"Mismatch at line {i+1}.\nInput: {input_data.splitlines()[i]}\nOracle: {o_json}\nAgent: {a_json}"

def test_pipeline_env_configured():
    env_file = "/app/pipeline.env"
    assert os.path.exists(env_file), f"Missing pipeline.env at {env_file}"

    with open(env_file, 'r') as f:
        content = f.read()

    # Check for correct SOURCE_URL
    assert "SOURCE_URL=http://127.0.0.1:8081/stream" in content or "SOURCE_URL=http://localhost:8081/stream" in content, \
        "SOURCE_URL is incorrectly configured in /app/pipeline.env"

    # Check for correct SINK_URL
    assert "SINK_URL=http://127.0.0.1:8082/ingest" in content or "SINK_URL=http://localhost:8082/ingest" in content, \
        "SINK_URL is incorrectly configured in /app/pipeline.env"