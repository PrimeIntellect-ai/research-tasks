# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def generate_random_id():
    length = random.randint(2, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_fuzz_inputs(n=1000, seed=42):
    random.seed(seed)
    entities = ["Employee", "Customer", "Product"]
    commands = ["MATCH_HIERARCHY", "AGGREGATE_REACH", "FIND_INTERSECT"]

    lines = []
    for _ in range(n):
        cmd = random.choice(commands)
        if cmd == "MATCH_HIERARCHY":
            entity = random.choice(entities)
            start_id = generate_random_id()
            max_depth = random.randint(1, 10)
            lines.append(f"{cmd} {entity} {start_id} {max_depth}")
        elif cmd == "AGGREGATE_REACH":
            entity = random.choice(entities)
            start_id = generate_random_id()
            lines.append(f"{cmd} {entity} {start_id}")
        elif cmd == "FIND_INTERSECT":
            entity1 = random.choice(entities)
            id1 = generate_random_id()
            entity2 = random.choice(entities)
            id2 = generate_random_id()
            lines.append(f"{cmd} {entity1} {id1} {entity2} {id2}")
    return "\n".join(lines) + "\n"

def test_cypher_generator_fuzz_equivalence():
    agent_bin = "/home/user/cypher_generator"
    oracle_bin = "/app/oracle_cypher_gen"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary at {oracle_bin} is not executable"

    input_data = generate_fuzz_inputs(n=1000, seed=1337)

    # Run oracle
    try:
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            timeout=10
        )
        oracle_output = oracle_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle failed to execute: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle timed out.")

    # Run agent
    try:
        agent_proc = subprocess.run(
            [agent_bin],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            timeout=10
        )
        agent_output = agent_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent binary failed to execute: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Agent binary timed out.")

    oracle_lines = oracle_output.strip().split('\n')
    agent_lines = agent_output.strip().split('\n')
    input_lines = input_data.strip().split('\n')

    assert len(agent_lines) == len(oracle_lines), (
        f"Output line count mismatch. Expected {len(oracle_lines)}, got {len(agent_lines)}"
    )

    for i, (oracle_line, agent_line) in enumerate(zip(oracle_lines, agent_lines)):
        assert oracle_line == agent_line, (
            f"Mismatch on input line {i+1}:\n"
            f"Input:  {input_lines[i]}\n"
            f"Oracle: {oracle_line}\n"
            f"Agent:  {agent_line}"
        )