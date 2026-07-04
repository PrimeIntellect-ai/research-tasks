# test_final_state.py
import os
import subprocess
import pytest

def test_required_files_exist():
    expected_files = [
        "/home/user/model.pkl",
        "/home/user/detector.py",
        "/home/user/video_features.csv",
        "/home/user/video_result.txt"
    ]
    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Expected file {file_path} is missing."

def test_video_result():
    with open("/home/user/video_result.txt", "r") as f:
        content = f.read().strip()
    assert content == "EVIL", f"Expected /home/user/video_result.txt to contain 'EVIL', but got '{content}'."

def run_detector(csv_path):
    result = subprocess.run(
        ["python", "/home/user/detector.py", csv_path],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def test_adversarial_corpus():
    evil_dir = "/app/eval_corpus/evil"
    clean_dir = "/app/eval_corpus/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".csv")]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".csv")]

    assert len(evil_files) > 0, "No CSV files found in evil corpus."
    assert len(clean_files) > 0, "No CSV files found in clean corpus."

    bypassed_evil = []
    for evil_csv in evil_files:
        output = run_detector(evil_csv)
        if output != "EVIL":
            bypassed_evil.append(os.path.basename(evil_csv))

    modified_clean = []
    for clean_csv in clean_files:
        output = run_detector(clean_csv)
        if output != "CLEAN":
            modified_clean.append(os.path.basename(clean_csv))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))