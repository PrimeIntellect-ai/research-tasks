# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_processor"
    agent_path = "/home/user/processor.sh"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent script missing at {agent_path}"

    random.seed(42)
    N = 50

    for i in range(N):
        L = random.randint(100, 1000)
        sequence = [str(random.randint(1000000000, 1000000500)) for _ in range(L)]
        input_data = "\n".join(sequence) + "\n"

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data.encode('utf-8'),
            capture_output=True,
            timeout=5
        )
        oracle_stdout = oracle_proc.stdout.decode('utf-8')

        # Run agent
        agent_proc = subprocess.run(
            ["bash", agent_path],
            input=input_data.encode('utf-8'),
            capture_output=True,
            timeout=5
        )
        agent_stdout = agent_proc.stdout.decode('utf-8')

        if oracle_stdout != agent_stdout:
            # Provide a truncated view of the mismatch
            oracle_lines = oracle_stdout.splitlines()
            agent_lines = agent_stdout.splitlines()

            error_msg = f"Output mismatch on fuzz iteration {i}.\n"
            error_msg += f"Input length: {L}\n"

            for j in range(max(len(oracle_lines), len(agent_lines))):
                o_line = oracle_lines[j] if j < len(oracle_lines) else "<EOF>"
                a_line = agent_lines[j] if j < len(agent_lines) else "<EOF>"
                if o_line != a_line:
                    error_msg += f"First mismatch at line {j+1}:\n"
                    error_msg += f"Input value: {sequence[j] if j < len(sequence) else 'N/A'}\n"
                    error_msg += f"Expected (oracle): {o_line}\n"
                    error_msg += f"Got (agent)      : {a_line}\n"
                    break

            pytest.fail(error_msg)

def test_pipeline_running():
    alerts_log = "/home/user/alerts.log"
    assert os.path.exists(alerts_log), f"{alerts_log} does not exist. Pipeline may not be running."

    with open(alerts_log, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 5, f"Expected at least 5 lines in {alerts_log}, but found {len(lines)}."