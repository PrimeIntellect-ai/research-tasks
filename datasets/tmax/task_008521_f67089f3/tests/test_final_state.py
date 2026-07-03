# test_final_state.py

import os
import sys
import json
import subprocess
import pytest

def test_test_pipeline_exists_and_passes():
    path = '/home/user/test_pipeline.py'
    assert os.path.isfile(path), f"Expected test file at {path} is missing."

    # Run pytest on the file
    result = subprocess.run([sys.executable, "-m", "pytest", path], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest failed on {path}:\n{result.stdout}\n{result.stderr}"

    with open(path, 'r') as f:
        content = f.read()
    assert "def test_no_float_cast" in content, "test_no_float_cast function is missing from test_pipeline.py"

def test_experiment_results_json():
    path = '/home/user/experiment_results.json'
    assert os.path.isfile(path), f"Expected results file at {path} is missing."

    with open(path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("experiment_results.json is not a valid JSON file.")

    assert "best_params" in results, "Key 'best_params' missing from experiment_results.json"
    assert "learning_rate" in results["best_params"], "Key 'learning_rate' missing from best_params"
    assert "max_iter" in results["best_params"], "Key 'max_iter' missing from best_params"
    assert "best_score" in results, "Key 'best_score' missing from experiment_results.json"
    assert isinstance(results["best_score"], float), "best_score must be a float"
    assert 0.0 <= results["best_score"] <= 1.0, "best_score must be between 0.0 and 1.0"

def test_clean_data_logic():
    sys.path.insert(0, '/home/user')
    try:
        from pipeline import load_data, clean_data
    except ImportError as e:
        pytest.fail(f"Could not import load_data or clean_data from pipeline.py: {e}")

    df = load_data()
    df_clean = clean_data(df)
    assert str(df_clean['user_id'].dtype) == 'Int64', f"Expected Int64 dtype for user_id, got {df_clean['user_id'].dtype}"

    # Check that missing values are correctly handled
    missing_mask = df_clean['user_id'].isna()
    expected_missing = df_clean['feature_1'] < -1.0
    assert (missing_mask == expected_missing).all(), "Missing values in user_id do not match the expected condition (feature_1 < -1.0)."

def test_pipeline_train_and_evaluate_logic():
    path = '/home/user/pipeline.py'
    with open(path, 'r') as f:
        content = f.read()

    assert "GridSearchCV" in content, "GridSearchCV is missing from pipeline.py"
    assert "cv=3" in content.replace(" ", ""), "cv=3 is missing from GridSearchCV call"
    assert "random_state=42" in content, "random_state=42 is missing"
    assert "HistGradientBoostingClassifier" in content, "HistGradientBoostingClassifier is missing"