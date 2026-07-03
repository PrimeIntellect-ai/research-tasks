# test_final_state.py

import os
import json
import urllib.request
import subprocess
import pytest

def test_phase1_cleaned_data():
    """Verify that cleaned_data.csv exists and matches the expected deduplication logic."""
    cleaned_path = "/home/user/cleaned_data.csv"
    assert os.path.exists(cleaned_path), f"{cleaned_path} does not exist."

    # We use a subprocess to run the golden logic to avoid importing third-party libs directly in the pytest process,
    # relying on the fact that the user must have installed pandas and scikit-learn in the environment.
    golden_script = """
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    df = pd.read_csv('/home/user/raw_data.csv')
    vec = TfidfVectorizer(stop_words='english')
    X = vec.fit_transform(df['text'])

    kept_indices = []
    for i in range(len(df)):
        if not kept_indices:
            kept_indices.append(i)
            continue
        sims = cosine_similarity(X[i], X[kept_indices])
        if sims.max() < 0.80:
            kept_indices.append(i)

    golden_df = df.iloc[kept_indices].reset_index(drop=True)
    golden_df.to_csv('/tmp/golden_cleaned.csv', index=False)
except Exception as e:
    print(f"Error computing golden data: {e}")
"""
    try:
        subprocess.run(["python3", "-c", golden_script], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute golden dataset (are pandas and scikit-learn installed?). Error: {e.stderr}")

    assert os.path.exists("/tmp/golden_cleaned.csv"), "Golden dataset was not created."

    with open(cleaned_path, "r", encoding="utf-8") as f:
        user_data = f.read().strip()
    with open("/tmp/golden_cleaned.csv", "r", encoding="utf-8") as f:
        golden_data = f.read().strip()

    assert user_data == golden_data, "The contents of cleaned_data.csv do not match the expected deduplicated output based on the TF-IDF cosine similarity logic."

def test_phase2_model_and_param():
    """Verify that the best parameter and model are saved correctly."""
    param_path = "/home/user/best_param.txt"
    model_path = "/home/user/model.joblib"

    assert os.path.exists(param_path), f"{param_path} does not exist."
    assert os.path.exists(model_path), f"{model_path} does not exist."

    with open(param_path, "r", encoding="utf-8") as f:
        param_val = f.read().strip()

    # The best parameter should be one of the tested grid values.
    assert param_val in ["0.1", "1.0", "10.0"], f"best_param.txt contains an unexpected value: '{param_val}'. Expected one of 0.1, 1.0, 10.0."

def test_phase3_api_and_benchmark():
    """Verify that the API is running, returns correct JSON structure, and benchmark results exist."""
    app_path = "/home/user/app.py"
    bench_script_path = "/home/user/benchmark.sh"
    bench_res_path = "/home/user/benchmark_results.txt"

    assert os.path.exists(app_path), f"{app_path} does not exist."
    assert os.path.exists(bench_script_path), f"{bench_script_path} does not exist."
    assert os.path.exists(bench_res_path), f"{bench_res_path} does not exist."

    with open(bench_res_path, "r", encoding="utf-8") as f:
        res = f.read().strip()

    try:
        val = float(res)
        assert val > 0, "Benchmark time must be greater than 0."
    except ValueError:
        pytest.fail(f"benchmark_results.txt does not contain a valid numeric time. Found: '{res}'")

    # Test the Flask API endpoint
    req = urllib.request.Request(
        "http://localhost:5000/predict",
        data=json.dumps({"text": "Is this a valid test message?"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"API returned status code {response.status}"
            data = json.loads(response.read().decode("utf-8"))
            assert "prediction" in data, "API response JSON does not contain the 'prediction' key."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the API on port 5000. Is the Flask server running? Error: {e}")
    except json.JSONDecodeError:
        pytest.fail("API did not return valid JSON.")