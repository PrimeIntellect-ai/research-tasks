# test_final_state.py

import os
import subprocess
import tempfile
import json
import stat

def test_binary_exists():
    binary_path = "/home/user/log_sanitizer/target/release/log_sanitizer"
    assert os.path.isfile(binary_path), f"Rust binary not found at {binary_path}. Did you compile it in release mode?"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable."

def test_wrapper_script_exists():
    script_path = "/home/user/run_bridge.sh"
    assert os.path.isfile(script_path), f"Wrapper script not found at {script_path}."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Wrapper script at {script_path} is not executable."

def test_adversarial_corpus():
    binary_path = "/home/user/log_sanitizer/target/release/log_sanitizer"
    clean_corpus = "/app/corpus/clean/clean_logs.jsonl"
    evil_corpus = "/app/corpus/evil/evil_logs.jsonl"

    # Check clean logs
    with tempfile.NamedTemporaryFile(delete=False) as tmp_clean_out:
        clean_out_path = tmp_clean_out.name

    try:
        subprocess.run([binary_path, "--input", clean_corpus, "--output", clean_out_path], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of sanitizer on clean corpus failed: {e.stderr.decode()}")

    with open(clean_corpus, "r") as f:
        clean_input_lines = f.readlines()
    with open(clean_out_path, "r") as f:
        clean_output_lines = f.readlines()

    # Order might not be guaranteed due to parallel processing, so we compare sets of lines or sorted lists
    clean_input_set = set(line.strip() for line in clean_input_lines if line.strip())
    clean_output_set = set(line.strip() for line in clean_output_lines if line.strip())

    missing_clean = clean_input_set - clean_output_set
    assert not missing_clean, f"{len(missing_clean)} of {len(clean_input_set)} clean logs modified or rejected. Example missing: {list(missing_clean)[:1]}"

    # Check evil logs
    with tempfile.NamedTemporaryFile(delete=False) as tmp_evil_out:
        evil_out_path = tmp_evil_out.name

    try:
        subprocess.run([binary_path, "--input", evil_corpus, "--output", evil_out_path], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of sanitizer on evil corpus failed: {e.stderr.decode()}")

    with open(evil_corpus, "r") as f:
        evil_input_lines = f.readlines()
    with open(evil_out_path, "r") as f:
        evil_output_lines = f.readlines()

    evil_output_set = set(line.strip() for line in evil_output_lines if line.strip())

    assert not evil_output_set, f"{len(evil_output_set)} of {len(evil_input_lines)} evil logs bypassed validation. Example bypassed: {list(evil_output_set)[:1]}"

    os.remove(clean_out_path)
    os.remove(evil_out_path)