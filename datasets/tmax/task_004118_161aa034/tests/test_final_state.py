# test_final_state.py

import os
import re
import math
import pytest

def test_predictions_csv_exists_and_correct():
    file_path = "/home/user/predictions.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The C++ program failed to create it."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 4, f"File {file_path} does not contain the expected number of rows (header + 3 data rows)."

    assert lines[0] == "id,pred", f"Header in {file_path} is incorrect. Expected 'id,pred', got '{lines[0]}'."

    # Expected predictions based on the math
    expected_preds = {
        "1": "0.5025",
        "2": "0.5987",
        "3": "0.5000"
    }

    for line in lines[1:]:
        parts = line.split(",")
        assert len(parts) == 2, f"Invalid format in line '{line}' of {file_path}. Expected 'id,pred'."
        uid, pred = parts[0], parts[1]
        assert uid in expected_preds, f"Unexpected id '{uid}' found in {file_path}."
        assert pred == expected_preds[uid], f"Incorrect prediction for id {uid}. Expected {expected_preds[uid]}, got {pred}."

def test_benchmark_txt_exists_and_correct():
    file_path = "/home/user/benchmark.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The C++ program failed to create it."

    with open(file_path, "r") as f:
        content = f.read().strip()

    pattern = r"^Total inference time: \d+ us$"
    assert re.match(pattern, content), f"File {file_path} content '{content}' does not match expected format 'Total inference time: [X] us'."

def test_run_pipeline_script_exists_and_optimized():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "-O3" in content, f"Script {script_path} does not seem to compile with '-O3' optimization flag."

def test_cpp_source_exists():
    cpp_path = "/home/user/etl_inference.cpp"
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} does not exist."