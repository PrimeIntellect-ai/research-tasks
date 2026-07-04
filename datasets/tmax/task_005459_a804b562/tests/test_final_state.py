# test_final_state.py
import os
import re
import subprocess
import pytest
import requests

def get_expected_anomalies(video_path="/app/monitoring.mp4"):
    """
    Derive the expected anomalies by running ffmpeg and applying
    the imputation and changepoint detection logic as described in the task.
    """
    cmd = ["ffmpeg", "-i", video_path, "-vf", "signalstats", "-f", "null", "-"]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)

    frames = []
    # Parse ffmpeg signalstats output
    for line in result.stderr.splitlines():
        if "YAVG:" in line and "n:" in line:
            n_match = re.search(r"n:\s*(\d+)", line)
            yavg_match = re.search(r"YAVG:\s*([\d\.]+)", line)
            if n_match and yavg_match:
                frames.append((int(n_match.group(1)), float(yavg_match.group(1))))

    frames.sort(key=lambda x: x[0])

    imputed_yavg = []
    for i in range(len(frames)):
        n, yavg = frames[i]
        if yavg == 0.0:
            # Impute using previous and next valid frames
            prev_y = next((frames[j][1] for j in range(i-1, -1, -1) if frames[j][1] != 0.0), None)
            next_y = next((frames[j][1] for j in range(i+1, len(frames)) if frames[j][1] != 0.0), None)
            if prev_y is not None and next_y is not None:
                yavg = (prev_y + next_y) / 2.0
            elif prev_y is not None:
                yavg = prev_y
            elif next_y is not None:
                yavg = next_y
        imputed_yavg.append(yavg)

    anomalies = []
    for i in range(1, len(frames)):
        diff = abs(imputed_yavg[i] - imputed_yavg[i-1])
        if diff > 50.0:
            anomalies.append((frames[i][0], diff))

    return anomalies

def test_anomalies_csv():
    """Validate that the CSV file was created correctly with the expected anomalies."""
    expected = get_expected_anomalies()
    csv_path = "/home/user/anomalies.csv"
    assert os.path.exists(csv_path), f"CSV file not found: {csv_path}"

    actual = []
    with open(csv_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            assert len(parts) == 2, f"Invalid CSV line format: '{line}'"
            actual.append((int(parts[0]), float(parts[1])))

    assert len(actual) == len(expected), f"Expected {len(expected)} anomalies, but found {len(actual)}"

    for (act_n, act_diff), (exp_n, exp_diff) in zip(actual, expected):
        assert act_n == exp_n, f"Expected frame number {exp_n}, got {act_n}"
        assert abs(act_diff - exp_diff) < 1e-2, f"Expected difference {exp_diff} for frame {exp_n}, got {act_diff}"

def test_http_server():
    """Validate that the HTTP server is running and serves the correct CSV content."""
    url = "http://127.0.0.1:8080/anomalies"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    csv_path = "/home/user/anomalies.csv"
    assert os.path.exists(csv_path), f"CSV file not found: {csv_path}"

    with open(csv_path, "r") as f:
        expected_content = f.read().strip()

    actual_content = response.text.strip()
    assert actual_content == expected_content, "HTTP response body does not match the exact contents of anomalies.csv"