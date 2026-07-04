# test_final_state.py

import os
import subprocess
import time
import json
import random
import string
import pytest

def test_gateway_config():
    config_path = "/home/user/app/gateway/config.yaml"
    assert os.path.isfile(config_path), f"{config_path} is missing"
    with open(config_path, "r") as f:
        content = f.read()
    assert "50051" in content, "gateway config missing auth target port 50051"
    assert "50052" in content, "gateway config missing backend target port 50052"

def test_proto_file_updated():
    proto_path = "/home/user/app/proto/auth.proto"
    assert os.path.isfile(proto_path), f"{proto_path} is missing"
    with open(proto_path, "r") as f:
        content = f.read()
    assert "map<string, string> attributes = 3;" in content, "auth.proto is missing the required attributes field in CheckRequest"

def generate_expression_and_context(depth=0):
    if depth > 3 or random.random() < 0.3:
        # Base case: comparison
        var = random.choice(string.ascii_lowercase)
        val = "".join(random.choices(string.ascii_lowercase, k=3))
        op = random.choice(["==", "!="])
        expr = f"{var} {op} '{val}'"
        return expr, {var: val if random.random() < 0.5 else "other"}
    else:
        # Recursive case: logical operator
        left_expr, left_ctx = generate_expression_and_context(depth + 1)
        right_expr, right_ctx = generate_expression_and_context(depth + 1)
        op = random.choice(["&&", "||"])
        expr = f"({left_expr} {op} {right_expr})"
        ctx = {**left_ctx, **right_ctx}
        return expr, ctx

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/evaluator"
    agent_path = "/home/user/app/auth/auth_eval"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    N = 500

    for i in range(N):
        expr, ctx = generate_expression_and_context()
        ctx_json = json.dumps(ctx)

        oracle_proc = subprocess.run([oracle_path, expr, ctx_json], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, expr, ctx_json], capture_output=True, text=True)

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i}.\n"
            f"Expression: {expr}\n"
            f"Context: {ctx_json}\n"
            f"Oracle stdout: {oracle_out}\n"
            f"Oracle stderr: {oracle_proc.stderr.strip()}\n"
            f"Agent stdout: {agent_out}\n"
            f"Agent stderr: {agent_proc.stderr.strip()}"
        )

def test_end_to_end_flow():
    start_script = "/home/user/app/start.sh"
    assert os.path.isfile(start_script), f"{start_script} is missing"
    assert os.access(start_script, os.X_OK), f"{start_script} is not executable"

    # Run the start script
    proc = subprocess.Popen([start_script], cwd="/home/user/app", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Wait for services to boot
        time.sleep(3)

        # Test the endpoint
        curl_cmd = [
            "curl", "-s", "-w", "%{http_code}", "-o", "/dev/null",
            "-X", "POST", "http://localhost:8080/secure-data",
            "-H", "X-Role: admin",
            "-H", "X-Action: read"
        ]

        curl_proc = subprocess.run(curl_cmd, capture_output=True, text=True)
        http_code = curl_proc.stdout.strip()

        assert http_code == "200", f"Expected HTTP 200 OK, but got {http_code}"
    finally:
        # Cleanup processes started by start.sh (best effort)
        subprocess.run(["pkill", "-f", "gateway|auth|backend"], capture_output=True)
        proc.terminate()