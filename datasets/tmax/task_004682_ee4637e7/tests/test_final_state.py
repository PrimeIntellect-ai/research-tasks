# test_final_state.py
import os
import csv
import json
import math
import subprocess
import pytest

def test_fast_mse_compiled():
    path = "/home/user/src/fast_mse.so"
    assert os.path.isfile(path), f"Compiled shared library {path} is missing."

def test_glitch_filter():
    script_path = "/home/user/glitch_filter.py"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    # Use hidden eval if available, otherwise fallback to the training corpus
    clean_dir = "/app/corpus_hidden_eval/clean/"
    if not os.path.isdir(clean_dir):
        clean_dir = "/app/corpus/clean/"

    evil_dir = "/app/corpus_hidden_eval/evil/"
    if not os.path.isdir(evil_dir):
        evil_dir = "/app/corpus/evil/"

    # Test Clean Corpus
    result_clean = subprocess.run(
        ["python3", script_path, clean_dir],
        capture_output=True, text=True
    )
    assert result_clean.returncode == 0, f"Script failed on clean directory: {result_clean.stderr}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    clean_output_lines = [line.strip() for line in result_clean.stdout.strip().split('\n') if line.strip()]

    # We expect every clean file to be marked as CLEAN
    clean_failures = []
    for line in clean_output_lines:
        if not line.endswith(": CLEAN"):
            clean_failures.append(line)

    # Test Evil Corpus
    result_evil = subprocess.run(
        ["python3", script_path, evil_dir],
        capture_output=True, text=True
    )
    assert result_evil.returncode == 0, f"Script failed on evil directory: {result_evil.stderr}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    evil_output_lines = [line.strip() for line in result_evil.stdout.strip().split('\n') if line.strip()]

    evil_failures = []
    for line in evil_output_lines:
        if not line.endswith(": EVIL"):
            evil_failures.append(line)

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected. Offending: {', '.join(clean_failures[:5])}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed. Offending: {', '.join(evil_failures[:5])}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))

def test_observational_data():
    path = "/home/user/observational_data.csv"
    assert os.path.isfile(path), f"Observational data file {path} is missing."

    frame_60_x = None
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('frame_index') == '60':
                frame_60_x = float(row['x'])
                break

    assert frame_60_x is not None, "Frame 60 is missing from observational_data.csv"

    expected_x = 320 + 150 * 1 * math.exp(-0.015 * 60)
    assert abs(frame_60_x - expected_x) <= 2.0, f"Frame 60 X coordinate {frame_60_x} is not within 2 pixels of expected {expected_x}"

def test_model_params():
    path = "/home/user/model_params.json"
    assert os.path.isfile(path), f"Model parameters file {path} is missing."

    with open(path, 'r') as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "gamma" in params, "Key 'gamma' missing from model_params.json"
    assert "omega" in params, "Key 'omega' missing from model_params.json"

    gamma = float(params["gamma"])
    omega = float(params["omega"])

    expected_gamma = 0.015
    expected_omega = 0.1047

    assert abs(gamma - expected_gamma) / expected_gamma <= 0.05, f"Gamma {gamma} is not within 5% of {expected_gamma}"
    assert abs(omega - expected_omega) / expected_omega <= 0.05, f"Omega {omega} is not within 5% of {expected_omega}"