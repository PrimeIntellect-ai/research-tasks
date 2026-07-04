# test_final_state.py

import os
import json
import glob
import subprocess
import pytest

def test_video_analysis_output():
    analysis_file = "/home/user/video_analysis.json"
    assert os.path.exists(analysis_file), f"File {analysis_file} does not exist."

    with open(analysis_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{analysis_file} is not valid JSON.")

    assert "frame_number" in data, "Missing 'frame_number' in video_analysis.json"
    assert "transaction_id" in data, "Missing 'transaction_id' in video_analysis.json"

    assert data["frame_number"] == 142, f"Expected frame_number 142, got {data['frame_number']}"
    assert data["transaction_id"] == "TX_8432", f"Expected transaction_id 'TX_8432', got '{data['transaction_id']}'"

def test_deadlock_detector_script():
    script_path = "/home/user/deadlock_detector.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_failures = []
    clean_failures = []

    # Test evil corpus (expected: {"status": "deadlock"})
    for file_path in evil_files:
        result = subprocess.run(
            ["python3", script_path, file_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            evil_failures.append(f"{os.path.basename(file_path)} (crashed)")
            continue

        try:
            out_data = json.loads(result.stdout.strip())
            if out_data.get("status") != "deadlock":
                evil_failures.append(f"{os.path.basename(file_path)} (got {out_data.get('status')})")
        except json.JSONDecodeError:
            evil_failures.append(f"{os.path.basename(file_path)} (invalid JSON output)")

    # Test clean corpus (expected: {"status": "clean"})
    for file_path in clean_files:
        result = subprocess.run(
            ["python3", script_path, file_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            clean_failures.append(f"{os.path.basename(file_path)} (crashed)")
            continue

        try:
            out_data = json.loads(result.stdout.strip())
            if out_data.get("status") != "clean":
                clean_failures.append(f"{os.path.basename(file_path)} (got {out_data.get('status')})")
        except json.JSONDecodeError:
            clean_failures.append(f"{os.path.basename(file_path)} (invalid JSON output)")

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified: {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))