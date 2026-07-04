# test_final_state.py

import os
import subprocess
import requests
import pytest

def get_expected_t_init():
    cmd = [
        "ffmpeg", "-i", "/app/thermal_experiment.mp4",
        "-vf", "select=eq(n\\,20),format=gray",
        "-vframes", "1",
        "-f", "rawvideo", "-"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    data = res.stdout
    if not data:
        return None, None
    avg_floor = int(sum(data) / len(data))
    avg_round = round(sum(data) / len(data))
    return avg_floor, avg_round

def test_profiling_report():
    report_path = "/home/user/profiling_report.txt"
    assert os.path.exists(report_path), f"Profiling report not found at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in profiling report, got {len(lines)}"

    t_init_line = lines[0]
    bottleneck_line = lines[1]

    assert t_init_line.startswith("T_INIT="), f"First line must start with T_INIT=, got: {t_init_line}"
    assert bottleneck_line.startswith("BOTTLENECK="), f"Second line must start with BOTTLENECK=, got: {bottleneck_line}"

    try:
        t_init_val = int(t_init_line.split("=")[1])
    except ValueError:
        pytest.fail(f"T_INIT value is not a valid integer: {t_init_line}")

    bottleneck_val = bottleneck_line.split("=")[1]
    assert len(bottleneck_val) > 0, "BOTTLENECK value must not be empty"

    avg_floor, avg_round = get_expected_t_init()
    if avg_floor is not None:
        assert t_init_val in (avg_floor, avg_round), f"Expected T_INIT to be {avg_floor} or {avg_round}, got {t_init_val}"

def test_health_endpoint():
    try:
        resp = requests.get("http://127.0.0.1:8000/health", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /health endpoint: {e}")

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"
    assert resp.text.strip() == "OK", f"Expected body 'OK', got '{resp.text}'"

def test_simulate_endpoint():
    try:
        resp = requests.get("http://127.0.0.1:8000/simulate?steps=10", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /simulate endpoint: {e}")

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert isinstance(data, list), f"Expected JSON array, got {type(data)}"
    assert len(data) == 100, f"Expected exactly 100 points, got {len(data)}"

    for i, val in enumerate(data):
        assert isinstance(val, (int, float)), f"Value at index {i} is not a number: {val}"