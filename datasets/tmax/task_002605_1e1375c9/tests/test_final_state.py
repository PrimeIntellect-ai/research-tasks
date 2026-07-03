# test_final_state.py

import os
import json
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/traffic_sanitizer.py"
EVIL_CORPUS_DIR = "/app/corpora/evil"
CLEAN_CORPUS_DIR = "/app/corpora/clean"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_evil_corpus_redacted():
    """Assert that the agent's script correctly redacts all evil payloads."""
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in evil_files:
            input_path = os.path.join(EVIL_CORPUS_DIR, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run([SCRIPT_PATH, input_path, output_path], capture_output=True, text=True)
            if result.returncode != 0:
                failed_files.append((filename, f"Script crashed with return code {result.returncode}"))
                continue

            if not os.path.exists(output_path):
                failed_files.append((filename, "Output file not created"))
                continue

            try:
                with open(output_path, 'r') as f:
                    out_data = json.load(f)

                header_val = out_data.get("headers", {}).get("X-Diagnostic-Dump")
                if header_val != "[REDACTED_ELF]":
                    failed_files.append((filename, f"Header not redacted. Got: {header_val}"))
            except Exception as e:
                failed_files.append((filename, f"Failed to parse output JSON: {e}"))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(evil_files)} evil bypassed.\n"
        error_msg += "\n".join([f"{f}: {reason}" for f, reason in failed_files[:10]])
        if len(failed_files) > 10:
            error_msg += f"\n... and {len(failed_files) - 10} more."
        pytest.fail(error_msg)

def test_clean_corpus_preserved():
    """Assert that the agent's script preserves all clean payloads without modification."""
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in clean_files:
            input_path = os.path.join(CLEAN_CORPUS_DIR, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run([SCRIPT_PATH, input_path, output_path], capture_output=True, text=True)
            if result.returncode != 0:
                failed_files.append((filename, f"Script crashed with return code {result.returncode}"))
                continue

            if not os.path.exists(output_path):
                failed_files.append((filename, "Output file not created"))
                continue

            try:
                with open(input_path, 'r') as f:
                    in_data = json.load(f)
                with open(output_path, 'r') as f:
                    out_data = json.load(f)

                if in_data != out_data:
                    failed_files.append((filename, "Output JSON does not match input JSON semantically"))
            except Exception as e:
                failed_files.append((filename, f"Failed to parse JSON: {e}"))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(clean_files)} clean modified.\n"
        error_msg += "\n".join([f"{f}: {reason}" for f, reason in failed_files[:10]])
        if len(failed_files) > 10:
            error_msg += f"\n... and {len(failed_files) - 10} more."
        pytest.fail(error_msg)