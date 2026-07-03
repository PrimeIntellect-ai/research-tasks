# test_final_state.py
import os
import subprocess

def test_find_stable_script_exists_and_executable():
    script_path = "/home/user/find_stable.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_find_stable_script_execution_and_output():
    script_path = "/home/user/find_stable.sh"
    results_path = "/home/user/results/stability.csv"

    # Remove the results file if it exists to ensure the script creates it
    if os.path.exists(results_path):
        os.remove(results_path)

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    # Check if the output file was created
    assert os.path.isfile(results_path), f"Expected output file {results_path} was not created."

    # Verify the contents of the CSV
    expected_lines = [
        "protein_A,0.02",
        "protein_B,0.01",
        "protein_C,0.1",
        "protein_D,0.005"
    ]

    with open(results_path, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.split("\n") if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in CSV, found {len(actual_lines)}."

    for expected in expected_lines:
        assert expected in actual_lines, f"Expected row '{expected}' not found in {results_path}."