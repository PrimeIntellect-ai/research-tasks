# test_final_state.py

import pytest
import requests
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

URL = "http://127.0.0.1:8000/predict"
TOKEN = "project zeus pipeline"
TEST_FEATURES = [1.5, 0.5, 2.0, 1.0, 3.0]

@pytest.fixture(scope="module")
def expected_prediction():
    np.random.seed(1337)
    X = np.random.exponential(scale=2.0, size=(1000, 5))
    y = X[:, 0] * 3.5 + X[:, 1] * 1.2 - X[:, 2] * 0.5 + np.random.randn(1000) * 0.5

    X_train_raw, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)

    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)

    x_in = np.array([TEST_FEATURES])
    x_in_scaled = scaler.transform(x_in)
    return model.predict(x_in_scaled)[0]

def test_api_unauthorized_no_token():
    """Verify that the API returns 401 when no token is provided."""
    try:
        response = requests.post(URL, json={"features": TEST_FEATURES})
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the API at {URL}. Is the service running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_api_unauthorized_invalid_token():
    """Verify that the API returns 401 when an invalid token is provided."""
    headers = {"Authorization": "Bearer invalid token"}
    try:
        response = requests.post(URL, json={"features": TEST_FEATURES}, headers=headers)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the API at {URL}. Is the service running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_api_authorized_prediction(expected_prediction):
    """Verify that the API returns the correct prediction with the valid token."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.post(URL, json={"features": TEST_FEATURES}, headers=headers)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the API at {URL}. Is the service running?")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "prediction" in data, "Response JSON does not contain 'prediction' key"

    prediction = data["prediction"]
    assert isinstance(prediction, (int, float)), "Prediction is not a number"

    diff = abs(prediction - expected_prediction)
    assert diff < 1e-4, f"Prediction {prediction} is not within 1e-4 of expected {expected_prediction}"