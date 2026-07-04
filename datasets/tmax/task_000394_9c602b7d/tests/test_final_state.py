# test_final_state.py
import os
import json
import ast

def test_metrics_json_exists_and_valid():
    metrics_file = '/home/user/metrics.json'
    assert os.path.exists(metrics_file), f"Missing file: {metrics_file}"

    with open(metrics_file, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{metrics_file} is not a valid JSON file."

    assert "test_accuracy" in metrics, "Missing 'test_accuracy' key in metrics.json"
    assert "first_5_predictions" in metrics, "Missing 'first_5_predictions' key in metrics.json"

    assert isinstance(metrics["test_accuracy"], float), "'test_accuracy' must be a float"
    assert isinstance(metrics["first_5_predictions"], list), "'first_5_predictions' must be a list"
    assert len(metrics["first_5_predictions"]) == 5, "'first_5_predictions' must contain exactly 5 elements"
    assert all(isinstance(x, int) for x in metrics["first_5_predictions"]), "All predictions must be integers"

def test_pipeline_script_fixed():
    pipeline_file = '/home/user/etl_pipeline.py'
    assert os.path.exists(pipeline_file), f"Missing file: {pipeline_file}"

    with open(pipeline_file, 'r') as f:
        content = f.read()

    # Check that train_test_split is used
    assert "train_test_split" in content, "train_test_split is missing from the script"

    # Very basic static analysis to ensure train_test_split appears before fit_transform
    # to verify the data leakage was fixed.
    try:
        tree = ast.parse(content)
    except SyntaxError:
        assert False, f"Syntax error in {pipeline_file}"

    # Find line numbers for train_test_split and TfidfVectorizer/PCA fit_transform
    split_lineno = None
    tfidf_fit_lineno = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == 'train_test_split':
                split_lineno = node.lineno
            elif isinstance(node.func, ast.Attribute) and node.func.attr == 'fit_transform':
                if tfidf_fit_lineno is None:
                    tfidf_fit_lineno = node.lineno

    if split_lineno and tfidf_fit_lineno:
        assert split_lineno < tfidf_fit_lineno, "train_test_split must be called before fit_transform to avoid data leakage"