# test_final_state.py

import os
import subprocess
import pytest

def test_orchestrate_script_exists_and_executable():
    """Check if orchestrate.sh exists and is executable."""
    script_path = "/home/user/sim/orchestrate.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_orchestrate_execution_and_result():
    """Run orchestrate.sh and verify the result.log output."""
    script_path = "/home/user/sim/orchestrate.sh"

    # Run the orchestration script
    result = subprocess.run([script_path], cwd="/home/user/sim", capture_output=True, text=True)
    assert result.returncode == 0, f"orchestrate.sh failed with return code {result.returncode}. stderr: {result.stderr}"

    log_path = "/home/user/sim/result.log"
    assert os.path.isfile(log_path), f"{log_path} was not created by orchestrate.sh."

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    assert log_content == "REPRODUCIBLE", f"Expected result.log to contain 'REPRODUCIBLE', got '{log_content}'"

def test_sum_potentials_correctness():
    """Verify that sum_potentials produces the correct Kahan sum."""
    executable_path = "/home/user/sim/sum_potentials"
    data_path = "/home/user/sim/data.txt"

    assert os.path.isfile(executable_path), f"{executable_path} is missing. Did orchestrate.sh compile it?"

    result = subprocess.run([executable_path, data_path], capture_output=True, text=True)
    assert result.returncode == 0, "sum_potentials failed to execute."

    output = result.stdout.strip()
    expected_output = "10010000.000000"

    assert output == expected_output, f"Expected sum_potentials to output {expected_output}, got {output}. Kahan summation may not be correctly implemented."

def test_c_source_contains_kahan_logic():
    """Check if sum_potentials.c contains variables typical of Kahan summation."""
    c_file = "/home/user/sim/sum_potentials.c"
    assert os.path.isfile(c_file), f"{c_file} is missing."

    with open(c_file, "r") as f:
        content = f.read()

    # A naive sum is just sum += val. Kahan uses a compensation variable (e.g., c).
    # We won't strictly check for 'c' but we can check that it doesn't just do naive sum.
    # The output test is the strongest assertion, but we can ensure it's not just returning a hardcoded value.
    assert "fopen" in content, "Source file seems to have lost file reading logic."
    assert "fscanf" in content, "Source file seems to have lost file parsing logic."