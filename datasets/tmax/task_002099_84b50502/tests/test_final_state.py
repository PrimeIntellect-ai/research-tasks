# test_final_state.py

import os
import subprocess
import tempfile
import pytest

AGENT_SCRIPT = "/home/user/filter.py"
EVIL_CORPUS_DIR = "/app/eval_corpus/evil"
CLEAN_CORPUS_DIR = "/app/eval_corpus/clean"

def run_agent_script(input_path, output_path):
    cmd = ["python3", AGENT_SCRIPT, "--input", input_path, "--output", output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def test_agent_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

def test_adversarial_corpus():
    if not os.path.isfile(AGENT_SCRIPT):
        pytest.fail(f"Cannot test corpus: {AGENT_SCRIPT} is missing.")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    evil_bypassed = []
    clean_modified = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test evil corpus
        for filename in evil_files:
            input_path = os.path.join(EVIL_CORPUS_DIR, filename)
            output_path = os.path.join(tmpdir, f"evil_out_{filename}")

            result = run_agent_script(input_path, output_path)

            if result.returncode != 1 or os.path.exists(output_path):
                evil_bypassed.append(filename)

        # Test clean corpus
        for filename in clean_files:
            input_path = os.path.join(CLEAN_CORPUS_DIR, filename)
            output_path = os.path.join(tmpdir, f"clean_out_{filename}")

            result = run_agent_script(input_path, output_path)

            if result.returncode != 0 or not os.path.exists(output_path):
                clean_modified.append(filename)
            else:
                with open(input_path, "rb") as f_in, open(output_path, "rb") as f_out:
                    if f_in.read() != f_out.read():
                        clean_modified.append(filename)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))