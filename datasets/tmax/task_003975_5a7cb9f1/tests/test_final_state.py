# test_final_state.py

import os
import json
import subprocess
import pytest

def test_scan_clean_corpus():
    scan_script = "/home/user/scan.py"
    assert os.path.isfile(scan_script), f"Scan script not found at {scan_script}"

    clean_dir = "/app/corpora/clean"
    results_file = "/home/user/results.json"

    # Run scan script on clean corpus
    result = subprocess.run(["python3", scan_script, clean_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"scan.py failed with return code {result.returncode}\nStderr: {result.stderr}"

    assert os.path.isfile(results_file), f"Results file not found at {results_file}"

    with open(results_file, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    # Check that all files in clean corpus are marked as clean
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.zip')]
    failed_clean = []

    for f in clean_files:
        if results.get(f) != "clean":
            failed_clean.append(f)

    if failed_clean:
        pytest.fail(f"{len(failed_clean)} of {len(clean_files)} clean files modified/rejected: {', '.join(failed_clean)}")

def test_scan_evil_corpus():
    scan_script = "/home/user/scan.py"
    assert os.path.isfile(scan_script), f"Scan script not found at {scan_script}"

    evil_dir = "/app/corpora/evil"
    results_file = "/home/user/results.json"

    # Run scan script on evil corpus
    result = subprocess.run(["python3", scan_script, evil_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"scan.py failed with return code {result.returncode}\nStderr: {result.stderr}"

    assert os.path.isfile(results_file), f"Results file not found at {results_file}"

    with open(results_file, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    # Check that all files in evil corpus are marked as evil
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.zip')]
    failed_evil = []

    for f in evil_files:
        if results.get(f) != "evil":
            failed_evil.append(f)

    if failed_evil:
        pytest.fail(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed: {', '.join(failed_evil)}")

def test_banned_user():
    banned_file = "/home/user/banned.txt"
    assert os.path.isfile(banned_file), f"Banned user file not found at {banned_file}"

    with open(banned_file, "r") as f:
        banned_user = f.read().strip()

    assert banned_user == "eve_hacker", f"Expected banned user 'eve_hacker', but got '{banned_user}'"