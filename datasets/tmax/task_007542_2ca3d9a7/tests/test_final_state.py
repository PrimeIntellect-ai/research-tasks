# test_final_state.py
import os
import json
import subprocess
import pytest

RESULTS_FILE = "/home/user/research/results.json"
DATA_FILE = "/home/user/research/data.csv"

def get_truth_values():
    """
    Computes the truth values using the environment's installed libraries 
    (pandas, scikit-learn) via a subprocess, since the test itself must 
    only use the standard library.
    """
    script = """
import pandas as pd
import json
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, KFold

df = pd.read_csv("/home/user/research/data.csv")
X = df.drop("target", axis=1)
y = df["target"]

pipeline = Pipeline([
    ('imputer', SimpleImputer()),
    ('scaler', StandardScaler()),
    ('model', Ridge(random_state=42))
])

param_grid = {
    'imputer__strategy': ['mean', 'median'],
    'model__alpha': [0.1, 1.0, 10.0, 100.0]
}

cv = KFold(n_splits=5, shuffle=True, random_state=42)
grid_search = GridSearchCV(pipeline, param_grid, cv=cv)
grid_search.fit(X, y)

results = {
    "best_alpha": grid_search.best_params_['model__alpha'],
    "best_imputer_strategy": grid_search.best_params_['imputer__strategy'],
    "best_cv_score": round(float(grid_search.best_score_), 4)
}

print(json.dumps(results))
"""
    result = subprocess.run(
        ["python3", "-c", script],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout.strip())

def test_results_file_exists():
    assert os.path.isfile(RESULTS_FILE), f"The file {RESULTS_FILE} does not exist."

def test_results_content():
    assert os.path.isfile(RESULTS_FILE), f"The file {RESULTS_FILE} does not exist."

    with open(RESULTS_FILE, "r") as f:
        try:
            student_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RESULTS_FILE} does not contain valid JSON.")

    expected_keys = {"best_alpha", "best_imputer_strategy", "best_cv_score"}
    missing_keys = expected_keys - set(student_results.keys())
    assert not missing_keys, f"The results.json is missing keys: {missing_keys}"

    truth = get_truth_values()

    assert student_results["best_alpha"] == truth["best_alpha"], \
        f"Expected best_alpha to be {truth['best_alpha']}, got {student_results['best_alpha']}"

    assert student_results["best_imputer_strategy"] == truth["best_imputer_strategy"], \
        f"Expected best_imputer_strategy to be '{truth['best_imputer_strategy']}', got '{student_results['best_imputer_strategy']}'"

    assert isinstance(student_results["best_cv_score"], float), \
        "best_cv_score must be a float."

    assert round(student_results["best_cv_score"], 4) == truth["best_cv_score"], \
        f"Expected best_cv_score to be {truth['best_cv_score']}, got {student_results['best_cv_score']}"