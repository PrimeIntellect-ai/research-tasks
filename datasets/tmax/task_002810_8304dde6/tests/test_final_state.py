# test_final_state.py
import os
import pytest

def test_diffusion_result():
    result_path = "/home/user/diffusion_result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist. The script did not produce the expected output file."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        pred_d = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {result_path} as a float. Content: '{content}'")

    truth_d = 0.015
    tolerance = 0.002

    assert abs(pred_d - truth_d) <= tolerance, (
        f"Predicted diffusion coefficient D={pred_d} is outside the acceptable "
        f"tolerance {tolerance} of the ground truth {truth_d}."
    )