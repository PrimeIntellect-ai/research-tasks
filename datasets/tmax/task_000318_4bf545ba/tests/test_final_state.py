# test_final_state.py
import pytest
import requests
import torch
import torch.nn as nn

API_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer data_ops_2024"}

class SimpleMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )

    def forward(self, x):
        return self.net(x)

def get_expected_prediction():
    model = SimpleMLP()
    model.load_state_dict(torch.load('/home/user/model/weights.pth'))
    model.eval()
    with torch.no_grad():
        input_tensor = torch.tensor([[25.0, 50.0, 1013.0]], dtype=torch.float32)
        return model(input_tensor).item()

def test_api_unauthorized():
    """Ensure the API requires authentication."""
    try:
        response = requests.get(f"{API_URL}/stats", timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("API server is not running on 127.0.0.1:8080.")

    assert response.status_code in [401, 403], f"Expected 401/403 for unauthorized request, got {response.status_code}."

def test_api_stats():
    """Check the GET /stats endpoint for correct cleaning statistics."""
    try:
        response = requests.get(f"{API_URL}/stats", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("API server is not running on 127.0.0.1:8080.")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "dropped_outliers" in data, "Missing 'dropped_outliers' in /stats response."
    assert "imputed_missing" in data, "Missing 'imputed_missing' in /stats response."

    assert data["dropped_outliers"] == 2, f"Expected 2 dropped outliers, got {data['dropped_outliers']}."
    assert data["imputed_missing"] == 2, f"Expected 2 imputed missing values, got {data['imputed_missing']}."

def test_api_predict():
    """Check the POST /predict endpoint for correct model inference."""
    payload = {
        "temperature": 25.0,
        "humidity": 50.0,
        "pressure": 1013.0
    }
    try:
        response = requests.post(f"{API_URL}/predict", headers=AUTH_HEADER, json=payload, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("API server is not running on 127.0.0.1:8080.")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "prediction" in data, "Missing 'prediction' in /predict response."

    expected_pred = get_expected_prediction()
    actual_pred = data["prediction"]

    assert abs(actual_pred - expected_pred) < 1e-4, f"Prediction mismatch. Expected {expected_pred}, got {actual_pred}."