# test_final_state.py
import os
import json
import subprocess
import glob

def test_cycle_frames_json():
    json_path = "/home/user/cycle_frames.json"
    assert os.path.isfile(json_path), f"Missing required output file: {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    assert "cycle_frames" in data, f"Key 'cycle_frames' missing in {json_path}"

    expected_frames = [45, 46, 47, 120, 121, 250, 251, 252, 253]
    actual_frames = data["cycle_frames"]

    assert actual_frames == expected_frames, f"Expected cycle_frames to be {expected_frames}, but got {actual_frames}"

def test_quality_gate_adversarial():
    script_path = "/home/user/quality_gate.py"
    assert os.path.isfile(script_path), f"Missing quality gate script: {script_path}"

    clean_dir = "/app/verifier/clean"
    evil_dir = "/app/verifier/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_clean = []
    for cf in clean_files:
        result = subprocess.run(["python3", script_path, cf], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "ACCEPT":
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        result = subprocess.run(["python3", script_path, ef], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "REJECT":
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: " + ", ".join(failed_clean))
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted: " + ", ".join(failed_evil))

    if error_msgs:
        assert False, " | ".join(error_msgs)