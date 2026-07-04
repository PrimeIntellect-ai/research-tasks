# test_final_state.py

import os
import subprocess
import pytest

def test_audio_trigger():
    txt_path = "/home/user/audio_trigger.txt"
    assert os.path.isfile(txt_path), f"File {txt_path} is missing. You must transcribe the audio trigger."
    with open(txt_path, "r") as f:
        content = f.read().strip().lower()

    expected = "restart cluster maintenance override"
    assert content == expected, f"Incorrect audio transcription. Expected '{expected}', but got '{content}'."

def test_daemon_processor_fixed():
    processor_path = "/home/user/daemon/processor.py"
    assert os.path.isfile(processor_path), f"File {processor_path} is missing."

    result = subprocess.run(["python3", processor_path, "--test"], capture_output=True, text=True)
    expected_output = '{"error": "circular reference detected"}'
    assert expected_output in result.stdout, (
        f"Processor did not return expected error JSON. "
        f"Expected to find '{expected_output}' in stdout. Output: {result.stdout}"
    )

def test_log_filter_adversarial():
    py_script = "/home/user/log_filter.py"
    sh_script = "/home/user/log_filter.sh"

    if os.path.isfile(py_script):
        cmd_prefix = ["python3", py_script]
    elif os.path.isfile(sh_script):
        cmd_prefix = ["bash", sh_script]
    else:
        pytest.fail("Neither /home/user/log_filter.py nor /home/user/log_filter.sh found. You must create the log filter script.")

    evil_logs_dir = "/app/evil_logs/"
    clean_logs_dir = "/app/clean_logs/"

    assert os.path.isdir(evil_logs_dir), f"Evil logs directory missing at {evil_logs_dir}"
    assert os.path.isdir(clean_logs_dir), f"Clean logs directory missing at {clean_logs_dir}"

    evil_files = sorted([os.path.join(evil_logs_dir, f) for f in os.listdir(evil_logs_dir) if os.path.isfile(os.path.join(evil_logs_dir, f))])
    clean_files = sorted([os.path.join(clean_logs_dir, f) for f in os.listdir(clean_logs_dir) if os.path.isfile(os.path.join(clean_logs_dir, f))])

    assert len(evil_files) > 0, "No evil log files found to test."
    assert len(clean_files) > 0, "No clean log files found to test."

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run(cmd_prefix + [f], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        res = subprocess.run(cmd_prefix + [f], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (expected exit code 1): {', '.join(evil_bypassed[:5])}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (expected exit code 0): {', '.join(clean_modified[:5])}")

    if errors:
        pytest.fail(" | ".join(errors))