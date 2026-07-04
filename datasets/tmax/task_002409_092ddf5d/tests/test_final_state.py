# test_final_state.py
import os
import subprocess
import pytest

def test_config_perturbation_fixed():
    config_path = "/app/vendor/tabular/config.go"
    assert os.path.isfile(config_path), f"Vendored package file {config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read()
    assert "DisableImputation = true" not in content, "The perturbation in config.go was not fixed. DisableImputation is still true."

def test_go_program_exists():
    assert os.path.isfile("/home/user/filter_data.go"), "/home/user/filter_data.go is missing."

def test_adversarial_corpus():
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean CSV files found."
    assert len(evil_files) > 0, "No evil CSV files found."

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run(
            ["go", "run", "filter_data.go", cf],
            cwd="/home/user",
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            clean_failures.append(f"{os.path.basename(cf)} (Execution failed: {result.stderr.strip()})")
            continue

        lines = [line for line in result.stdout.strip().split('\n') if line.strip()]
        # Clean files should have >0 data rows, meaning >1 line (header + data)
        if len(lines) <= 1:
            clean_failures.append(f"{os.path.basename(cf)} (Produced {len(lines)} lines, expected > 1)")

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run(
            ["go", "run", "filter_data.go", ef],
            cwd="/home/user",
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            # If it exits gracefully with no output, it should have returncode 0. 
            # If it fails, we consider it a bypass if it's not a graceful rejection.
            # But the prompt allows exiting gracefully. Let's assume non-zero is a crash, not graceful.
            pass # We'll just check stdout if it succeeds, but a crash might be acceptable for evil? 
                 # "or exit gracefully with no output". Graceful implies returncode 0.
                 # Let's be strict and check output lines anyway.

        lines = [line for line in result.stdout.strip().split('\n') if line.strip()]
        # Evil files should have 0 data rows, meaning <= 1 line (header only or empty)
        if len(lines) > 1 and result.returncode == 0:
            evil_failures.append(f"{os.path.basename(ef)} (Produced {len(lines)} lines, expected <= 1)")

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: " + ", ".join(evil_failures))
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/failed: " + ", ".join(clean_failures))

    assert not error_messages, " | ".join(error_messages)