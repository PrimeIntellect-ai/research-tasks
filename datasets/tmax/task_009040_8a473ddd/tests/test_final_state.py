# test_final_state.py

import os
import json
import pytest

def test_optimized_weights_file_exists():
    file_path = "/home/user/ops_triage/optimized_weights.json"
    assert os.path.isfile(file_path), f"The output file {file_path} was not found. Did you run the pipeline successfully?"

def test_optimized_weights_content_correct():
    file_path = "/home/user/ops_triage/optimized_weights.json"
    assert os.path.isfile(file_path), f"The output file {file_path} is missing."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    assert "optimal_x" in data, "The JSON output is missing the 'optimal_x' key."
    assert data["optimal_x"] == -2.0, f"Expected optimal_x to be -2.0, but got {data['optimal_x']}."

def test_model_optimizer_bug_fixed():
    file_path = "/home/user/ops_triage/model_optimizer.py"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    assert "x += grad * learning_rate" not in content, "The logical bug in model_optimizer.py (adding the gradient) is still present."
    assert "x -= grad * learning_rate" in content or "x = x - grad * learning_rate" in content, "The update rule in model_optimizer.py was not correctly fixed to subtract the gradient."