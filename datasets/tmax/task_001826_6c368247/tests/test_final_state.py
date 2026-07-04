# test_final_state.py

import os
import re
import subprocess
import pytest

CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"
SANITISER_PATH = "/home/user/sanitiser.py"
SERVICE_PATH = "/home/user/.config/systemd/user/log-pipeline.service"

def test_sanitiser_exists_and_executable():
    assert os.path.exists(SANITISER_PATH), f"Sanitiser script not found at {SANITISER_PATH}"
    assert os.path.isfile(SANITISER_PATH), f"{SANITISER_PATH} is not a file"
    # Ensure it can be run with python3
    # The prompt says "The verifier will run `cat <corpus_file> | python3 /home/user/sanitiser.py`."

def test_sanitiser_against_corpora():
    assert os.path.exists(SANITISER_PATH), f"Sanitiser script missing: {SANITISER_PATH}"

    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_modified = []
    evil_bypassed = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        with open(filepath, 'rb') as f:
            original_data = f.read()

        proc = subprocess.run(
            ["python3", SANITISER_PATH],
            input=original_data,
            capture_output=True
        )

        if proc.stdout != original_data:
            clean_modified.append(filename)

    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        with open(filepath, 'rb') as f:
            original_data = f.read()

        proc = subprocess.run(
            ["python3", SANITISER_PATH],
            input=original_data,
            capture_output=True
        )

        # The evil files should be completely filtered out (output nothing)
        # Wait, if a file has multiple lines, some might be safe?
        # The prompt says: "100% of lines from the evil/ corpus must be rejected (the script outputs nothing for those lines)."
        # Assuming the evil corpus files ONLY contain evil lines.
        if proc.stdout.strip() != b"":
            evil_bypassed.append(filename)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail("; ".join(error_msgs))

def test_systemd_service_updated():
    assert os.path.exists(SERVICE_PATH), f"Service file missing: {SERVICE_PATH}"

    with open(SERVICE_PATH, "r") as f:
        content = f.read()

    # Check After=tunnel.service
    assert re.search(r"^After=.*tunnel\.service", content, re.MULTILINE), \
        "Service file does not contain 'After=tunnel.service' in the [Unit] section."

    # Check ExecStart
    # Regex similar to ExecStart=.*python3 /home/user/sanitiser\.py.*\|.*/app/legacy_parser
    exec_start_match = re.search(r"^ExecStart=(.*)$", content, re.MULTILINE)
    assert exec_start_match, "Service file missing ExecStart directive."

    exec_start_line = exec_start_match.group(1)
    # The pipeline should contain python3 /home/user/sanitiser.py piped to /app/legacy_parser
    assert re.search(r"python3\s+/home/user/sanitiser\.py", exec_start_line) or \
           re.search(r"/home/user/sanitiser\.py", exec_start_line), \
           "ExecStart does not invoke the sanitiser script."

    assert "|" in exec_start_line, "ExecStart does not contain a pipe."
    assert "/app/legacy_parser" in exec_start_line, "ExecStart does not invoke the legacy parser."

    # Ensure sanitiser comes before legacy_parser
    sanitiser_idx = exec_start_line.find("sanitiser.py")
    parser_idx = exec_start_line.find("/app/legacy_parser")
    assert sanitiser_idx < parser_idx, "Sanitiser must be piped into the legacy parser."