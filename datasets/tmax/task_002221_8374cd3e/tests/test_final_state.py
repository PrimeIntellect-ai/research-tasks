# test_final_state.py

import os
import subprocess

def test_biomodel_c_fixed():
    path = "/home/user/biomodel.c"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "0.001" in content, "The integration time step dt was not changed to 0.001 in biomodel.c."

def test_pipeline_sh_exists_and_works():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

    # Run the pipeline script with the test inputs from the prompt
    target = "ACGTACGTACGT"
    primer = "ACGT"

    result = subprocess.run(["bash", path, target, primer], capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.sh failed with error: {result.stderr}"

    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist."

    with open(result_path, 'r') as f:
        result_content = f.read().strip()

    assert result_content == "-0.0195", f"Expected result.txt to contain exactly '-0.0195', but got '{result_content}'"

def test_pipeline_is_dynamic():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

    # Run with different inputs to ensure the solution is not hardcoded
    target = "AAAA"
    primer = "A"

    # Calculate expected value for occurrences = 4, k = 8.0
    x = 1.0
    y = 0.0
    dt = 0.001
    k = 8.0
    for _ in range(10000):
        dx = y
        dy = -k * x - 0.5 * y
        x += dx * dt
        y += dy * dt
    expected_output = f"{x:.4f}"

    subprocess.run(["bash", path, target, primer], capture_output=True, text=True)

    result_path = "/home/user/result.txt"
    with open(result_path, 'r') as f:
        result_content = f.read().strip()

    assert result_content == expected_output, f"Expected result.txt to contain '{expected_output}' for inputs {target} {primer}, but got '{result_content}'. The script might be hardcoded."