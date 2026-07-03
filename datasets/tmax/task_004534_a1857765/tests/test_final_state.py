# test_final_state.py
import os
import subprocess
import random
import json

def test_math_port_script_exists_and_executable():
    script_path = "/home/user/math_port.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_math"
    agent_path = "/home/user/math_port.sh"

    assert os.path.exists(oracle_path), f"Oracle {oracle_path} missing."

    random.seed(42)
    test_cases = [random.randint(1, 100000) for _ in range(100)]

    for n in test_cases:
        payload = json.dumps({"query": {"value": n}})

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=payload,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["bash", agent_path],
            input=payload,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed on input {payload}. Stderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout.strip()

        assert agent_output == oracle_output, (
            f"Mismatch on input {payload}.\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )