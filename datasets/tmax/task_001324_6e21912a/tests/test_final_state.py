# test_final_state.py

import os
import json
import subprocess
import pytest

def run_detector(input_dir, output_file):
    script_path = "/home/user/detector.py"
    assert os.path.exists(script_path), f"Detector script not found at {script_path}"

    # Run the detector script
    result = subprocess.run(
        ["python3", script_path, input_dir, output_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Detector script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert os.path.exists(output_file), f"Output file {output_file} was not created."

def test_evil_corpus_classification():
    evil_dir = "/test/corpus/evil/"
    out_file = "/tmp/out_evil.json"

    if os.path.exists(out_file):
        os.remove(out_file)

    run_detector(evil_dir, out_file)

    with open(out_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {out_file} is not valid JSON.")

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    bypassed = []
    for f in evil_files:
        if f not in results:
            bypassed.append(f"{f} (missing from output)")
        elif results[f] != "C2":
            bypassed.append(f"{f} (classified as {results[f]})")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: " + ", ".join(bypassed[:10]) + ("..." if len(bypassed) > 10 else ""))

def test_clean_corpus_classification():
    clean_dir = "/test/corpus/clean/"
    out_file = "/tmp/out_clean.json"

    if os.path.exists(out_file):
        os.remove(out_file)

    run_detector(clean_dir, out_file)

    with open(out_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {out_file} is not valid JSON.")

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    modified = []
    for f in clean_files:
        if f not in results:
            modified.append(f"{f} (missing from output)")
        elif results[f] != "BENIGN":
            modified.append(f"{f} (classified as {results[f]})")

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified: " + ", ".join(modified[:10]) + ("..." if len(modified) > 10 else ""))

def test_no_binary_invocation():
    # Ensure the script doesn't just call the binary.
    # While it's hard to statically prove they didn't call it, we can check if they imported subprocess/os.system
    # Actually, the prompt says "The automated testing environment will run your script on an isolated system where the binary is not present."
    # Since we are testing in the environment, we can temporarily move the binary and run it again to ensure it doesn't depend on it.
    binary_path = "/app/c2_auth_check"
    backup_path = "/app/c2_auth_check.bak"

    if os.path.exists(binary_path):
        os.rename(binary_path, backup_path)

    try:
        clean_dir = "/test/corpus/clean/"
        out_file = "/tmp/out_clean_isolated.json"

        if os.path.exists(out_file):
            os.remove(out_file)

        run_detector(clean_dir, out_file)

        with open(out_file, 'r') as f:
            results = json.load(f)

        clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
        assert len(results) == len(clean_files), "Detector failed to process all files when binary was removed."

    finally:
        if os.path.exists(backup_path):
            os.rename(backup_path, binary_path)