# test_final_state.py
import os
import subprocess
import time
import socket
import pytest

MAIL_FILTER_BIN = "/home/user/mail_filter"
FORWARDER_SCRIPT = "/home/user/start_forwarder.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_mail_filter_exists_and_executable():
    assert os.path.isfile(MAIL_FILTER_BIN), f"Binary {MAIL_FILTER_BIN} does not exist."
    assert os.access(MAIL_FILTER_BIN, os.X_OK), f"Binary {MAIL_FILTER_BIN} is not executable."

def test_adversarial_corpus_mail_filter():
    """
    Test the mail_filter binary against the clean and evil corpora.
    Clean emails must exit 0, Evil emails must exit 1.
    """
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.eml')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.eml')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for cf in clean_files:
        with open(cf, 'rb') as f:
            proc = subprocess.run([MAIL_FILTER_BIN], stdin=f, capture_output=True)
            if proc.returncode != 0:
                clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        with open(ef, 'rb') as f:
            proc = subprocess.run([MAIL_FILTER_BIN], stdin=f, capture_output=True)
            if proc.returncode != 1:
                evil_failed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed[:5])}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed[:5])}")

    assert not errors, "Corpus verification failed:\n" + "\n".join(errors)

def test_forwarder_script_exists_and_executable():
    assert os.path.isfile(FORWARDER_SCRIPT), f"Script {FORWARDER_SCRIPT} does not exist."
    assert os.access(FORWARDER_SCRIPT, os.X_OK), f"Script {FORWARDER_SCRIPT} is not executable."

def test_forwarder_functionality():
    """
    Test the bash automation script.
    It should listen on 10025, pipe to mail_filter, and forward to 10026 if accepted.
    """
    # Find a clean and an evil email
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.eml')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.eml')]

    clean_email_path = clean_files[0]
    evil_email_path = evil_files[0]

    with open(clean_email_path, 'rb') as f:
        clean_email_data = f.read()
    with open(evil_email_path, 'rb') as f:
        evil_email_data = f.read()

    # Start dummy listener on 10026
    receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver.bind(('127.0.0.1', 10026))
    receiver.listen(1)
    receiver.settimeout(2.0)

    # Start the forwarder script
    forwarder_proc = subprocess.Popen([FORWARDER_SCRIPT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1) # Wait for it to start listening on 10025

    try:
        # Test clean email
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender.connect(('127.0.0.1', 10025))
        sender.sendall(clean_email_data)
        sender.close()

        try:
            conn, addr = receiver.accept()
            conn.settimeout(2.0)
            received_data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                received_data += chunk
            conn.close()
            assert received_data == clean_email_data, "Forwarded clean email data does not match original."
        except socket.timeout:
            pytest.fail("Did not receive forwarded clean email on port 10026.")

        # Test evil email
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender.connect(('127.0.0.1', 10025))
        sender.sendall(evil_email_data)
        sender.close()

        try:
            conn, addr = receiver.accept()
            conn.settimeout(2.0)
            received_data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                received_data += chunk
            conn.close()
            assert received_data == b"", "Received data for evil email on port 10026, but should have been dropped."
        except socket.timeout:
            # This is expected, evil email should not be forwarded
            pass

    finally:
        forwarder_proc.terminate()
        forwarder_proc.wait(timeout=2)
        receiver.close()