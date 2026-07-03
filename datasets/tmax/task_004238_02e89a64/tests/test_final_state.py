# test_final_state.py

import os
import subprocess
import tempfile
import pytest

AGENT_SCRIPT = "/home/user/detector.py"
CLEAN_CORPUS = "/app/corpus/clean/tokens.txt"
EVIL_CORPUS = "/app/corpus/evil/tokens.txt"

def run_detector(input_file, output_file):
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    result = subprocess.run(
        ["python3", AGENT_SCRIPT, input_file, output_file],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nstderr: {result.stderr}"
    assert os.path.exists(output_file), f"Output file not created at {output_file}"

def test_clean_corpus():
    with tempfile.NamedTemporaryFile(delete=False) as tmp_out:
        out_path = tmp_out.name

    try:
        run_detector(CLEAN_CORPUS, out_path)

        with open(CLEAN_CORPUS, "r") as f:
            clean_tokens = f.read().splitlines()
        with open(out_path, "r") as f:
            out_tokens = f.read().splitlines()

        assert len(clean_tokens) == len(out_tokens), f"Expected {len(clean_tokens)} output lines, got {len(out_tokens)}"

        modified_count = 0
        for i, (expected, actual) in enumerate(zip(clean_tokens, out_tokens)):
            if expected != actual:
                modified_count += 1

        assert modified_count == 0, f"{modified_count} of {len(clean_tokens)} clean tokens modified."
    finally:
        if os.path.exists(out_path):
            os.remove(out_path)

def test_evil_corpus():
    with tempfile.NamedTemporaryFile(delete=False) as tmp_out:
        out_path = tmp_out.name

    try:
        run_detector(EVIL_CORPUS, out_path)

        with open(EVIL_CORPUS, "r") as f:
            evil_tokens = f.read().splitlines()
        with open(out_path, "r") as f:
            out_tokens = f.read().splitlines()

        assert len(evil_tokens) == len(out_tokens), f"Expected {len(evil_tokens)} output lines, got {len(out_tokens)}"

        bypassed_count = 0
        for i, actual in enumerate(out_tokens):
            if actual != "[MALICIOUS_TOKEN_REDACTED]":
                bypassed_count += 1

        assert bypassed_count == 0, f"{bypassed_count} of {len(evil_tokens)} evil tokens bypassed redaction."
    finally:
        if os.path.exists(out_path):
            os.remove(out_path)