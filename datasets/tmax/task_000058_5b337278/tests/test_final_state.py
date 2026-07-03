# test_final_state.py

import os
import subprocess
import random
import string
import urllib.request
import urllib.error
import pytest

def generate_input():
    num_lines = random.randint(0, 100)
    lines = []
    for _ in range(num_lines):
        id_len = random.randint(4, 8)
        id_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(id_len))
        timestamp = random.randint(1600000000, 1700000000)
        num_vals = random.randint(1, 20)
        vals = [f"{random.uniform(-100.5, 100.5):.2f}" for _ in range(num_vals)]
        lines.append(f"{id_str}|{timestamp}|{','.join(vals)}")
    return "\n".join(lines) + ("\n" if num_lines > 0 else "")

def test_fuzz_equivalence():
    oracle_path = "/app/legacy/process_v2.py"
    agent_path = "/home/user/migrated/processor"

    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    for i in range(500):
        inp = generate_input()

        # Run oracle
        oracle_proc = subprocess.run(
            ["python2", oracle_path],
            input=inp,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input:\n{inp}\nError:\n{oracle_proc.stderr}"

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=inp,
            text=True,
            capture_output=True
        )

        if agent_proc.returncode != 0 or agent_proc.stdout != oracle_proc.stdout:
            pytest.fail(
                f"Mismatch on iteration {i}.\n"
                f"Input:\n{inp}\n\n"
                f"Oracle Output:\n{oracle_proc.stdout}\n\n"
                f"Agent Output:\n{agent_proc.stdout}\n\n"
                f"Agent Stderr:\n{agent_proc.stderr}"
            )

def test_e2e_service_composition():
    random.seed(999)
    inp = generate_input()

    # Get expected from oracle
    oracle_proc = subprocess.run(
        ["python2", "/app/legacy/process_v2.py"],
        input=inp,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, "Oracle failed to generate expected output."
    expected_output = oracle_proc.stdout

    req = urllib.request.Request(
        "http://localhost:8080/api/process",
        data=inp.encode('utf-8'),
        headers={'Content-Type': 'text/plain'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            resp_body = response.read().decode('utf-8')
            assert resp_body == expected_output, (
                f"E2E response mismatch.\nExpected:\n{expected_output}\nGot:\n{resp_body}"
            )
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTP request failed with status {e.code}: {e.read().decode('utf-8', errors='replace')}")
    except urllib.error.URLError as e:
        pytest.fail(f"HTTP request failed: {e.reason}")