# test_final_state.py
import os
import subprocess
import random
import pytest

AGENT_SCRIPT = "/home/user/simulate_gene.py"
ORACLE_SCRIPT = "/app/oracle_simulate.py"

def test_agent_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

def run_script(script_cmd, arg):
    try:
        result = subprocess.run(
            script_cmd + [arg],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return None, "Timeout", -1

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script not found at {ORACLE_SCRIPT}"

    # Generate test cases
    random.seed(42)
    test_cases = [""] # Edge case: empty string

    for _ in range(500):
        length = random.randint(10, 100)
        seq = "".join(random.choices("ACGT", k=length))
        test_cases.append(seq)

    agent_cmd = ["python3", AGENT_SCRIPT]
    oracle_cmd = [ORACLE_SCRIPT] # Oracle is executable

    for seq in test_cases:
        oracle_out, oracle_err, oracle_rc = run_script(oracle_cmd, seq)
        agent_out, agent_err, agent_rc = run_script(agent_cmd, seq)

        assert agent_out is not None, f"Agent script timed out on input: '{seq}'"
        assert agent_out == oracle_out, (
            f"Output mismatch on input: '{seq}'\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}\n"
            f"Agent stderr: {agent_err}"
        )