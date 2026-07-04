# test_final_state.py

import os
import json
import subprocess
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_agent_tool():
    """
    Executes the agent's Rust tool against the clean and evil corpora before running assertions.
    """
    app_dir = "/home/user/etl_filter"
    assert os.path.isdir(app_dir), f"Rust application directory missing at {app_dir}"

    # Compile and run on clean corpus
    res_clean = subprocess.run(
        ["cargo", "run", "--release", "--", "--input-dir", "/app/corpus/clean/"],
        cwd=app_dir,
        capture_output=True,
        text=True
    )
    assert res_clean.returncode == 0, f"Cargo run failed on clean corpus.\nSTDOUT:\n{res_clean.stdout}\nSTDERR:\n{res_clean.stderr}"

    # Compile and run on evil corpus
    res_evil = subprocess.run(
        ["cargo", "run", "--release", "--", "--input-dir", "/app/corpus/evil/"],
        cwd=app_dir,
        capture_output=True,
        text=True
    )
    assert res_evil.returncode == 0, f"Cargo run failed on evil corpus.\nSTDOUT:\n{res_evil.stdout}\nSTDERR:\n{res_evil.stderr}"

def test_audio_baseline():
    baseline_path = "/home/user/audio_baseline.txt"
    assert os.path.isfile(baseline_path), f"Audio baseline output missing at {baseline_path}"

    with open(baseline_path, "r") as f:
        content = f.read().strip()

    assert content == "0.63", f"Expected average amplitude to be '0.63', but got '{content}'"

def test_clean_corpus_preserved():
    clean_dir = "/app/corpus/clean/"
    sanitized_dir = os.path.join(clean_dir, "sanitized")

    assert os.path.isdir(sanitized_dir), f"Sanitized directory not created for clean corpus at {sanitized_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".json")]
    assert len(clean_files) > 0, "No JSON files found in clean corpus"

    failed_files = []

    for filename in clean_files:
        orig_path = os.path.join(clean_dir, filename)
        san_path = os.path.join(sanitized_dir, filename)

        if not os.path.isfile(san_path):
            failed_files.append(filename)
            continue

        with open(orig_path, "r") as f:
            orig_data = json.load(f)

        with open(san_path, "r") as f:
            try:
                san_data = json.load(f)
            except json.JSONDecodeError:
                failed_files.append(filename)
                continue

        # Compare records (ignoring order if necessary, but length should match exactly)
        if len(orig_data) != len(san_data):
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified or omitted: {failed_files}"

def test_evil_corpus_rejected():
    evil_dir = "/app/corpus/evil/"
    sanitized_dir = os.path.join(evil_dir, "sanitized")

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".json")]
    assert len(evil_files) > 0, "No JSON files found in evil corpus"

    bypassed_files = []

    if os.path.isdir(sanitized_dir):
        for filename in evil_files:
            san_path = os.path.join(sanitized_dir, filename)
            if os.path.isfile(san_path):
                # Check if the output file contains any records
                with open(san_path, "r") as f:
                    content = f.read().strip()
                    if not content:
                        continue
                    try:
                        san_data = json.load(f)
                        if isinstance(san_data, list) and len(san_data) > 0:
                            bypassed_files.append(filename)
                    except json.JSONDecodeError:
                        pass

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed sanitization: {bypassed_files}"