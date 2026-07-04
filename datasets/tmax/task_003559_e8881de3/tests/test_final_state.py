# test_final_state.py

import os
import subprocess
import pytest

def test_bypass_seed_recovered():
    """Check if the bypass seed was correctly recovered from the video."""
    seed_file = "/home/user/bypass_seed.txt"
    assert os.path.isfile(seed_file), f"Expected seed file not found at {seed_file}"

    with open(seed_file, "r") as f:
        content = f.read().strip()

    expected_seed = "BYPASS_SEED:xyz_hx99_v2"
    assert content == expected_seed, f"Incorrect seed recovered. Expected '{expected_seed}', got '{content}'"

def test_waf_binary_exists():
    """Check if the compiled WAF binary exists and is executable."""
    binary_path = "/home/user/waf"
    assert os.path.isfile(binary_path), f"WAF binary not found at {binary_path}. Did you compile your C++ code?"
    assert os.access(binary_path, os.X_OK), f"WAF binary at {binary_path} is not executable."

def test_waf_adversarial_corpus():
    """Evaluate the WAF against the clean and evil corpora."""
    binary_path = "/home/user/waf"
    assert os.path.isfile(binary_path), "Cannot run WAF tests: binary missing."

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_files = sorted([f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))])
    clean_files = sorted([f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))])

    bypassed_evil = []
    for evil_file in evil_files:
        file_path = os.path.join(evil_dir, evil_file)
        with open(file_path, "rb") as f:
            input_data = f.read()

        try:
            result = subprocess.run(
                [binary_path], 
                input=input_data, 
                capture_output=True, 
                timeout=2
            )
            output = result.stdout.decode('utf-8', errors='ignore').strip()
            if output != "REJECT":
                bypassed_evil.append(evil_file)
        except subprocess.TimeoutExpired:
            bypassed_evil.append(f"{evil_file} (Timeout)")
        except Exception as e:
            bypassed_evil.append(f"{evil_file} (Error: {e})")

    modified_clean = []
    for clean_file in clean_files:
        file_path = os.path.join(clean_dir, clean_file)
        with open(file_path, "rb") as f:
            input_data = f.read()

        try:
            result = subprocess.run(
                [binary_path], 
                input=input_data, 
                capture_output=True, 
                timeout=2
            )
            output = result.stdout.decode('utf-8', errors='ignore').strip()
            if output != "ACCEPT":
                modified_clean.append(clean_file)
        except subprocess.TimeoutExpired:
            modified_clean.append(f"{clean_file} (Timeout)")
        except Exception as e:
            modified_clean.append(f"{clean_file} (Error: {e})")

    error_messages = []
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    assert not error_messages, " | ".join(error_messages)