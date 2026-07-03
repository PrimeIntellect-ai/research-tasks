# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_aggregate_sh_correct_output():
    """Verify that aggregate.sh produces the correct output for the original metrics file."""
    script_path = "/home/user/aggregate.sh"
    metrics_path = "/home/user/data/metrics.txt"

    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    result = subprocess.run([script_path, metrics_path], capture_output=True, text=True)
    assert result.returncode == 0, f"aggregate.sh failed with exit code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    assert output == "Total: 295", f"Expected 'Total: 295', but got '{output}'"

def test_aggregate_sh_handles_edge_cases():
    """Verify that aggregate.sh handles empty values, NaN, and spaces correctly using a custom file."""
    script_path = "/home/user/aggregate.sh"

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        tmp.write("a= 10 \n")
        tmp.write("b=\n")
        tmp.write("c=NaN\n")
        tmp.write("d=  20\n")
        tmp.write("e=invalid\n")
        tmp_path = tmp.name

    try:
        result = subprocess.run([script_path, tmp_path], capture_output=True, text=True)
        assert result.returncode == 0, f"aggregate.sh failed on edge cases. Stderr: {result.stderr}"

        output = result.stdout.strip()
        assert output == "Total: 30", f"Expected 'Total: 30' for edge cases, but got '{output}'"
    finally:
        os.remove(tmp_path)

def test_regression_test_script():
    """Verify that test_aggregate.sh exists, is executable, and passes."""
    test_script_path = "/home/user/test_aggregate.sh"

    assert os.path.isfile(test_script_path), f"{test_script_path} does not exist."
    assert os.access(test_script_path, os.X_OK), f"{test_script_path} is not executable."

    result = subprocess.run([test_script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{test_script_path} failed with exit code {result.returncode}. Stderr: {result.stderr}\nStdout: {result.stdout}"