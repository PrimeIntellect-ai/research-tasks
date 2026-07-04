# test_final_state.py

import os
import subprocess
import json
import pytest

def test_red_frames_detection():
    red_frames_path = "/home/user/red_frames.txt"
    assert os.path.isfile(red_frames_path), f"File {red_frames_path} does not exist."

    with open(red_frames_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_frames = ["14", "42", "89"]
    assert lines == expected_frames, f"Expected red frames {expected_frames}, but got {lines}."

def test_rust_binary_exists():
    binary_path = "/home/user/log_filter/target/release/log_filter"
    assert os.path.isfile(binary_path), f"Rust binary not found at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"File at {binary_path} is not executable."

def test_log_sanitiser_clean_corpus():
    binary_path = "/home/user/log_filter/target/release/log_filter"
    clean_corpus_path = "/app/eval/clean_corpus.jsonl"

    assert os.path.isfile(clean_corpus_path), f"Clean corpus not found at {clean_corpus_path}."

    with open(clean_corpus_path, "r") as f:
        clean_lines = [line.strip() for line in f if line.strip()]

    process = subprocess.Popen(
        [binary_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input="\n".join(clean_lines) + "\n")

    output_lines = [line.strip() for line in stdout.splitlines() if line.strip()]

    bypassed = len(clean_lines) - len(output_lines)

    assert len(output_lines) == len(clean_lines), f"{bypassed} of {len(clean_lines)} clean modified or dropped."

    # Optionally, verify JSON equivalence
    for orig, out in zip(clean_lines, output_lines):
        try:
            assert json.loads(orig) == json.loads(out), f"Clean line modified: {orig} -> {out}"
        except json.JSONDecodeError:
            pytest.fail(f"Output line is not valid JSON: {out}")

def test_log_sanitiser_evil_corpus():
    binary_path = "/home/user/log_filter/target/release/log_filter"
    evil_corpus_path = "/app/eval/evil_corpus.jsonl"

    assert os.path.isfile(evil_corpus_path), f"Evil corpus not found at {evil_corpus_path}."

    with open(evil_corpus_path, "r") as f:
        evil_lines = [line.strip() for line in f if line.strip()]

    process = subprocess.Popen(
        [binary_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input="\n".join(evil_lines) + "\n")

    output_lines = [line.strip() for line in stdout.splitlines() if line.strip()]

    bypassed = len(output_lines)

    assert bypassed == 0, f"{bypassed} of {len(evil_lines)} evil bypassed. Offending outputs: {output_lines[:5]}"