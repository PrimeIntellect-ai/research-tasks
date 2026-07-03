# test_final_state.py
import os
import math

def test_resolution_content():
    resolution_path = "/home/user/resolution.txt"
    assert os.path.isfile(resolution_path), f"File {resolution_path} does not exist. Did you create it?"

    with open(resolution_path, 'r') as f:
        content = f.read().strip()

    assert content, f"File {resolution_path} is empty."

    try:
        value = float(content)
    except ValueError:
        assert False, f"Content of {resolution_path} is not a valid float: '{content}'"

    # The duration is 45 ms, which is 0.045 seconds.
    # The C program computes 1000.0 / duration.
    expected_value = 1000.0 / 0.045

    assert math.isclose(value, expected_value, rel_tol=1e-4), f"Value in {resolution_path} ({value}) does not match the expected calculated metric."

def test_output_txt_content():
    output_path = "/home/user/pipeline/output.txt"
    assert os.path.isfile(output_path), f"File {output_path} does not exist. Did you successfully run the fixed pipeline script?"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content, f"File {output_path} is empty."

    try:
        value = float(content)
    except ValueError:
        assert False, f"Content of {output_path} is not a valid float: '{content}'"

    expected_value = 1000.0 / 0.045
    assert math.isclose(value, expected_value, rel_tol=1e-4), f"Value in {output_path} ({value}) does not match the expected calculated metric."