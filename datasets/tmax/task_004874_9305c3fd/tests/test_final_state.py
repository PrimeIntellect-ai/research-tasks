# test_final_state.py

import os
import random
import base64
import subprocess
import urllib.request
import json
import pytest

APP_DIR = "/home/user/app"
GATEWAY_PATH = os.path.join(APP_DIR, "gateway.js")
WORKER_PATH = os.path.join(APP_DIR, "worker.py")
ORACLE_PATH = os.path.join(APP_DIR, "oracle_worker")

def test_gateway_js_fixed():
    assert os.path.isfile(GATEWAY_PATH), f"{GATEWAY_PATH} is missing."
    with open(GATEWAY_PATH, "r") as f:
        content = f.read()

    assert "6379" in content, "gateway.js does not contain the correct Redis port 6379."
    assert "6380" not in content, "gateway.js still contains the incorrect Redis port 6380."
    assert "math_jobs" in content, "gateway.js does not contain the correct queue name 'math_jobs'."
    assert "old_jobs" not in content, "gateway.js still contains the incorrect queue name 'old_jobs'."

def test_worker_py_exists():
    assert os.path.isfile(WORKER_PATH), f"{WORKER_PATH} is missing."

def test_end_to_end_api():
    """Test the end-to-end flow via the Node.js API gateway."""
    payload = json.dumps({"expr": "(DIV -10 3)"}).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:8080/calc",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode("utf-8"))
            assert "result" in data, "Response JSON missing 'result' key."
            assert data["result"] == -4, f"Expected result -4, got {data['result']} (Python 2 division semantics not replicated?)"
    except urllib.error.URLError as e:
        pytest.fail(f"End-to-end API request failed. Is the gateway and worker running? Error: {e}")

def generate_ast(depth, max_depth):
    if depth >= max_depth or (depth > 1 and random.random() < 0.3):
        # Generate leaf node
        val = random.randint(-100000, 100000)
        # Avoid generating 0 to minimize division by zero issues in fuzzing
        if val == 0:
            val = 1
        return str(val)

    op = random.choice(["ADD", "SUB", "MUL", "DIV"])
    left = generate_ast(depth + 1, max_depth)
    right = generate_ast(depth + 1, max_depth)

    return f"({op} {left} {right})"

def generate_fuzz_inputs(n):
    random.seed(42)
    inputs = []
    for _ in range(n):
        depth = random.randint(1, 5)
        expr = generate_ast(1, depth)
        b64_expr = base64.b64encode(expr.encode("utf-8")).decode("utf-8")
        inputs.append((expr, b64_expr))
    return inputs

def test_fuzz_equivalence():
    """Fuzz equivalence test against the oracle binary."""
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} is missing."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable."

    inputs = generate_fuzz_inputs(500)

    for expr, b64_expr in inputs:
        oracle_cmd = [ORACLE_PATH, "--cli", b64_expr]
        agent_cmd = ["python3", WORKER_PATH, "--cli", b64_expr]

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        # If oracle crashed (e.g. division by zero), we skip or expect agent to also crash/error
        if oracle_res.returncode != 0 and agent_res.returncode != 0:
            continue

        assert oracle_out == agent_out, (
            f"Mismatch on input expr: {expr}\n"
            f"Base64: {b64_expr}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )