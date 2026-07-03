# test_final_state.py
import math
import subprocess
import requests
import time
import pytest

def get_video_dimensions(video_path):
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    w, h = map(int, result.stdout.strip().split('x'))
    return w, h

def compute_expected_stats(video_path):
    w, h = get_video_dimensions(video_path)
    frame_size = w * h

    cmd = [
        'ffmpeg', '-i', video_path, '-vf', 'fps=1',
        '-f', 'image2pipe', '-pix_fmt', 'gray', '-vcodec', 'rawvideo', '-'
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    out, _ = process.communicate()

    means = []
    for i in range(0, len(out), frame_size):
        frame = out[i:i+frame_size]
        if len(frame) == frame_size:
            means.append(sum(frame) / frame_size)

    n = len(means)
    x = list(range(1, n + 1))
    y = means

    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(xi*xi for xi in x)
    sum_y2 = sum(yi*yi for yi in y)
    sum_xy = sum(xi*yi for xi, yi in zip(x, y))

    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))

    if denominator == 0:
        r = 0.0
    else:
        r = numerator / denominator

    # We can calculate the t-statistic to verify the p-value roughly if needed,
    # but we will primarily check the correlation coefficient.
    return r, n

def test_api_response():
    """Test that the API is running and returns the correct statistics."""
    url = "http://127.0.0.1:8080/stats"

    # Wait briefly for the server to be available
    max_retries = 5
    response = None
    for _ in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(1)

    assert response is not None, f"Failed to connect to {url}"
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "correlation" in data, "Missing 'correlation' in JSON response"
    assert "p_value" in data, "Missing 'p_value' in JSON response"
    assert "reproducible" in data, "Missing 'reproducible' in JSON response"
    assert data["reproducible"] is True, "'reproducible' must be true"

    expected_r, n = compute_expected_stats("/app/traffic.mp4")

    assert math.isclose(data["correlation"], expected_r, abs_tol=1e-3), \
        f"Correlation mismatch: expected {expected_r}, got {data['correlation']}"

    # Check that p_value is a float
    assert isinstance(data["p_value"], float), "p_value must be a float"