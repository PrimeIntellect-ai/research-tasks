# test_final_state.py
import os
import subprocess
import pytest

def test_restored_graph_exists():
    path = "/home/user/restored_graph.jsonl"
    assert os.path.isfile(path), f"The output file {path} was not created."

def test_restored_graph_accuracy():
    output_path = "/home/user/restored_graph.jsonl"
    verifier_path = "/app/verify_accuracy.py"

    assert os.path.isfile(output_path), f"Output file missing: {output_path}"
    assert os.path.isfile(verifier_path), f"Verifier script missing: {verifier_path}"

    try:
        result = subprocess.run(
            ["python3", verifier_path, output_path],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Verifier script failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    output_str = result.stdout.strip()
    try:
        # The script is expected to print a single float to stdout
        accuracy = float(output_str.split()[-1])
    except ValueError:
        pytest.fail(f"Could not parse verifier output as float. Output was: {output_str}")

    threshold = 0.98
    assert accuracy >= threshold, f"Accuracy {accuracy} is below the required threshold of {threshold}."