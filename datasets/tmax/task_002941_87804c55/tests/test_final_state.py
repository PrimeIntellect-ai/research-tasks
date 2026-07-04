# test_final_state.py
import os
import subprocess
import tarfile
import socket
import pytest

BINARY_PATH = "/home/user/safe_archiver/target/release/safe_archiver"
CLEAN_CORPUS = "/opt/corpora/clean"
EVIL_CORPUS = "/opt/corpora/evil"
UPLOAD_DIR = "/tmp/flask_uploads"

def get_redis_value(key):
    """Fetch a value from Redis using raw RESP protocol."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6379))
        cmd = f"*2\r\n$3\r\nGET\r\n${len(key)}\r\n{key}\r\n"
        s.sendall(cmd.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        s.close()

        if data.startswith('$'):
            parts = data.split('\r\n')
            if len(parts) >= 2:
                return parts[1]
        return None
    except Exception:
        return None

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Binary not found at {BINARY_PATH}. Did you build with --release?"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable."

def test_evil_corpus_rejected():
    evil_dirs = sorted([os.path.join(EVIL_CORPUS, d) for d in os.listdir(EVIL_CORPUS) if os.path.isdir(os.path.join(EVIL_CORPUS, d))])
    assert len(evil_dirs) > 0, "No evil directories found to test."

    bypassed = []
    for i, d in enumerate(evil_dirs):
        archive_name = f"evil_test_{i}.tar.gz"
        result = subprocess.run([BINARY_PATH, d, archive_name], capture_output=True)
        if result.returncode != 1:
            bypassed.append(os.path.basename(d))

    assert not bypassed, f"{len(bypassed)} of {len(evil_dirs)} evil bypassed: {bypassed}"

def test_clean_corpus_accepted():
    clean_dirs = sorted([os.path.join(CLEAN_CORPUS, d) for d in os.listdir(CLEAN_CORPUS) if os.path.isdir(os.path.join(CLEAN_CORPUS, d))])
    assert len(clean_dirs) > 0, "No clean directories found to test."

    modified = []
    for i, d in enumerate(clean_dirs):
        archive_name = f"clean_test_{i}.tar.gz"
        result = subprocess.run([BINARY_PATH, d, archive_name], capture_output=True)
        if result.returncode != 0:
            modified.append(os.path.basename(d))

    assert not modified, f"{len(modified)} of {len(clean_dirs)} clean modified/rejected: {modified}"

def test_redis_incremented():
    val = get_redis_value("backup:success")
    assert val is not None, "Could not retrieve backup:success from Redis."
    assert val == "10", f"Expected Redis backup:success to be 10, got {val}"

def test_flask_uploads():
    assert os.path.isdir(UPLOAD_DIR), f"Upload directory {UPLOAD_DIR} does not exist."
    uploads = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".tar.gz")]

    assert len(uploads) == 10, f"Expected 10 uploads in {UPLOAD_DIR}, found {len(uploads)}"

    for upload in uploads:
        path = os.path.join(UPLOAD_DIR, upload)
        try:
            with tarfile.open(path, "r:gz") as tar:
                members = tar.getmembers()
                assert len(members) > 0, f"Archive {upload} is empty."
        except Exception as e:
            pytest.fail(f"Uploaded tarball {upload} is invalid or cannot be read: {e}")