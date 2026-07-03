# test_final_state.py
import math
import requests
import pytest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from scipy import stats

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer EXP-9942-X"}
BAD_AUTH_HEADER = {"Authorization": "Bearer WRONG-TOKEN"}

def test_metadata_endpoint_correct_auth():
    try:
        resp = requests.get(f"{BASE_URL}/metadata", headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the API on 127.0.0.1:8080")

    assert resp.status_code == 200, f"Expected 200 OK for /metadata, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response from /metadata was not valid JSON. Response: {resp.text}")

    assert "seed" in data, "Missing 'seed' in metadata response"
    assert "alpha" in data, "Missing 'alpha' in metadata response"
    assert "baseline" in data, "Missing 'baseline' in metadata response"

    assert int(data["seed"]) == 1042, f"Expected seed 1042, got {data['seed']}"
    assert math.isclose(float(data["alpha"]), 0.05, rel_tol=1e-5), f"Expected alpha 0.05, got {data['alpha']}"
    assert math.isclose(float(data["baseline"]), 0.65, rel_tol=1e-5), f"Expected baseline 0.65, got {data['baseline']}"

def test_reproducibility_endpoint_correct_auth():
    try:
        resp = requests.get(f"{BASE_URL}/test-reproducibility", headers=AUTH_HEADER, timeout=15)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the API on 127.0.0.1:8080")

    assert resp.status_code == 200, f"Expected 200 OK for /test-reproducibility, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response from /test-reproducibility was not valid JSON. Response: {resp.text}")

    assert "mean_accuracy" in data, "Missing 'mean_accuracy' in response"
    assert "p_value" in data, "Missing 'p_value' in response"
    assert "reproducible" in data, "Missing 'reproducible' in response"

    # Compute expected values
    df = pd.read_csv('/app/dataset.csv')
    df = df.dropna()
    df = df[df['target'].isin([0, 1])]

    X = df.drop(columns=['target'])
    y = df['target']

    clf = RandomForestClassifier(random_state=1042)
    scores = cross_val_score(clf, X, y, cv=10)
    mean_acc = scores.mean()

    t_stat, p_val_2sided = stats.ttest_1samp(scores, 0.65)
    if t_stat > 0:
        p_val = p_val_2sided / 2
    else:
        p_val = 1 - (p_val_2sided / 2)

    reproducible = bool(p_val < 0.05 and mean_acc > 0.65)

    assert math.isclose(float(data["mean_accuracy"]), mean_acc, rel_tol=1e-3), f"Expected mean_accuracy ~{mean_acc}, got {data['mean_accuracy']}"
    assert math.isclose(float(data["p_value"]), p_val, rel_tol=1e-3), f"Expected p_value ~{p_val}, got {data['p_value']}"
    assert bool(data["reproducible"]) == reproducible, f"Expected reproducible={reproducible}, got {data['reproducible']}"

def test_auth_failure():
    try:
        resp = requests.get(f"{BASE_URL}/metadata", headers=BAD_AUTH_HEADER, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the API on 127.0.0.1:8080")

    assert resp.status_code == 401, f"Expected 401 Unauthorized for /metadata with wrong token, got {resp.status_code}"

    resp2 = requests.get(f"{BASE_URL}/test-reproducibility", headers=BAD_AUTH_HEADER, timeout=15)
    assert resp2.status_code == 401, f"Expected 401 Unauthorized for /test-reproducibility with wrong token, got {resp2.status_code}"

    resp3 = requests.get(f"{BASE_URL}/metadata", timeout=5)
    assert resp3.status_code == 401, f"Expected 401 Unauthorized for /metadata with missing token, got {resp3.status_code}"