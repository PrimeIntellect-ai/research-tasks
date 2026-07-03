# test_final_state.py

import os
import json
import base64
import random
import subprocess
import re
import pytest

AGENT_SCRIPT = "/home/user/audit_wrapper.sh"
ORACLE_SCRIPT = "/opt/oracle/audit_wrapper_oracle"
TOKEN_TOOL = "/app/libauthtoken-1.2.0/token_tool"

def create_jwt(sub, exp):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {}
    if sub is not None:
        payload["sub"] = sub
    if exp is not None:
        payload["exp"] = exp

    h_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    p_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    sig = base64.urlsafe_b64encode(b"fakesig").decode().rstrip("=")
    return f"{h_b64}.{p_b64}.{sig}"

def normalize_output(output):
    # The timestamp can vary by a second between runs, so we normalize it for comparison.
    return re.sub(r"timestamp=\d+", "timestamp=X", output.strip())

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script at {AGENT_SCRIPT} is not executable"

def test_token_tool_compiled():
    assert os.path.isfile(TOKEN_TOOL), f"Compiled token_tool not found at {TOKEN_TOOL}"
    assert os.access(TOKEN_TOOL, os.X_OK), f"token_tool at {TOKEN_TOOL} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script not found at {ORACLE_SCRIPT}"

    random.seed(42)
    subjects = [
        "admin", 
        "user", 
        "<script>alert(1)</script>", 
        "UNION SELECT * FROM users", 
        "' OR 1=1", 
        "normal_user_123",
        None
    ]
    exps = [
        None,
        1500000000, # expired
        2000000000, # valid
        2147483647, # max valid
        2147483648, # overflow
        9999999999  # large overflow
    ]

    # Generate 1000 test cases
    tokens = []
    for _ in range(1000):
        sub = random.choice(subjects)
        exp = random.choice(exps)
        tokens.append(create_jwt(sub, exp))

    for token in tokens:
        oracle_proc = subprocess.run([ORACLE_SCRIPT, token], capture_output=True, text=True)
        agent_proc = subprocess.run([AGENT_SCRIPT, token], capture_output=True, text=True)

        oracle_out = normalize_output(oracle_proc.stdout)
        agent_out = normalize_output(agent_proc.stdout)

        assert oracle_out == agent_out, (
            f"Mismatch for token: {token}\n"
            f"Oracle output: {oracle_proc.stdout.strip()}\n"
            f"Agent output:  {agent_proc.stdout.strip()}"
        )