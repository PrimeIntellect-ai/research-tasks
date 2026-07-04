# test_final_state.py
import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/legacy_matcher"
AGENT_PATH = "/home/user/new_matcher.py"

def generate_test_case(seed):
    random.seed(seed)

    N = random.randint(10, 50)
    M = random.randint(20, 150)
    Q = random.randint(5, 20)

    edge_types = ["REL_A", "REL_B", "REL_C", "REL_D"]

    edges = []
    for _ in range(M):
        u = random.randint(0, N - 2)
        v = random.randint(u + 1, N - 1)
        weight = round(random.uniform(0.1, 5.0), 2)
        etype = random.choice(edge_types)
        edges.append(f"{u} {v} {weight:.2f} {etype}")

    queries = []
    for _ in range(Q):
        start = random.randint(0, N - 2)
        end = random.randint(start + 1, N - 1)
        seq_len = random.randint(1, 4)
        seq = ",".join(random.choices(edge_types, k=seq_len))
        queries.append(f"{start} {end} {seq}")

    input_lines = [f"{N} {M} {Q}"] + edges + queries
    return "\n".join(input_lines) + "\n"

def run_program(cmd, input_data):
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            text=True,
            capture_output=True,
            timeout=5,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle {ORACLE_PATH} not found."
    assert os.path.exists(AGENT_PATH), f"Agent script {AGENT_PATH} not found."

    agent_cmd = ["python3", AGENT_PATH]
    oracle_cmd = [ORACLE_PATH]

    for i in range(100):
        input_data = generate_test_case(seed=1000 + i)

        oracle_out = run_program(oracle_cmd, input_data)
        agent_out = run_program(agent_cmd, input_data)

        if oracle_out != agent_out:
            error_msg = (
                f"Mismatch on test case {i}!\n\n"
                f"Input Data:\n{input_data}\n"
                f"Oracle Output:\n{oracle_out}\n"
                f"Agent Output:\n{agent_out}\n"
            )
            pytest.fail(error_msg)