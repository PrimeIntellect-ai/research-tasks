# test_final_state.py

import os
import subprocess
import pytest

def test_evaluate_script_exists():
    script_path = "/home/user/evaluate.py"
    assert os.path.exists(script_path), f"Evaluation script not found at {script_path}"
    assert os.path.isfile(script_path), f"Path {script_path} is not a file"

def test_evaluate_script_output_metric():
    script_path = "/home/user/evaluate.py"
    test_fasta_path = "/home/user/data/hidden_test.fasta"

    assert os.path.exists(script_path), f"Cannot run test: {script_path} does not exist."
    assert os.path.exists(test_fasta_path), f"Cannot run test: {test_fasta_path} does not exist."

    try:
        result = subprocess.run(
            ["python3", script_path, test_fasta_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"evaluate.py failed with return code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("evaluate.py timed out after 30 seconds.")

    output = result.stdout.strip()
    assert output, "evaluate.py produced no standard output."

    try:
        mll_value = float(output)
    except ValueError:
        pytest.fail(f"evaluate.py output could not be parsed as a float. Output was: {output!r}")

    threshold = -12.5
    assert mll_value >= threshold, (
        f"Mean Log-Likelihood (MLL) is too low. "
        f"Expected >= {threshold}, but got {mll_value}."
    )