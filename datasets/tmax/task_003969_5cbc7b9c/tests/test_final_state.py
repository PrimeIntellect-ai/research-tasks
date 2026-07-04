# test_final_state.py

import os
import time
import socket
import subprocess
import pytest

EVIL_CORPUS_PATH = "/app/telemetry_env/corpora/evil/"
CLEAN_CORPUS_PATH = "/app/telemetry_env/corpora/clean/"
DROPPED_LOG = "/tmp/dropped_payloads.log"
INGESTOR_BIN = "/app/telemetry_env/bin/telemetry_ingestor"
MAKEFILE_PATH = "/app/telemetry_env/src/Makefile"

def test_makefile_fixed():
    """Verify the Makefile was updated to use the v2 serialization library."""
    assert os.path.isfile(MAKEFILE_PATH), f"Makefile missing at {MAKEFILE_PATH}"
    with open(MAKEFILE_PATH, 'r') as f:
        content = f.read()
    assert "/opt/libser/v2" in content, "Makefile does not link against the correct library version (/opt/libser/v2)."
    assert "/opt/libser/v1" not in content, "Makefile still contains references to the old library version (/opt/libser/v1)."

def test_ingestor_running():
    """Verify the ingestor binary is compiled and running."""
    assert os.path.isfile(INGESTOR_BIN), f"Compiled binary missing at {INGESTOR_BIN}"

    # Check if process is running
    try:
        output = subprocess.check_output(["pgrep", "-f", "telemetry_ingestor"]).decode().strip()
        assert output, "telemetry_ingestor process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("telemetry_ingestor process is not running.")

def test_adversarial_corpus():
    """
    Send clean and evil corpora through the running ingestor.
    Verify clean payloads are NOT dropped and evil payloads ARE dropped.
    """
    # Clear the dropped payloads log before testing
    if os.path.exists(DROPPED_LOG):
        os.remove(DROPPED_LOG)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ingestor_address = ('127.0.0.1', 8080)

    # Process Clean Corpus
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_PATH) if os.path.isfile(os.path.join(CLEAN_CORPUS_PATH, f))]
    assert clean_files, "Clean corpus is empty."

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_PATH, filename)
        with open(filepath, 'rb') as f:
            data = f.read()
        sock.sendto(data, ingestor_address)
        time.sleep(0.01) # Small delay to prevent UDP buffer overflow

    time.sleep(1) # Wait for processing

    # Check that no clean payloads were dropped
    if os.path.exists(DROPPED_LOG):
        with open(DROPPED_LOG, 'r') as f:
            dropped_clean = f.readlines()
        assert len(dropped_clean) == 0, f"{len(dropped_clean)} of {len(clean_files)} clean payloads were incorrectly dropped."

    # Process Evil Corpus
    evil_files = [f for f in os.listdir(EVIL_CORPUS_PATH) if os.path.isfile(os.path.join(EVIL_CORPUS_PATH, f))]
    assert evil_files, "Evil corpus is empty."

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_PATH, filename)
        with open(filepath, 'rb') as f:
            data = f.read()
        sock.sendto(data, ingestor_address)
        time.sleep(0.01)

    time.sleep(1) # Wait for processing

    # Check that ALL evil payloads were dropped
    assert os.path.exists(DROPPED_LOG), "Dropped payloads log was not created after sending evil payloads."
    with open(DROPPED_LOG, 'r') as f:
        dropped_evil = f.readlines()

    dropped_count = len([line for line in dropped_evil if line.startswith("DROPPED:")])

    if dropped_count < len(evil_files):
        bypassed = len(evil_files) - dropped_count
        pytest.fail(f"{bypassed} of {len(evil_files)} evil payloads bypassed the filter.")

    assert dropped_count >= len(evil_files), f"Expected at least {len(evil_files)} dropped logs, got {dropped_count}."