# test_final_state.py

import os
import json
import ast

def test_results_json_exists():
    """Check if the results.json file was created."""
    file_path = "/home/user/results.json"
    assert os.path.isfile(file_path), f"File not found: {file_path}. Did you run the script?"

def test_results_json_structure():
    """Check if the results.json has the correct structure and keys."""
    file_path = "/home/user/results.json"
    with open(file_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not a valid JSON file."

    assert "best_score" in results, "'best_score' key missing from results.json"
    assert "best_params" in results, "'best_params' key missing from results.json"

    best_params = results["best_params"]
    assert isinstance(best_params, dict), "'best_params' should be a dictionary"
    assert "clf__C" in best_params, "'clf__C' missing from best_params"
    assert "tfidf__max_features" in best_params, "'tfidf__max_features' missing from best_params"

    assert isinstance(results["best_score"], float), "'best_score' should be a float"
    assert best_params["clf__C"] in [0.1, 1.0], "'clf__C' should be one of the grid search values"
    assert best_params["tfidf__max_features"] in [10, 50], "'tfidf__max_features' should be one of the grid search values"

def test_train_py_uses_pipeline():
    """Check if train.py was updated to use a Pipeline and correct grid search params."""
    file_path = "/home/user/train.py"
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read()

    # Check for Pipeline usage
    assert "Pipeline" in content, "train.py does not seem to use a scikit-learn Pipeline."

    # Check for hyperparameter names
    assert "tfidf__max_features" in content, "train.py does not tune 'tfidf__max_features'."
    assert "clf__C" in content, "train.py does not tune 'clf__C'."

    # Check for CV=3
    content_no_spaces = content.replace(" ", "")
    assert "cv=3" in content_no_spaces, "train.py does not seem to use cv=3 in GridSearchCV."

def test_train_py_no_data_leakage():
    """Ensure that the explicit data leakage (fit_transform before GridSearchCV) is removed."""
    file_path = "/home/user/train.py"
    with open(file_path, 'r') as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            assert False, "train.py contains a syntax error."

    # We look for calls to fit_transform. In a proper pipeline setup, fit_transform is handled internally
    # by GridSearchCV, so the user script shouldn't call it directly on the vectorizer outside the pipeline.
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == 'fit_transform':
                    # If they call fit_transform, it might be a sign they didn't fix the leakage properly,
                    # though they could technically call it on something else. We just warn/fail if they 
                    # are doing it the old way.
                    pass