# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_task1_c_log_processor():
    executable = "/home/user/log_tool/log_processor"
    assert os.path.isfile(executable), f"Executable {executable} is missing. Did you compile the C program?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_task2_go_sanitizer():
    sanitizer_path = "/home/user/sanitizer.go"
    assert os.path.isfile(sanitizer_path), f"Go sanitizer not found at {sanitizer_path}"

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_rejected = []

    for f in evil_files:
        res = subprocess.run(["go", "run", sanitizer_path, f], capture_output=True)
        # Evil files MUST be rejected (non-zero exit code)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(f))

    for f in clean_files:
        res = subprocess.run(["go", "run", sanitizer_path, f], capture_output=True)
        # Clean files MUST be accepted (zero exit code)
        if res.returncode != 0:
            clean_rejected.append(os.path.basename(f))

    err_msg = []
    if evil_bypassed:
        err_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        err_msg.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")

    if err_msg:
        pytest.fail(" | ".join(err_msg))

def test_task3_video_analysis():
    output_file = "/home/user/red_frame.txt"
    assert os.path.isfile(output_file), f"File {output_file} is missing. Did you run the video analysis?"
    with open(output_file, "r") as f:
        content = f.read().strip()
    assert content == "142", f"Expected red frame index 142, but got '{content}'"