# test_final_state.py
import os
import sys
import json
import base64
import random
import subprocess
import pytest

def test_core_py_fixed():
    core_py_path = "/app/vendor/log_extractor-1.0/log_extractor/core.py"
    assert os.path.isfile(core_py_path), f"File {core_py_path} is missing."
    with open(core_py_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Accept 'utf-8', "utf-8", 'utf8', "utf8"
    assert "utf-8" in content.lower() or "utf8" in content.lower(), "The bug in core.py does not appear to be fixed to decode as utf-8."

def test_fuzz_equivalence_and_logging():
    agent_script = "/home/user/analyzer.py"
    oracle_script = "/app/oracle/analyzer_oracle.py"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} missing."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} missing."

    log_file = "/home/user/pipeline.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    random.seed(42)
    texts = [
        "System normal", 
        "User login successful", 
        "CRÍTICO: database failure", 
        "Disk space 严重 low", 
        "KRITISCH: overload", 
        "Warning 🚨", 
        "All good 123", 
        "こんにちは"
    ]

    N = 100
    uids_processed = []

    for _ in range(N):
        uid = random.randint(1000, 9999)
        chosen = random.choice(texts)
        raw_b64 = base64.b64encode(chosen.encode('utf-8')).decode('ascii')
        input_data = json.dumps({"uid": uid, "raw_b64": raw_b64})

        uids_processed.append(uid)

        # Run oracle
        oracle_proc = subprocess.run(
            [sys.executable, oracle_script],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {input_data}"
        oracle_out = json.loads(oracle_proc.stdout.strip())

        # Run agent
        agent_proc = subprocess.run(
            [sys.executable, agent_script],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input {input_data}\nStderr: {agent_proc.stderr}"
        try:
            agent_out = json.loads(agent_proc.stdout.strip())
        except json.JSONDecodeError:
            pytest.fail(f"Agent did not output valid JSON on input {input_data}.\nOutput: {agent_proc.stdout}")

        assert oracle_out == agent_out, f"Mismatch on input {input_data}.\nOracle: {oracle_out}\nAgent: {agent_out}"

    # Check pipeline.log
    assert os.path.isfile(log_file), f"Pipeline log {log_file} was not created."
    with open(log_file, "r", encoding="utf-8") as f:
        log_lines = [line.strip() for line in f if line.strip()]

    assert len(log_lines) == N, f"Expected {N} lines in {log_file}, got {len(log_lines)}"

    for uid, line in zip(uids_processed, log_lines):
        expected_line = f"[INFO] Processed uid {uid}"
        assert line == expected_line, f"Log line mismatch. Expected '{expected_line}', got '{line}'"