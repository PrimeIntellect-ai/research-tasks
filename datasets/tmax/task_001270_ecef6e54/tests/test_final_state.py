# test_final_state.py

import os
import subprocess
import tempfile
import re
import pytest

CLEAN_CORPUS_DIR = "/home/user/corpus/clean"
EVIL_CORPUS_DIR = "/home/user/corpus/evil"
PIPELINE_SCRIPT = "/home/user/pipeline.sh"
CRON_RUNNER_SCRIPT = "/home/user/cron_runner.sh"
MASKER_BIN = "/app/log-masker-1.0.0/masker"

def test_masker_compiled():
    assert os.path.isfile(MASKER_BIN), f"{MASKER_BIN} does not exist. Did you compile the vendored package?"
    assert os.access(MASKER_BIN, os.X_OK), f"{MASKER_BIN} is not executable."

def test_pipeline_script_exists_and_executable():
    assert os.path.isfile(PIPELINE_SCRIPT), f"{PIPELINE_SCRIPT} does not exist."
    assert os.access(PIPELINE_SCRIPT, os.X_OK), f"{PIPELINE_SCRIPT} is not executable."

def test_adversarial_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    clean_modified = []
    evil_bypassed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test clean corpus
        for basename in clean_files:
            input_path = os.path.join(CLEAN_CORPUS_DIR, basename)
            output_path = os.path.join(tmpdir, f"clean_{basename}")

            subprocess.run([PIPELINE_SCRIPT, input_path, output_path], capture_output=True, text=True)

            if not os.path.isfile(output_path):
                clean_modified.append(basename)
                continue

            with open(input_path, "r") as f:
                original_content = f.read()
            with open(output_path, "r") as f:
                processed_content = f.read()

            if original_content != processed_content:
                clean_modified.append(basename)

        # Test evil corpus
        for basename in evil_files:
            input_path = os.path.join(EVIL_CORPUS_DIR, basename)
            output_path = os.path.join(tmpdir, f"evil_{basename}")

            subprocess.run([PIPELINE_SCRIPT, input_path, output_path], capture_output=True, text=True)

            if not os.path.isfile(output_path):
                evil_bypassed.append(basename)
                continue

            with open(output_path, "r") as f:
                processed_content = f.read()

            # Check if PII is redacted
            # The prompt says api_key=[32-chars] and ssn=[9-digits] must be redacted to [REDACTED]
            # If we see any api_key= followed by 32 chars or ssn= followed by 9 digits, it's a bypass.
            # Also check if it actually contains [REDACTED].
            if re.search(r'api_key=[a-zA-Z0-9]{32}', processed_content) or re.search(r'ssn=[0-9]{9}', processed_content):
                evil_bypassed.append(basename)
            elif "api_key=[REDACTED]" not in processed_content and "ssn=[REDACTED]" not in processed_content:
                # If it didn't redact properly
                evil_bypassed.append(basename)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))

def test_cron_job_installed():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    crontab_content = result.stdout

    expected_cron = f"*/5 * * * * {CRON_RUNNER_SCRIPT}"

    found = False
    for line in crontab_content.splitlines():
        line = line.strip()
        if line == expected_cron or line.startswith("*/5 * * * *") and CRON_RUNNER_SCRIPT in line:
            found = True
            break

    assert found, f"Cron job not correctly installed. Expected to find '{expected_cron}' in crontab."

def test_cron_runner_script_exists_and_executable():
    assert os.path.isfile(CRON_RUNNER_SCRIPT), f"{CRON_RUNNER_SCRIPT} does not exist."
    assert os.access(CRON_RUNNER_SCRIPT, os.X_OK), f"{CRON_RUNNER_SCRIPT} is not executable."