# test_final_state.py
import os
import random
import subprocess

def test_edges_file_exists():
    """Check if the extracted edges file exists."""
    edges_path = "/home/user/edges.txt"
    assert os.path.isfile(edges_path), f"Edges file {edges_path} is missing."

def test_query_source_exists():
    """Check if the C source file exists."""
    source_path = "/home/user/query.c"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

def test_query_executable_exists():
    """Check if the compiled executable exists and is executable."""
    exe_path = "/home/user/query"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"Executable {exe_path} is not executable."

def test_fuzz_equivalence():
    """Fuzz test the agent's executable against the oracle."""
    oracle_path = "/app/oracle"
    agent_path = "/home/user/query"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"

    # Generate N=500 random inputs
    random.seed(42)
    inputs = []
    for _ in range(500):
        u = random.randint(0, 255)
        v = random.randint(0, 255)
        inputs.append(f"{u} {v}")

    input_data = "\n".join(inputs) + "\n"

    # Run the oracle
    oracle_proc = subprocess.run(
        [oracle_path], 
        input=input_data, 
        text=True, 
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed to run: {oracle_proc.stderr}"

    # Run the agent's program
    agent_proc = subprocess.run(
        [agent_path], 
        input=input_data, 
        text=True, 
        capture_output=True
    )

    oracle_lines = oracle_proc.stdout.strip().split('\n')
    agent_lines = agent_proc.stdout.strip().split('\n')

    assert len(oracle_lines) == len(agent_lines), (
        f"Output line count mismatch: Oracle produced {len(oracle_lines)} lines, "
        f"Agent produced {len(agent_lines)} lines."
    )

    for i, (in_str, o_line, a_line) in enumerate(zip(inputs, oracle_lines, agent_lines)):
        assert o_line == a_line, (
            f"Mismatch on input '{in_str}':\n"
            f"Expected (Oracle): {o_line}\n"
            f"Got (Agent):       {a_line}"
        )