# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

ORACLE_PATH = "/opt/oracle/in_degree_oracle"
AGENT_PATH = "/app/libcsv-graph/in_degree"
NUM_FUZZ_CASES = 50

def generate_fuzz_case(seed):
    random.seed(seed)
    num_edges = random.randint(10, 500)
    csv_lines = []
    for _ in range(num_edges):
        source = random.randint(1, 100)
        target = random.randint(1, 100)
        weight = random.randint(1, 50)
        csv_lines.append(f"{source},{target},{weight}")

    threshold = random.randint(0, 100)
    limit = random.randint(1, 20)
    offset = random.randint(0, 20)

    return "\n".join(csv_lines) + "\n", threshold, limit, offset

def run_program(executable, csv_path, threshold, limit, offset):
    cmd = [executable, csv_path, str(threshold), str(limit), str(offset)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def test_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Executable not found at {AGENT_PATH}. Did you run 'make'?"
    assert os.access(AGENT_PATH, os.X_OK), f"File at {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}. Cannot verify."

    for i in range(NUM_FUZZ_CASES):
        csv_content, threshold, limit, offset = generate_fuzz_case(i + 1000)

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            oracle_stdout, oracle_stderr, oracle_rc = run_program(ORACLE_PATH, tmp_path, threshold, limit, offset)
            agent_stdout, agent_stderr, agent_rc = run_program(AGENT_PATH, tmp_path, threshold, limit, offset)

            error_msg = (
                f"Mismatch on fuzz case {i} (seed {i+1000}):\n"
                f"Threshold: {threshold}, Limit: {limit}, Offset: {offset}\n"
                f"Input CSV:\n{csv_content[:200]}...\n\n"
                f"Oracle Output:\n{oracle_stdout}\n"
                f"Agent Output:\n{agent_stdout}\n"
            )

            assert agent_rc == oracle_rc, f"Return code mismatch. Oracle: {oracle_rc}, Agent: {agent_rc}\n{error_msg}"
            assert agent_stdout == oracle_stdout, f"Output mismatch.\n{error_msg}"
        finally:
            os.remove(tmp_path)