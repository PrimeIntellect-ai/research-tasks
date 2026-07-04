# test_final_state.py

import subprocess
import requests
import random
import pytest

def get_embeddings():
    cmd = [
        "ffmpeg", "-i", "/app/traffic_camera.mp4",
        "-vf", "fps=1",
        "-f", "image2pipe",
        "-pix_fmt", "rgb24",
        "-vcodec", "rawvideo",
        "-"
    ]
    proc = subprocess.run(cmd, capture_output=True, check=True)
    raw_data = proc.stdout
    frame_size = 320 * 240 * 3
    num_frames = len(raw_data) // frame_size
    embeddings = []
    for i in range(num_frames):
        frame_data = raw_data[i*frame_size:(i+1)*frame_size]
        r = sum(frame_data[0::3]) / (320*240)
        g = sum(frame_data[1::3]) / (320*240)
        b = sum(frame_data[2::3]) / (320*240)
        embeddings.append((r, g, b))
    return embeddings

def get_covariance(embeddings, ddof=1):
    n = len(embeddings)
    means = [sum(x)/n for x in zip(*embeddings)]
    cov = [[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            cov[i][j] = sum((e[i]-means[i])*(e[j]-means[j]) for e in embeddings) / (n - ddof)
    return cov

def get_bootstrap_red(embeddings):
    reds = [e[0] for e in embeddings]
    random.seed(42)
    n = len(reds)
    means = []
    for _ in range(10000):
        sample = [random.choice(reds) for _ in range(n)]
        means.append(sum(sample)/n)
    means.sort()

    # Percentile method
    lower = means[int(10000 * 0.025)]
    upper = means[int(10000 * 0.975)]
    return lower, upper

@pytest.fixture(scope="module")
def embeddings():
    return get_embeddings()

def test_covariance_endpoint(embeddings):
    try:
        response = requests.get("http://127.0.0.1:8080/covariance", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to /covariance endpoint: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    lines = response.text.strip().split('\n')
    assert len(lines) == 3, f"Expected 3 rows in covariance matrix, got {len(lines)}"

    actual_cov = []
    for line in lines:
        parts = line.split(',')
        assert len(parts) == 3, f"Expected 3 columns in covariance matrix, got {len(parts)} in line: {line}"
        actual_cov.append([float(p) for p in parts])

    expected_cov_ddof1 = get_covariance(embeddings, ddof=1)
    expected_cov_ddof0 = get_covariance(embeddings, ddof=0)

    # Check against both ddof=1 and ddof=0
    match_ddof1 = True
    match_ddof0 = True
    for i in range(3):
        for j in range(3):
            if abs(actual_cov[i][j] - expected_cov_ddof1[i][j]) > 0.5:
                match_ddof1 = False
            if abs(actual_cov[i][j] - expected_cov_ddof0[i][j]) > 0.5:
                match_ddof0 = False

    assert match_ddof1 or match_ddof0, f"Covariance matrix does not match expected values. Actual: {actual_cov}"

def test_bootstrap_endpoint(embeddings):
    try:
        response = requests.get("http://127.0.0.1:8080/bootstrap_red", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to /bootstrap_red endpoint: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    line = response.text.strip()
    parts = line.split(',')
    assert len(parts) == 2, f"Expected 2 values (lower, upper), got {len(parts)} in response: {line}"

    actual_lower = float(parts[0])
    actual_upper = float(parts[1])

    expected_lower, expected_upper = get_bootstrap_red(embeddings)

    assert abs(actual_lower - expected_lower) < 1.0, f"Lower bound {actual_lower} is too far from expected {expected_lower}"
    assert abs(actual_upper - expected_upper) < 1.0, f"Upper bound {actual_upper} is too far from expected {expected_upper}"