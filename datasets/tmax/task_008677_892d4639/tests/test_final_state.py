# test_final_state.py

import os
import pytest

def test_evaluate_script_exists_and_executable():
    script_path = "/home/user/evaluate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_best_model_output():
    output_path = "/home/user/best_model.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_content = "model_alpha,0.8846"
    assert content == expected_content, f"Expected output '{expected_content}', but got '{content}'"