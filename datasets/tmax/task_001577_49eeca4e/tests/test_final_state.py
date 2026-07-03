# test_final_state.py

import os
import subprocess
import pytest

AGENT_BIN = "/home/user/workspace/log_filter"
CLEAN_CORPUS_DIR = "/app/secret_corpus/clean"
EVIL_CORPUS_DIR = "/app/secret_corpus/evil"

def run_filter(input_text: str) -> str:
    result = subprocess.run(
        [AGENT_BIN],
        input=input_text,
        text=True,
        capture_output=True,
        check=False
    )
    return result.stdout

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_BIN), f"Expected executable not found at {AGENT_BIN}"
    assert os.access(AGENT_BIN, os.X_OK), f"File at {AGENT_BIN} is not executable"

def test_adversarial_corpus_evaluation():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Missing clean corpus dir: {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Missing evil corpus dir: {EVIL_CORPUS_DIR}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    bypassed_evil = []
    modified_clean = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        output = run_filter(content)

        # Evil lines should be completely dropped. 
        # The output should be empty or only contain whitespace/newlines if the input was entirely evil.
        # Let's check line by line to be precise.
        input_lines = content.splitlines()
        output_lines = [line for line in output.splitlines() if line]

        if len(output_lines) > 0:
            bypassed_evil.append(filename)

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        output = run_filter(content)

        # Clean lines should be preserved exactly.
        input_lines = [line for line in content.splitlines() if line]
        output_lines = [line for line in output.splitlines() if line]

        if input_lines != output_lines:
            modified_clean.append(filename)

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if errors:
        pytest.fail(" | ".join(errors))