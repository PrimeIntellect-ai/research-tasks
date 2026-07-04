# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_filter_sh_exists_and_executable():
    script_path = "/home/user/filter.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_adversarial_corpus_clean():
    script_path = "/home/user/filter.sh"
    clean_dir = "/app/hidden_corpus/clean"

    if not os.path.exists(clean_dir):
        pytest.skip("Hidden clean corpus not found, skipping.")

    clean_files = glob.glob(os.path.join(clean_dir, "*.jpg")) + glob.glob(os.path.join(clean_dir, "*.jpeg"))
    if not clean_files:
        pytest.skip("No images found in hidden clean corpus.")

    failed_files = []
    for img in clean_files:
        result = subprocess.run([script_path, img], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(img))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean images were incorrectly flagged as evil (exit code != 0). Offending files: {failed_files[:5]}..."

def test_adversarial_corpus_evil():
    script_path = "/home/user/filter.sh"
    evil_dir = "/app/hidden_corpus/evil"

    if not os.path.exists(evil_dir):
        pytest.skip("Hidden evil corpus not found, skipping.")

    evil_files = glob.glob(os.path.join(evil_dir, "*.jpg")) + glob.glob(os.path.join(evil_dir, "*.jpeg"))
    if not evil_files:
        pytest.skip("No images found in hidden evil corpus.")

    failed_files = []
    for img in evil_files:
        result = subprocess.run([script_path, img], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(img))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil images bypassed the filter (exit code != 1). Offending files: {failed_files[:5]}..."

def test_anomalies_txt():
    anomalies_path = "/home/user/anomalies.txt"
    assert os.path.exists(anomalies_path), f"{anomalies_path} does not exist."

    with open(anomalies_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "anomalies.txt is empty."

    # Check if frame_012 to frame_018 (or similar indices) are the only ones
    # Since ffmpeg might be 0-indexed or 1-indexed, we check if the numbers are consecutive and 7 in total
    # Or we can just check that it contains 7 items and they contain '12', '13', '14', '15', '16', '17', '18' or '13' to '19'
    import re
    numbers = []
    for line in lines:
        match = re.search(r'\d+', line)
        if match:
            numbers.append(int(match.group()))

    assert len(numbers) >= 6 and len(numbers) <= 8, f"Expected around 7 anomalies, found {len(numbers)}: {lines}"

    # Check consecutive
    numbers.sort()
    assert numbers[-1] - numbers[0] == len(numbers) - 1, f"Anomalies are not consecutive frames: {lines}"

def test_fps_txt():
    fps_path = "/home/user/fps.txt"
    assert os.path.exists(fps_path), f"{fps_path} does not exist."

    with open(fps_path, "r") as f:
        content = f.read().strip()

    try:
        fps_val = float(content)
        assert fps_val > 0, "FPS must be greater than 0."
    except ValueError:
        pytest.fail(f"fps.txt does not contain a valid number: {content}")