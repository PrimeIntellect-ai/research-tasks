# test_final_state.py

import os
import subprocess
import pytest

def test_waf_simulator_executable_exists():
    executable_path = "/home/user/waf_simulator"
    assert os.path.isfile(executable_path), f"WAF simulator executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"WAF simulator at {executable_path} is not executable"

def test_waf_simulator_against_corpora():
    executable_path = "/home/user/waf_simulator"
    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".json")]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".json")]

    assert len(evil_files) > 0, f"No JSON files found in evil corpus: {evil_dir}"
    assert len(clean_files) > 0, f"No JSON files found in clean corpus: {clean_dir}"

    evil_bypassed = []
    for evil_file in evil_files:
        file_path = os.path.join(evil_dir, evil_file)
        result = subprocess.run([executable_path, file_path], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(evil_file)

    clean_rejected = []
    for clean_file in clean_files:
        file_path = os.path.join(clean_dir, clean_file)
        result = subprocess.run([executable_path, file_path], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(clean_file)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_rejected)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))