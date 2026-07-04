# test_final_state.py
import pytest
import requests
import numpy as np
import torch
import torch.nn as nn
from scipy import stats

BASE_URL = "http://127.0.0.1:8000"

def get_expected_data():
    np.random.seed(42)
    feat_0_19 = np.random.rand(1000, 20)
    feat_20 = np.random.normal(loc=3.5, scale=0.8, size=(1000, 1))
    data = np.hstack([feat_0_19, feat_20]).astype(np.float32)
    return data, feat_20.flatten()

def get_expected_stats(feat_20):
    res = stats.ttest_1samp(feat_20, popmean=0.0)
    p_value = res.pvalue
    ci_lower, ci_upper = stats.t.interval(0.95, df=len(feat_20)-1, loc=np.mean(feat_20), scale=stats.sem(feat_20))
    return p_value, ci_lower, ci_upper

def get_expected_recommendations(data, item_id=0):
    torch.manual_seed(42)
    model = nn.Sequential(
        nn.Linear(21, 128),
        nn.ReLU(),
        nn.Linear(128, 64),
        nn.ReLU()
    )

    with torch.no_grad():
        x = torch.tensor(data)
        embeddings = model(x)

    embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)
    sim_matrix = torch.mm(embeddings, embeddings.t())

    sims = sim_matrix[item_id].clone()
    sims[item_id] = -float('inf')
    top5 = torch.topk(sims, 5).indices.tolist()
    return top5

def test_stats_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/stats: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data_json = response.json()
    assert "p_value" in data_json, "Missing 'p_value' in response"
    assert "ci_lower" in data_json, "Missing 'ci_lower' in response"
    assert "ci_upper" in data_json, "Missing 'ci_upper' in response"

    _, feat_20 = get_expected_data()
    expected_p, expected_ci_lower, expected_ci_upper = get_expected_stats(feat_20)

    assert abs(data_json["p_value"] - expected_p) < 1e-5 or (data_json["p_value"] < 1e-10 and expected_p < 1e-10), \
        f"p_value mismatch. Expected ~{expected_p}, got {data_json['p_value']}"
    assert abs(data_json["ci_lower"] - expected_ci_lower) < 1e-2, \
        f"ci_lower mismatch. Expected {expected_ci_lower}, got {data_json['ci_lower']}"
    assert abs(data_json["ci_upper"] - expected_ci_upper) < 1e-2, \
        f"ci_upper mismatch. Expected {expected_ci_upper}, got {data_json['ci_upper']}"

def test_recommend_endpoint():
    item_id = 0
    try:
        response = requests.get(f"{BASE_URL}/recommend?item_id={item_id}", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/recommend: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data_json = response.json()
    assert "similar_items" in data_json, "Missing 'similar_items' in response"

    data, _ = get_expected_data()
    expected_top5 = get_expected_recommendations(data, item_id)

    assert data_json["similar_items"] == expected_top5, \
        f"similar_items mismatch. Expected {expected_top5}, got {data_json['similar_items']}"