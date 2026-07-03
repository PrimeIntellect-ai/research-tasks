# test_final_state.py

import os
import subprocess
import random
import pytest

def test_plot_experiments_fixed():
    script_path = "/home/user/plot_experiments.py"
    plot_path = "/home/user/experiment_plot.png"

    # Run the script to generate the plot
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"plot_experiments.py failed to run:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    # Check if the plot was created and is not empty
    assert os.path.exists(plot_path), f"Plot file {plot_path} was not created."
    assert os.path.getsize(plot_path) > 100, f"Plot file {plot_path} is suspiciously small or empty."

def test_new_oracle_fuzz_equivalence():
    oracle_path = "/app/drift_oracle"
    agent_script = "/home/user/new_oracle.py"

    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."

    random.seed(42)

    for i in range(100):
        length = random.randint(5, 100)
        actual_vals = [str(random.randint(0, 10000)) for _ in range(length)]
        predicted_vals = [str(random.randint(0, 10000)) for _ in range(length)]

        actual_csv = ",".join(actual_vals)
        predicted_csv = ",".join(predicted_vals)

        # Run oracle
        oracle_result = subprocess.run(
            [oracle_path, actual_csv, predicted_csv],
            capture_output=True,
            text=True
        )
        assert oracle_result.returncode == 0, f"Oracle failed on iteration {i} with input length {length}."
        oracle_output = oracle_result.stdout.strip()

        # Run agent script
        agent_result = subprocess.run(
            ["python3", agent_script, actual_csv, predicted_csv],
            capture_output=True,
            text=True
        )
        assert agent_result.returncode == 0, f"Agent script failed on iteration {i}:\nSTDERR: {agent_result.stderr}"
        agent_output = agent_result.stdout.strip()

        assert agent_output == oracle_output, (
            f"Mismatch on iteration {i}!\n"
            f"Input actual: {actual_csv[:50]}...\n"
            f"Input predicted: {predicted_csv[:50]}...\n"
            f"Oracle output: '{oracle_output}'\n"
            f"Agent output: '{agent_output}'"
        )