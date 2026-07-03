# test_final_state.py

import os
import time
import subprocess
import requests
import pytest

EXPECTED_WORDS = [
    "hello", "i", "am", "calling", "because", "my", "internet", "connection", 
    "is", "completely", "unresponsive", "and", "i", "demand", "an", 
    "immediate", "cancellation", "of", "my", "subscription"
]

def test_transcript_csv():
    transcript_path = "/home/user/transcript.csv"
    assert os.path.exists(transcript_path), f"Transcript file {transcript_path} is missing."

    with open(transcript_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(EXPECTED_WORDS), f"Expected {len(EXPECTED_WORDS)} lines in transcript, found {len(lines)}"

    for i, expected_word in enumerate(EXPECTED_WORDS):
        expected_line = f"{i},{expected_word}"
        assert lines[i] == expected_line, f"Line {i} mismatch: expected '{expected_line}', got '{lines[i]}'"

def test_feed_script_and_server_metrics():
    feed_script = "/home/user/feed.sh"
    assert os.path.exists(feed_script), f"Feed script {feed_script} is missing."
    assert os.access(feed_script, os.X_OK), f"Feed script {feed_script} is not executable."

    # Run feed.sh a few times to ensure all data is processed
    for _ in range(3):
        subprocess.run([feed_script], check=False)
        time.sleep(1)

    # Allow server time to process
    time.sleep(2)

    try:
        response = requests.get("http://127.0.0.1:8080/metrics", timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to metrics server at 127.0.0.1:8080 or bad response: {e}")

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "rolling_avg" in data, "JSON response missing 'rolling_avg' key."
    assert "anomalies" in data, "JSON response missing 'anomalies' key."

    rolling_avg = float(data["rolling_avg"])
    anomalies = int(data["anomalies"])

    # Based on the derived pipeline logic, after 20 words:
    # rolling_avg should be 6.1 and anomalies should be 7.
    assert abs(rolling_avg - 6.1) < 0.05, f"Expected rolling_avg ~6.1, got {rolling_avg}"
    assert anomalies == 7, f"Expected 7 anomalies, got {anomalies}"