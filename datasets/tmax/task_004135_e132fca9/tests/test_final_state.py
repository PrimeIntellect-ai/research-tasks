# test_final_state.py

import requests
import pytest

def test_api_north_wing():
    """Verify the API response for North_Wing."""
    url = "http://127.0.0.1:8000/api/v1/sensor_stats?location=North_Wing"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "location" in data, "Missing 'location' in response"
    assert data["location"] == "North_Wing", f"Expected location 'North_Wing', got {data['location']}"

    assert "pca_explained_variance" in data, "Missing 'pca_explained_variance' in response"
    assert isinstance(data["pca_explained_variance"], (int, float)), "pca_explained_variance must be a number"
    assert 0.0 <= data["pca_explained_variance"] <= 1.0, f"pca_explained_variance should be between 0 and 1, got {data['pca_explained_variance']}"

    assert "bootstrap_ci_95" in data, "Missing 'bootstrap_ci_95' in response"
    assert isinstance(data["bootstrap_ci_95"], list) and len(data["bootstrap_ci_95"]) == 2, "bootstrap_ci_95 must be a list of 2 numbers"
    assert data["bootstrap_ci_95"][0] < data["bootstrap_ci_95"][1], "bootstrap_ci_95 lower bound must be less than upper bound"

    assert "ttest_p_value" in data, "Missing 'ttest_p_value' in response"
    assert isinstance(data["ttest_p_value"], (int, float)), "ttest_p_value must be a number"
    assert 0.0 <= data["ttest_p_value"] <= 1.0, f"ttest_p_value should be between 0 and 1, got {data['ttest_p_value']}"

def test_api_south_wing():
    """Verify the API response for South_Wing."""
    url = "http://127.0.0.1:8000/api/v1/sensor_stats?location=South_Wing"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "location" in data, "Missing 'location' in response"
    assert data["location"] == "South_Wing", f"Expected location 'South_Wing', got {data['location']}"

    assert "pca_explained_variance" in data, "Missing 'pca_explained_variance' in response"
    assert isinstance(data["pca_explained_variance"], (int, float)), "pca_explained_variance must be a number"
    assert 0.0 <= data["pca_explained_variance"] <= 1.0, f"pca_explained_variance should be between 0 and 1, got {data['pca_explained_variance']}"

    assert "bootstrap_ci_95" in data, "Missing 'bootstrap_ci_95' in response"
    assert isinstance(data["bootstrap_ci_95"], list) and len(data["bootstrap_ci_95"]) == 2, "bootstrap_ci_95 must be a list of 2 numbers"
    assert data["bootstrap_ci_95"][0] < data["bootstrap_ci_95"][1], "bootstrap_ci_95 lower bound must be less than upper bound"

    assert "ttest_p_value" in data, "Missing 'ttest_p_value' in response"
    assert isinstance(data["ttest_p_value"], (int, float)), "ttest_p_value must be a number"
    assert 0.0 <= data["ttest_p_value"] <= 1.0, f"ttest_p_value should be between 0 and 1, got {data['ttest_p_value']}"