# test_final_state.py

import os
import subprocess
import pytest

def test_makefile_fixed_and_compiles():
    log_tool_dir = "/home/user/log_tool"
    assert os.path.isdir(log_tool_dir), f"Directory {log_tool_dir} is missing."

    # Run make to compile the tool
    result = subprocess.run(["make"], cwd=log_tool_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with output:\n{result.stderr}\n{result.stdout}"

    parser_path = os.path.join(log_tool_dir, "parser")
    assert os.path.isfile(parser_path), f"Compiled binary {parser_path} is missing."
    assert os.access(parser_path, os.X_OK), f"Compiled binary {parser_path} is not executable."

def test_filter_script_exists():
    filter_path = "/home/user/filter.py"
    assert os.path.isfile(filter_path), f"Filter script missing at {filter_path}"

def test_adversarial_corpus_filtering():
    filter_path = "/home/user/filter.py"
    evil_corpus_dir = "/app/corpus/evil"
    clean_corpus_dir = "/app/corpus/clean"

    assert os.path.isdir(evil_corpus_dir), f"Missing evil corpus at {evil_corpus_dir}"
    assert os.path.isdir(clean_corpus_dir), f"Missing clean corpus at {clean_corpus_dir}"

    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]
    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]

    evil_bypassed = []
    clean_modified = []

    # Test Evil Corpus
    for evil_file in evil_files:
        result = subprocess.run(["python3", filter_path, evil_file], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "":
            evil_bypassed.append(os.path.basename(evil_file))

    # Test Clean Corpus
    for clean_file in clean_files:
        with open(clean_file, 'r') as f:
            expected_output = f.read()

        result = subprocess.run(["python3", filter_path, clean_file], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout != expected_output:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))