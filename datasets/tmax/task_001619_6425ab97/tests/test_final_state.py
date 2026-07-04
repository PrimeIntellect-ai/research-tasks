# test_final_state.py

import os
import json
import ast
import pytest

def test_metrics_json_exists_and_schema():
    """Verify metrics.json exists and has the correct schema."""
    metrics_path = "/home/user/ml_project/metrics.json"
    assert os.path.isfile(metrics_path), f"Expected metrics file at {metrics_path} does not exist."

    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_path} is not valid JSON.")

    assert "train_mse" in metrics, "metrics.json is missing 'train_mse' key."
    assert "test_mse" in metrics, "metrics.json is missing 'test_mse' key."

    assert isinstance(metrics["train_mse"], (int, float)), "'train_mse' must be a number."
    assert isinstance(metrics["test_mse"], (int, float)), "'test_mse' must be a number."

def test_pipeline_no_leakage_ast():
    """Parse pipeline.py to ensure train_test_split is called before custom_pca."""
    pipeline_path = "/home/user/ml_project/pipeline.py"
    assert os.path.isfile(pipeline_path), f"Expected pipeline script at {pipeline_path} does not exist."

    with open(pipeline_path, "r") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {pipeline_path}: {e}")

    class CallVisitor(ast.NodeVisitor):
        def __init__(self):
            self.calls = []

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                self.calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                self.calls.append(node.func.attr)
            self.generic_visit(node)

    visitor = CallVisitor()
    visitor.visit(tree)

    calls = visitor.calls

    assert "train_test_split" in calls, "train_test_split is not called in pipeline.py."
    assert "custom_pca" in calls, "custom_pca is not called in pipeline.py."

    # Check that train_test_split occurs before custom_pca in the source file
    # We can do a simple string index check on the source code to be robust against different AST structures
    split_idx = source.find("train_test_split")
    pca_idx = source.find("custom_pca", split_idx) # look for custom_pca after train_test_split

    # It's possible custom_pca is defined before, so we check the usage in the main block or after split
    # Let's check the lines in the file
    lines = source.splitlines()
    split_line = -1
    pca_usage_line = -1

    for i, line in enumerate(lines):
        if "train_test_split(" in line:
            split_line = i
        if "custom_pca(" in line and "def custom_pca" not in line:
            pca_usage_line = i

    if split_line != -1 and pca_usage_line != -1:
        assert split_line < pca_usage_line, "Data leakage: custom_pca is called before train_test_split."

def test_metrics_values_changed_from_leaked():
    """Ensure the metrics are different from the leaked version, implying a fix."""
    metrics_path = "/home/user/ml_project/metrics.json"
    if not os.path.isfile(metrics_path):
        pytest.fail("metrics.json not found.")

    with open(metrics_path, "r") as f:
        metrics = json.load(f)

    # The leaked version has a specific signature of MSE (usually lower test MSE due to leakage)
    # Since we can't use sklearn to compute exact truth, we verify the metrics are reasonable floats
    train_mse = metrics["train_mse"]
    test_mse = metrics["test_mse"]

    assert train_mse > 0, "train_mse should be strictly positive."
    assert test_mse > 0, "test_mse should be strictly positive."

    # Test MSE is typically higher than Train MSE in this setup without leakage
    # The exact expected test_mse without leakage is around 5000+ depending on the data
    assert test_mse > 100, f"test_mse ({test_mse}) seems suspiciously low, possible data leakage remaining."