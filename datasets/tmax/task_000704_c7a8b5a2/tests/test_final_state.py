# test_final_state.py

import os
import subprocess
import time
import socket
import pytest

FIREWALL_SCRIPT = "/home/user/firewall.sh"
CLEAN_CORPUS_DIR = "/home/user/corpora/clean/"
EVIL_CORPUS_DIR = "/home/user/corpora/evil/"
EVIL_GOLDEN_DIR = "/home/user/corpora/evil_golden/"
START_PIPELINE = "/app/services/start_pipeline.sh"

def run_firewall_on_file(input_file):
    """Run the firewall script on a given input file and return the stdout."""
    with open(input_file, "rb") as f:
        result = subprocess.run(
            [FIREWALL_SCRIPT],
            stdin=f,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
    return result.stdout.decode("utf-8")

def test_firewall_exists_and_executable():
    assert os.path.isfile(FIREWALL_SCRIPT), f"Missing firewall script: {FIREWALL_SCRIPT}"
    assert os.access(FIREWALL_SCRIPT, os.X_OK), f"Firewall script is not executable: {FIREWALL_SCRIPT}"

def test_clean_corpus_preserved():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory."

    modified_files = []
    total = len(clean_files)

    for filename in clean_files:
        input_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(input_path, "r", encoding="utf-8") as f:
            expected_output = f.read()

        actual_output = run_firewall_on_file(input_path)

        if actual_output != expected_output:
            modified_files.append(filename)

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {total} clean modified: {', '.join(modified_files)}")

def test_evil_corpus_sanitized():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    bypassed_files = []
    total = len(evil_files)

    for filename in evil_files:
        input_path = os.path.join(EVIL_CORPUS_DIR, filename)
        golden_path = os.path.join(EVIL_GOLDEN_DIR, filename)

        assert os.path.isfile(golden_path), f"Missing golden file for {filename}"

        with open(golden_path, "r", encoding="utf-8") as f:
            expected_output = f.read()

        actual_output = run_firewall_on_file(input_path)

        if actual_output != expected_output:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {total} evil bypassed: {', '.join(bypassed_files)}")

def test_start_pipeline_composition():
    assert os.path.isfile(START_PIPELINE), f"Missing pipeline script: {START_PIPELINE}"
    with open(START_PIPELINE, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that it pipes receiver to firewall to aggregator
    # We can check for the presence of the script names and pipe characters
    assert "receiver.sh" in content, "start_pipeline.sh does not call receiver.sh"
    assert "firewall.sh" in content, "start_pipeline.sh does not call firewall.sh"
    assert "aggregator.sh" in content, "start_pipeline.sh does not call aggregator.sh"
    assert "|" in content, "start_pipeline.sh does not use pipes to connect the services"

def test_end_to_end_flow():
    # Start the pipeline
    pipeline_proc = subprocess.Popen(
        [START_PIPELINE],
        cwd="/app/services/",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    try:
        # Wait for receiver to start listening
        time.sleep(1)

        # Send data to localhost:9090
        test_data = (
            "2023-10-12T10:05:00|10.0.0.3|C\u200bharlie|My SSN is 123-45-6789\n"
            "2023-10-12T10:05:01Z|10.0.0.4|Dave|Hello\n"
        )

        try:
            with socket.create_connection(("localhost", 9090), timeout=2) as sock:
                sock.sendall(test_data.encode("utf-8"))
        except Exception as e:
            pytest.fail(f"Failed to connect to receiver on port 9090: {e}")

        # Give it time to process
        time.sleep(2)

        # Check aggregated.log
        aggregated_log = "/tmp/aggregated.log"
        assert os.path.isfile(aggregated_log), "Aggregated log was not created."

        with open(aggregated_log, "r", encoding="utf-8") as f:
            content = f.read()

        # Check sanitization in the end-to-end output
        assert "***-**-****" in content, "PII was not anonymized in end-to-end flow."
        assert "123-45-6789" not in content, "PII leaked in end-to-end flow."
        assert "\u200b" not in content, "Zero-width space was not removed in end-to-end flow."
        assert "2023-10-12T10:05:00Z" in content, "Timestamp was not aligned in end-to-end flow."

    finally:
        # Clean up the process group
        import signal
        try:
            os.killpg(os.getpgid(pipeline_proc.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass