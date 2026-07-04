# test_final_state.py

import os
import json
import subprocess
import requests
import pytest

def get_ground_truth_apds():
    truth_dir = "/tmp/truth_frames"
    os.makedirs(truth_dir, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-i", "/app/video.mp4", "-vf", "fps=1", 
        "-pix_fmt", "gray", f"{truth_dir}/frame_%04d.pgm"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    frames = sorted([f for f in os.listdir(truth_dir) if f.endswith(".pgm")])
    apds = []
    prev_data = None

    for frame in frames:
        filepath = os.path.join(truth_dir, frame)
        with open(filepath, 'rb') as f:
            data = f.read()

        tokens = []
        idx = 0
        while len(tokens) < 4:
            while idx < len(data) and data[idx:idx+1].isspace():
                idx += 1
            if idx < len(data) and data[idx] == ord('#'):
                while idx < len(data) and data[idx] != ord('\n'):
                    idx += 1
                continue
            start = idx
            while idx < len(data) and not data[idx:idx+1].isspace():
                idx += 1
            tokens.append(data[start:idx])

        # The single whitespace character after maxval is skipped
        # The rest is binary data
        pixel_data = data[idx+1:]

        if prev_data is not None:
            total_diff = sum(abs(a - b) for a, b in zip(pixel_data, prev_data))
            apd = total_diff / len(pixel_data)
            apds.append(apd)
        prev_data = pixel_data

    return apds

@pytest.fixture(scope="session")
def ground_truth():
    apds = get_ground_truth_apds()
    def _get_events(threshold):
        return [i + 2 for i, apd in enumerate(apds) if apd > threshold]
    return _get_events

def test_pipeline_go_exists():
    assert os.path.isfile("/home/user/pipeline.go"), "/home/user/pipeline.go does not exist."

def test_experiments_jsonl(ground_truth):
    exp_file = "/home/user/experiments.jsonl"
    assert os.path.isfile(exp_file), f"{exp_file} does not exist."

    with open(exp_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in {exp_file}, got {len(lines)}"

    results = {}
    for line in lines:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON line in {exp_file}: {line}")

        assert "threshold" in data and "event_count" in data, f"Missing keys in JSON line: {line}"
        results[data["threshold"]] = data["event_count"]

    for t in [5, 10, 15, 20]:
        assert t in results, f"Missing threshold {t} in {exp_file}"
        expected_count = len(ground_truth(t))
        assert results[t] == expected_count, f"For threshold {t}, expected {expected_count} events, got {results[t]}"

def test_api_unauthorized():
    url = "http://127.0.0.1:9090/api/events?threshold=10"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without API key, got {response.status_code}"

@pytest.mark.parametrize("threshold", [5, 15])
def test_api_events_authorized(ground_truth, threshold):
    url = f"http://127.0.0.1:9090/api/events?threshold={threshold}"
    headers = {"X-API-Key": "etl-golang-video"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "events" in data, f"Missing 'events' key in response: {data}"

    expected_events = ground_truth(threshold)
    assert data["events"] == expected_events, f"Expected events {expected_events} for threshold {threshold}, got {data['events']}"