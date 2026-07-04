# test_final_state.py
import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    agent_binary = "/home/user/query_engine"
    oracle_binary = "/app/oracle_engine"

    assert os.path.isfile(agent_binary), f"Agent program {agent_binary} not found."
    assert os.access(agent_binary, os.X_OK), f"Agent program {agent_binary} is not executable."
    assert os.path.isfile(oracle_binary), f"Oracle program {oracle_binary} not found."

    # Determine which CSV to use (prefer test_network if available)
    test_csv = "/app/test_network.csv"
    if not os.path.isfile(test_csv):
        test_csv = "/home/user/network.csv"

    assert os.path.isfile(test_csv), f"Test CSV {test_csv} not found."

    # Extract distinct nodes from the CSV
    nodes = set()
    with open(test_csv, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                try:
                    nodes.add(int(parts[0]))
                    nodes.add(int(parts[1]))
                except ValueError:
                    pass

    nodes_list = list(nodes)
    if not nodes_list:
        pytest.fail("No valid nodes found in the CSV file.")

    # Generate 500 random queries
    random.seed(42)
    queries = []
    for _ in range(500):
        u = random.choice(nodes_list)
        v = random.choice(nodes_list)
        queries.append(f"{u} {v}")

    input_data = "\n".join(queries) + "\n"

    # Run the oracle
    try:
        oracle_proc = subprocess.run(
            [oracle_binary, test_csv],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=15,
            check=True
        )
        oracle_output = oracle_proc.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle program failed to execute properly: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle program timed out.")

    # Run the agent
    try:
        agent_proc = subprocess.run(
            [agent_binary, test_csv],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=15
        )
        agent_output = agent_proc.stdout.strip().split("\n")
    except subprocess.TimeoutExpired:
        pytest.fail("Agent program timed out. Ensure it is efficient and processes stdin to EOF.")

    if agent_proc.returncode != 0:
        pytest.fail(f"Agent program exited with non-zero code {agent_proc.returncode}:\n{agent_proc.stderr}")

    # Handle edge case where output is completely empty but split("\n") gives [""]
    if agent_output == [""] and oracle_output != [""]:
        pytest.fail("Agent program produced no output.")

    assert len(agent_output) == len(oracle_output), (
        f"Output length mismatch. Expected {len(oracle_output)} lines, got {len(agent_output)}."
    )

    # Compare outputs line by line
    for i, (query, expected, actual) in enumerate(zip(queries, oracle_output, agent_output)):
        assert expected.strip() == actual.strip(), (
            f"Mismatch on query '{query}' (line {i+1}): Expected {expected.strip()}, got {actual.strip()}"
        )