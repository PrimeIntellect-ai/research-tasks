# test_final_state.py
import os
import subprocess
import pytest

def test_pipeline_sh_exists_and_executable():
    path = '/home/user/pipeline.sh'
    assert os.path.isfile(path), f"File not found: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_venv_exists():
    path = '/home/user/venv'
    assert os.path.isdir(path), f"Virtual environment not found at {path}"
    assert os.path.isfile(os.path.join(path, 'bin', 'python')), "Python executable not found in venv"

def test_output_txt():
    output_path = '/home/user/output.txt'
    assert os.path.isfile(output_path), f"Output file not found: {output_path}"

    with open(output_path, 'r') as f:
        student_val = f.read().strip()

    # Compute expected value using the student's venv
    script = """
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import BayesianRidge

df = pd.read_csv('/home/user/data.csv')
df_boot = df.sample(n=1000, replace=True, random_state=42)

pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(df_boot[['x1', 'x2', 'x3', 'x4']])

model = BayesianRidge()
model.fit(X_pca, df_boot['y'])

print(f"{model.alpha_:.4f}")
"""
    venv_python = '/home/user/venv/bin/python'
    try:
        result = subprocess.run([venv_python, '-c', script], capture_output=True, text=True, check=True)
        expected_val = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected value using venv. Ensure pandas and scikit-learn are installed in the venv. Error: {e.stderr}")

    assert student_val == expected_val, f"Expected output {expected_val}, but got {student_val}"