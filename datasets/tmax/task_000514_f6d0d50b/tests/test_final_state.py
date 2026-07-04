# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_rl_check_compiled_and_executable():
    path = "/home/user/rate_limiter/rl_check"
    assert os.path.isfile(path), f"Compiled executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_validate_job_sh_exists_and_executable():
    path = "/home/user/validate_job.sh"
    assert os.path.isfile(path), f"Script {path} is missing."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

def test_adversarial_corpus_validation():
    script_path = "/home/user/validate_job.sh"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run([script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        result = subprocess.run([script_path, ef], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean rejected: " + ", ".join(clean_failed))
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: " + ", ".join(evil_bypassed))

    assert not errors, "Adversarial corpus validation failed:\n" + "\n".join(errors)

def test_output_frame_exists_and_valid():
    path = "/home/user/output_frame.jpg"
    assert os.path.isfile(path), f"Output frame {path} is missing."

    # Use ffprobe to verify the frame size
    cmd = [
        "ffprobe", "-v", "error", 
        "-select_streams", "v:0", 
        "-show_entries", "stream=width,height", 
        "-of", "csv=s=x:p=0", 
        path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        dimensions = result.stdout.strip()
        assert dimensions == "640x480", f"Expected frame dimensions 640x480, got {dimensions}."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"ffprobe failed to read {path}. Is it a valid image? Error: {e.stderr}")
    except FileNotFoundError:
        pytest.fail("ffprobe command not found, cannot verify image dimensions.")

def test_benchmark_txt_exists_and_valid():
    path = "/home/user/benchmark.txt"
    assert os.path.isfile(path), f"Benchmark file {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "User time" in content, f"{path} does not contain expected '/usr/bin/time -v' output (missing 'User time')."