# test_final_state.py

import os
import pytest

def test_script_exists():
    script_path = "/home/user/optimize_k.sh"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

def test_model_params_output():
    output_path = "/home/user/model_params.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} is missing."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_result = "k=0.42"
    assert content == expected_result, f"Expected {output_path} to contain '{expected_result}', but found '{content}'."