# test_final_state.py

import os
import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /health endpoint: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")
    assert data.get("status") == "ok", f"Unexpected response: {data}"

def test_similar_0():
    try:
        resp = requests.get(f"{BASE_URL}/similar?time_sec=0", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /similar endpoint: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "similar_frames" in data, f"Missing 'similar_frames' key in {data}"
    assert isinstance(data["similar_frames"], list), f"'similar_frames' must be a list, got {type(data['similar_frames'])}"
    assert len(data["similar_frames"]) == 3, f"Expected 3 similar frames, got {len(data['similar_frames'])}"
    assert 0 not in data["similar_frames"], "The queried frame (0) should be excluded from results"

def test_similar_5():
    try:
        resp = requests.get(f"{BASE_URL}/similar?time_sec=5", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /similar endpoint: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "similar_frames" in data, f"Missing 'similar_frames' key in {data}"
    assert isinstance(data["similar_frames"], list), f"'similar_frames' must be a list, got {type(data['similar_frames'])}"
    assert len(data["similar_frames"]) == 3, f"Expected 3 similar frames, got {len(data['similar_frames'])}"
    assert 5 not in data["similar_frames"], "The queried frame (5) should be excluded from results"

def test_plot():
    try:
        resp = requests.get(f"{BASE_URL}/plot", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /plot endpoint: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text[:100]}"
    content_type = resp.headers.get("Content-Type", "")
    assert content_type.startswith("image/png"), f"Expected image/png content type, got {content_type}"
    assert len(resp.content) > 0, "Empty image content returned from /plot"

def test_data_3():
    try:
        resp = requests.get(f"{BASE_URL}/data?time_sec=3", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /data endpoint: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "embedding" in data, f"Missing 'embedding' key in {data}"
    assert isinstance(data["embedding"], list), "Embedding should be a list"
    assert len(data["embedding"]) == 4, f"Expected 4-dimensional embedding, got {len(data['embedding'])}"

    assert "temperature" in data, f"Missing 'temperature' in {data}"
    assert "humidity" in data, f"Missing 'humidity' in {data}"
    assert "luminosity" in data, f"Missing 'luminosity' in {data}"

    assert abs(data["temperature"] - 22.4) < 1e-5, f"Expected temperature 22.4, got {data['temperature']}"
    assert abs(data["humidity"] - 45.3) < 1e-5, f"Expected humidity 45.3, got {data['humidity']}"
    assert abs(data["luminosity"] - 210.0) < 1e-5, f"Expected luminosity 210.0, got {data['luminosity']}"

def test_plot_file_exists():
    path = "/app/output/correlation_heatmap.png"
    assert os.path.isfile(path), f"Missing plot file: {path}. The script should have saved it to this location."
    assert os.path.getsize(path) > 0, f"Plot file {path} is empty."