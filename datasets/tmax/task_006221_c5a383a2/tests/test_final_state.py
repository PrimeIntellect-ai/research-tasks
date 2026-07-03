# test_final_state.py
import os
import subprocess
import re

def test_go_tests_pass():
    """Ensure that the go tests pass consistently (fixing both the build error and the intermittent assertion)."""
    work_dir = "/home/user/oncall/vwap"
    assert os.path.isdir(work_dir), f"Directory {work_dir} does not exist."

    result = subprocess.run(
        ["go", "test", "-count=50"],
        cwd=work_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"go test failed. Output:\n{result.stdout}\n{result.stderr}"

def test_function_signature_unchanged():
    """Ensure the exported function signature remains exactly the same."""
    vwap_file = "/home/user/oncall/vwap/vwap.go"
    assert os.path.isfile(vwap_file), f"{vwap_file} is missing."

    with open(vwap_file, "r") as f:
        content = f.read()

    expected_signature = r"func ComputeVWAP\(\s*prices\s+\[\]float32\s*,\s*volumes\s+\[\]float32\s*\)\s+float32"
    assert re.search(expected_signature, content), "The signature of ComputeVWAP was changed or not found."

def test_result_file_correct():
    """Validate that the result.txt file contains the correctly computed VWAP."""
    result_file = "/home/user/result.txt"
    assert os.path.isfile(result_file), f"{result_file} is missing."

    # Compute expected result in Python to avoid hardcoding literal truth
    prices = [10000000.0, 100.0, 105.0]
    volumes = [1.0, 500000.0, 600000.0]

    numerator = sum(p * v for p, v in zip(prices, volumes))
    denominator = sum(volumes)
    expected_vwap = numerator / denominator
    expected_str = f"{expected_vwap:.4f}"

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert expected_str in content, f"Expected to find '{expected_str}' in {result_file}, but found '{content}'"