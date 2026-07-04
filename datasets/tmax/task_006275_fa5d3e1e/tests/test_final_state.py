# test_final_state.py
import os
import json
import subprocess
import math

def test_run_sh_exists_and_executable():
    """Check if run.sh exists and is executable."""
    path = '/home/user/run.sh'
    assert os.path.exists(path), f"{path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_results_json_exists_and_keys():
    """Check if results.json exists and contains the required keys."""
    path = '/home/user/results.json'
    assert os.path.exists(path), f"{path} does not exist."
    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{path} does not contain valid JSON."

    assert "accuracy" in data, "results.json is missing 'accuracy' key."
    assert "p_value" in data, "results.json is missing 'p_value' key."
    assert isinstance(data["accuracy"], (float, int)), "accuracy must be a number."
    assert isinstance(data["p_value"], (float, int)), "p_value must be a number."

def test_correct_metrics():
    """Recompute the expected metrics using the student's virtual environment and compare."""
    venv_python = '/home/user/venv/bin/python'
    assert os.path.exists(venv_python), f"Virtual environment python not found at {venv_python}. Did run.sh create it?"

    # Script to compute the exact expected values using the correct methodology
    script = """
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from scipy.stats import ttest_ind
import json

df = pd.read_csv('/home/user/telemetry.csv')
X = df.drop('label', axis=1)
y = df['label']

# 1. Train-test split first (fixes data leakage)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Fit scaler on train, transform train and test
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. Fit PCA on train, transform train and test
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

# 4. Train Logistic Regression and get accuracy
clf = LogisticRegression(random_state=42)
clf.fit(X_train_pca, y_train)
acc = float(clf.score(X_test_pca, y_test))

# 5. Extract PC1 for test set and perform t-test
pc1_test = X_test_pca[:, 0]
pc1_0 = pc1_test[y_test == 0]
pc1_1 = pc1_test[y_test == 1]
t_stat, p_value = ttest_ind(pc1_0, pc1_1)

print(json.dumps({"accuracy": acc, "p_value": float(p_value)}))
"""
    result = subprocess.run([venv_python, '-c', script], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to compute expected metrics using {venv_python}:\n{result.stderr}"

    try:
        expected_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, f"Failed to parse expected metrics output:\n{result.stdout}"

    with open('/home/user/results.json', 'r') as f:
        student_data = json.load(f)

    assert math.isclose(student_data["accuracy"], expected_data["accuracy"], rel_tol=1e-3), \
        f"Expected accuracy ~{expected_data['accuracy']:.4f}, but got {student_data['accuracy']}. Check data leakage fix."

    assert math.isclose(student_data["p_value"], expected_data["p_value"], rel_tol=1e-3), \
        f"Expected p_value ~{expected_data['p_value']:.4e}, but got {student_data['p_value']}. Check the hypothesis testing logic."