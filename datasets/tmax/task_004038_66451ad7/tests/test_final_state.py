# test_final_state.py

import os
import json
import pytest

def test_evaluation_result_accuracy():
    result_file = '/home/user/evaluation_result.json'
    assert os.path.isfile(result_file), f"Evaluation result file {result_file} is missing. Did you run /app/evaluate.py?"

    with open(result_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_file} is not valid JSON.")

    assert "accuracy" in data, f"Key 'accuracy' is missing in {result_file}."

    accuracy = data["accuracy"]
    assert isinstance(accuracy, (int, float)), f"Accuracy must be a number, got {type(accuracy)}."

    threshold = 0.99
    assert accuracy >= threshold, f"Accuracy is {accuracy}, which is below the required threshold of {threshold}."

def test_math_core_compiled():
    so_file = '/app/ext/math_core.so'
    assert os.path.isfile(so_file), f"Compiled extension {so_file} is missing. Did you fix the Makefile and run make?"