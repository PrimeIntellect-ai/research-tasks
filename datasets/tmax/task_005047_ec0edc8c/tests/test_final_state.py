# test_final_state.py

import csv
import math
import requests
import pytest

BASE_URL = "http://127.0.0.1:8123"

def load_data():
    data = {}
    with open("/app/customers.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = int(row["uid"])
            feat1 = float(row["feat1"])
            feat2 = float(row["feat2"])
            feat3 = float(row["feat3"])
            spend = float(row["spend"])
            data[uid] = {"feats": (feat1, feat2, feat3), "spend": spend}
    return data

def cosine_similarity(v1, v2):
    dot = sum(x * y for x, y in zip(v1, v2))
    norm1 = math.sqrt(sum(x * x for x in v1))
    norm2 = math.sqrt(sum(x * x for x in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def get_top_3_similar(data, target_uid):
    target_feats = data[target_uid]["feats"]
    sims = []
    for uid, info in data.items():
        if uid == target_uid:
            continue
        sim = cosine_similarity(target_feats, info["feats"])
        sims.append((uid, sim))
    # Sort by similarity descending
    sims.sort(key=lambda x: x[1], reverse=True)
    return [uid for uid, sim in sims[:3]]

@pytest.fixture(scope="module")
def dataset():
    return load_data()

def test_similar_endpoint(dataset):
    """Test the /similar endpoint for a few UIDs."""
    for test_uid in [10, 42, 99]:
        expected_top_3 = get_top_3_similar(dataset, test_uid)

        try:
            response = requests.get(f"{BASE_URL}/similar", params={"uid": test_uid}, timeout=5)
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to /similar endpoint: {e}")

        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

        try:
            result = response.json()
        except ValueError:
            pytest.fail(f"Response from /similar is not valid JSON: {response.text}")

        assert isinstance(result, list), f"Expected a JSON array, got {type(result)}"
        assert len(result) == 3, f"Expected exactly 3 similar UIDs, got {len(result)}"

        # Check if the returned UIDs match the expected ones
        assert result == expected_top_3, f"For UID {test_uid}, expected {expected_top_3}, but got {result}"

def test_predict_endpoint(dataset):
    """Test the /predict endpoint for a few UIDs."""
    for test_uid in [10, 42, 99]:
        try:
            response = requests.get(f"{BASE_URL}/predict", params={"uid": test_uid}, timeout=5)
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to /predict endpoint: {e}")

        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

        try:
            result = response.json()
        except ValueError:
            pytest.fail(f"Response from /predict is not valid JSON: {response.text}")

        assert isinstance(result, float) or isinstance(result, int), f"Expected a JSON float, got {type(result)}"

        # The true model is roughly 2.5*feat1 - 1.2*feat2 + 0.5*feat3
        feats = dataset[test_uid]["feats"]
        approx_true_spend = 2.5 * feats[0] - 1.2 * feats[1] + 0.5 * feats[2]

        # The prediction should be somewhat close to the true spend (within a reasonable margin due to noise and Ridge regularization)
        assert abs(result - approx_true_spend) < 5.0, f"Predicted spend {result} for UID {test_uid} is too far from expected approx true spend {approx_true_spend}"