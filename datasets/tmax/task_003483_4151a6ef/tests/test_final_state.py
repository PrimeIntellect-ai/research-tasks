# test_final_state.py

import os
import re
import pytest

def test_evaluate_script():
    path = "/home/user/evaluate.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    with open(path, "r") as f:
        content = f.read()
    assert "artifact_info.env" in content, f"{path} must source artifact_info.env"

def test_benchmark_script():
    path = "/home/user/benchmark.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    with open(path, "r") as f:
        content = f.read()
    assert "evaluate.sh" in content, f"{path} must call evaluate.sh"
    assert "expressions.txt" in content, f"{path} must read expressions.txt"

def test_evaluator_proto():
    path = "/home/user/evaluator.proto"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert re.search(r'syntax\s*=\s*"proto3"\s*;', content), "Missing or incorrect syntax declaration in proto file."
    assert re.search(r'service\s+ArtifactEvaluator\s*\{', content), "Missing service ArtifactEvaluator in proto file."
    assert re.search(r'rpc\s+Evaluate\s*\(\s*EvaluationRequest\s*\)\s*returns\s*\(\s*EvaluationResponse\s*\)', content), "Missing or incorrect rpc Evaluate in proto file."
    assert re.search(r'message\s+EvaluationRequest\s*\{', content), "Missing message EvaluationRequest in proto file."
    assert re.search(r'string\s+expression\s*=', content), "Missing string expression field in EvaluationRequest."
    assert re.search(r'message\s+EvaluationResponse\s*\{', content), "Missing message EvaluationResponse in proto file."
    assert re.search(r'int32\s+result\s*=', content), "Missing int32 result field in EvaluationResponse."

def test_evaluation_results_log():
    path = "/home/user/evaluation_results.log"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run benchmark.sh?"

    with open(path, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "MAJOR + 2 = 5",
        "MINOR * PATCH = 8",
        "(MAJOR + MINOR) * 2 = 14",
        "BUILD_NUMBER - (MAJOR * 10) = 75"
    ]

    for expected in expected_lines:
        assert any(expected in line for line in content), f"Expected result '{expected}' not found in {path}"