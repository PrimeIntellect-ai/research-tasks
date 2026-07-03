# test_final_state.py
import os
import re
import math
import requests
import pytest

def get_image_features(image_path):
    from PIL import Image
    import numpy as np
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    return [
        float(np.mean(r)),
        float(np.mean(g)),
        float(np.mean(b)),
        float(np.std(r)),
        float(np.std(g)),
        float(np.std(b))
    ]

def get_expected_data():
    frames_dir = "/home/user/frames"
    assert os.path.exists(frames_dir), f"Directory {frames_dir} does not exist."

    frame_files = [f for f in os.listdir(frames_dir) if re.match(r"^frame_\d+\.png$", f)]
    assert len(frame_files) > 0, "No frames extracted."

    N = len(frame_files)
    features = {}
    for i in range(1, N + 1):
        frame_path = os.path.join(frames_dir, f"frame_{i}.png")
        assert os.path.exists(frame_path), f"Missing {frame_path}"
        features[i] = get_image_features(frame_path)

    train_n = N // 2
    train_features = [features[i] for i in range(1, train_n + 1)]

    # Compute train means and stds
    train_means = []
    train_stds = []
    for col in range(6):
        col_vals = [f[col] for f in train_features]
        mean_val = sum(col_vals) / len(col_vals)
        train_means.append(mean_val)
        variance = sum((x - mean_val) ** 2 for x in col_vals) / len(col_vals)
        train_stds.append(math.sqrt(variance))

    # Scale all features
    scaled_features = {}
    for i in range(1, N + 1):
        scaled = []
        for col in range(6):
            std = train_stds[col] if train_stds[col] > 0 else 1.0
            val = (features[i][col] - train_means[col]) / std
            scaled.append(val)
        scaled_features[i] = scaled

    return N, train_means, scaled_features

def test_stats_endpoint():
    N, train_means, _ = get_expected_data()
    expected_means_rounded = [round(m, 2) for m in train_means]

    try:
        response = requests.get("http://127.0.0.1:8080/stats", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /stats endpoint: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "train_means" in data, "Missing 'train_means' in response"
    actual_means = data["train_means"]
    assert len(actual_means) == 6, f"Expected 6 means, got {len(actual_means)}"

    for i, (expected, actual) in enumerate(zip(expected_means_rounded, actual_means)):
        assert math.isclose(expected, actual, abs_tol=0.05), f"Mean {i} mismatch: expected ~{expected}, got {actual}"

def test_recommend_endpoint():
    N, _, scaled_features = get_expected_data()
    target_id = 2
    target_feats = scaled_features[target_id]

    distances = []
    for i in range(1, N + 1):
        if i == target_id:
            continue
        feats = scaled_features[i]
        dist = math.sqrt(sum((a - b)**2 for a, b in zip(target_feats, feats)))
        distances.append((dist, i))

    distances.sort()
    expected_recommendations = [i for dist, i in distances[:3]]

    try:
        response = requests.get(f"http://127.0.0.1:8080/recommend?frame_id={target_id}", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /recommend endpoint: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "recommendations" in data, "Missing 'recommendations' in response"
    actual_recommendations = data["recommendations"]

    assert actual_recommendations == expected_recommendations, f"Expected recommendations {expected_recommendations}, got {actual_recommendations}"