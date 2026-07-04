# test_final_state.py

import os
import json
import random
import string
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/oracle_query"
AGENT_SCRIPT = "/home/user/query.py"
N_TESTS = 100

def generate_random_json(depth=0):
    if depth > 3:
        return random.choice([
            random.randint(1, 100),
            ''.join(random.choices(string.ascii_letters, k=5))
        ])

    t = random.choice(['dict', 'list', 'int', 'str'])
    if t == 'dict':
        return {f"key_{i}": generate_random_json(depth + 1) for i in range(random.randint(1, 5))}
    elif t == 'list':
        return [generate_random_json(depth + 1) for _ in range(random.randint(1, 5))]
    elif t == 'int':
        return random.randint(1, 100)
    else:
        return ''.join(random.choices(string.ascii_letters, k=5))

def generate_random_query():
    queries = [
        "length(@)",
        "length(key_0)",
        "length(key_0 || `[]`)",
        "contains(@, `1`)",
        "contains(key_0 || `[]`, `10`)",
        "contains(@, `\"abc\"`)",
        "sort(@)",
        "sort(key_0 || `[]`)",
        "key_0",
        "key_0.key_1",
        "length(key_0.key_1 || `[]`)",
        "contains(key_1 || `[]`, `5`)",
    ]
    return random.choice(queries)

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle not executable at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = os.path.join(tmpdir, "test.json")

        for i in range(N_TESTS):
            data = generate_random_json()
            query = generate_random_query()

            with open(json_path, "w") as f:
                json.dump(data, f)

            # Run oracle
            oracle_cmd = [ORACLE_PATH, json_path, query]
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)

            # Run agent
            agent_cmd = ["python3", AGENT_SCRIPT, json_path, query]
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

            # Assert return codes match
            assert oracle_res.returncode == agent_res.returncode, (
                f"Return code mismatch on iteration {i}.\n"
                f"Query: {query}\n"
                f"JSON: {json.dumps(data)}\n"
                f"Oracle returncode: {oracle_res.returncode}\n"
                f"Agent returncode: {agent_res.returncode}\n"
                f"Oracle stderr: {oracle_res.stderr}\n"
                f"Agent stderr: {agent_res.stderr}"
            )

            # Assert stdout matches exactly
            assert oracle_res.stdout == agent_res.stdout, (
                f"Output mismatch on iteration {i}.\n"
                f"Query: {query}\n"
                f"JSON: {json.dumps(data)}\n"
                f"Oracle output: {repr(oracle_res.stdout)}\n"
                f"Agent output: {repr(agent_res.stdout)}"
            )

def test_script_imports_vendored():
    with open(AGENT_SCRIPT, "r") as f:
        content = f.read()
    assert "sys.path.insert(0, '/app/vendored/jmespath-1.0.1')" in content or "sys.path.insert(0,'/app/vendored/jmespath-1.0.1')" in content or "sys.path.insert(0, \"/app/vendored/jmespath-1.0.1\")" in content, \
        "Agent script does not appear to prepend the vendored directory to sys.path."