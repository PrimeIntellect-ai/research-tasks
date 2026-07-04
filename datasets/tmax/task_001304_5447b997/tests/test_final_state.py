# test_final_state.py
import os
import json
import string
import subprocess
import pytest

def test_json_report():
    report_path = '/home/user/recovery_report.json'
    assert os.path.isfile(report_path), f"Report file not found at {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "transcription" in data, "Missing 'transcription' key in report."
    assert "crash_timestamp" in data, "Missing 'crash_timestamp' key in report."
    assert "last_recovered_tx_id" in data, "Missing 'last_recovered_tx_id' key in report."

    # Check transcription
    transcription = data["transcription"].lower()
    # strip punctuation
    transcription = transcription.translate(str.maketrans('', '', string.punctuation))
    expected_phrase = "evacuation order authorized for sector seven"
    assert expected_phrase in transcription, f"Transcription does not contain expected phrase. Got: {data['transcription']}"

    # Check crash_timestamp
    assert data["crash_timestamp"] == "2023-10-27T08:14:02Z", f"Incorrect crash_timestamp. Got: {data['crash_timestamp']}"

    # Check last_recovered_tx_id
    assert data["last_recovered_tx_id"] == "9402", f"Incorrect last_recovered_tx_id. Got: {data['last_recovered_tx_id']}"

def test_rust_pii_filter():
    # Build the Rust project first to ensure we test the latest code
    build_cmd = ["cargo", "build", "--release"]
    try:
        subprocess.run(build_cmd, cwd="/app/pii-filter", check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to build Rust project: {e.stderr.decode('utf-8', errors='replace')}")

    binary_path = "/app/pii-filter/target/release/pii-filter"
    assert os.path.isfile(binary_path), f"Rust binary not found at {binary_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.txt')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.txt')]

    clean_modified = []
    evil_bypassed = []

    for cf in clean_files:
        filepath = os.path.join(clean_dir, cf)
        result = subprocess.run([binary_path, filepath], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(cf)

    for ef in evil_files:
        filepath = os.path.join(evil_dir, ef)
        result = subprocess.run([binary_path, filepath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(ef)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))