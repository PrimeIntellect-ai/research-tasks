# test_final_state.py

import os
import json
import random
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_processor"
AGENT_PATH = "/home/user/math_service/process.sh"
PROTO_PATH = "/home/user/math_service/proto/service.proto"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script not executable at {AGENT_PATH}"

    random.seed(42)
    for i in range(500):
        data_len = random.randint(1, 100)
        data = [random.randint(0, 1000) for _ in range(data_len)]
        multiplier = random.randint(1, 50)
        shift = random.randint(0, 100)

        input_json = json.dumps({
            "data": data,
            "multiplier": multiplier,
            "shift": shift
        })

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_json, text=True, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_json, text=True, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {input_json}"
        assert agent_proc.returncode == 0, f"Agent script failed on input: {input_json}\nStderr: {agent_proc.stderr}"

        try:
            oracle_out = json.loads(oracle_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle produced invalid JSON: {oracle_proc.stdout}")

        try:
            agent_out = json.loads(agent_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Agent produced invalid JSON: {agent_proc.stdout}\nStderr: {agent_proc.stderr}")

        assert agent_out == oracle_out, f"Mismatch on input {input_json}.\nOracle: {oracle_out}\nAgent: {agent_out}"

def test_proto_updated():
    assert os.path.isfile(PROTO_PATH), f"Proto file missing at {PROTO_PATH}"
    with open(PROTO_PATH, "r") as f:
        content = f.read()

    assert "multiplier" in content, "Proto file does not define the 'multiplier' field."
    assert "shift" in content, "Proto file does not define the 'shift' field."
    assert "result" in content, "Proto file does not define the 'result' field in ProcessResponse."