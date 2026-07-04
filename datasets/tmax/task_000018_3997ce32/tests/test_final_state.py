# test_final_state.py

import os

def test_script_exists_and_executable():
    """Check if the evaluation script exists and is executable."""
    script_path = "/home/user/evaluate_order.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_result_file_content():
    """Check if the result file contains the correct absolute difference."""
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"The result file {result_path} does not exist. Did you run your script?"

    with open(result_path, "r") as f:
        content = f.read().strip()

    try:
        difference = float(content)
    except ValueError:
        assert False, f"The content of {result_path} is not a valid floating-point number. Got: {content}"

    # The expected difference based on the provided signal.txt is exactly 3.0
    expected_difference = 3.0
    assert abs(difference - expected_difference) < 1e-6, (
        f"Expected the absolute difference to be {expected_difference}, "
        f"but got {difference}."
    )