# test_final_state.py

import os
import subprocess
import pytest
from pathlib import Path

SCRIPT_PATH = "/home/user/cert_filter.py"
EVIL_CORPUS = "/app/corpus/evil/"
CLEAN_CORPUS = "/app/corpus/clean/"

def run_script(corpus_path):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, corpus_path],
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr, result.returncode

def parse_output(stdout):
    results = {}
    for line in stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if " - " in line:
            filename, status = line.rsplit(" - ", 1)
            results[filename.strip()] = status.strip()
    return results

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Student script not found at {SCRIPT_PATH}"

def test_evil_corpus():
    stdout, stderr, returncode = run_script(EVIL_CORPUS)
    assert returncode == 0, f"Script failed on evil corpus with return code {returncode}.\nStderr: {stderr}"

    results = parse_output(stdout)
    evil_files = [f.name for f in Path(EVIL_CORPUS).glob("*.pem")]

    assert len(evil_files) > 0, "No files found in evil corpus."

    bypassed = []
    for f in evil_files:
        if f not in results:
            bypassed.append(f"{f} (missing from output)")
        elif results[f] != "EVIL":
            bypassed.append(f"{f} (marked as {results[f]})")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed:\n" + "\n".join(bypassed))

def test_clean_corpus():
    stdout, stderr, returncode = run_script(CLEAN_CORPUS)
    assert returncode == 0, f"Script failed on clean corpus with return code {returncode}.\nStderr: {stderr}"

    results = parse_output(stdout)
    clean_files = [f.name for f in Path(CLEAN_CORPUS).glob("*.pem")]

    assert len(clean_files) > 0, "No files found in clean corpus."

    modified = []
    for f in clean_files:
        if f not in results:
            modified.append(f"{f} (missing from output)")
        elif results[f] != "CLEAN":
            modified.append(f"{f} (marked as {results[f]})")

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (flagged as EVIL):\n" + "\n".join(modified))