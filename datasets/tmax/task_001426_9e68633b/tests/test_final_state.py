# test_final_state.py

import os
import subprocess
import pytest

def test_detector_script_exists():
    script_path = "/home/user/detector.py"
    assert os.path.isfile(script_path), f"Detector script not found at {script_path}"

def test_clean_corpus_accepted():
    script_path = "/home/user/detector.py"
    clean_dir = "/app/corpus/clean/"

    expected_files = {f for f in os.listdir(clean_dir) if f.endswith(".json")}
    assert len(expected_files) > 0, "No clean files found to test."

    result = subprocess.run(
        ["python3", script_path, clean_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed on clean corpus with error: {result.stderr}"

    output_lines = set(line.strip() for line in result.stdout.strip().split("\n") if line.strip())

    missing = expected_files - output_lines
    extra = output_lines - expected_files

    assert not missing, f"{len(missing)} of {len(expected_files)} clean files were incorrectly rejected: {missing}"
    assert not extra, f"Script output unexpected lines for clean corpus: {extra}"

def test_evil_corpus_rejected():
    script_path = "/home/user/detector.py"
    evil_dir = "/app/corpus/evil/"

    evil_files = {f for f in os.listdir(evil_dir) if f.endswith(".json")}
    assert len(evil_files) > 0, "No evil files found to test."

    result = subprocess.run(
        ["python3", script_path, evil_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed on evil corpus with error: {result.stderr}"

    output_lines = set(line.strip() for line in result.stdout.strip().split("\n") if line.strip())

    bypassed = output_lines.intersection(evil_files)

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil files bypassed the filter: {bypassed}"
    assert not output_lines, f"Script output unexpected lines for evil corpus: {output_lines}"

def test_log_file_created():
    log_file = "/home/user/pipeline.log"
    assert os.path.isfile(log_file), f"Log file not created at {log_file}"