# test_final_state.py

import os
import subprocess
import tempfile
import shutil
import urllib.request
import urllib.error
import pytest

SANITIZER_PATH = "/home/user/sanitizer/elf_sanitizer"
CLEAN_CORPUS = "/home/user/corpora/clean"
EVIL_CORPUS = "/home/user/corpora/evil"

def test_sanitizer_binary_exists():
    assert os.path.isfile(SANITIZER_PATH), f"Sanitizer binary not found at {SANITIZER_PATH}"
    assert os.access(SANITIZER_PATH, os.X_OK), f"Sanitizer binary at {SANITIZER_PATH} is not executable"

def test_sanitizer_adversarial_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.elf')]
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.elf')]

    assert len(evil_files) > 0, "No evil ELF files found in corpus"
    assert len(clean_files) > 0, "No clean ELF files found in corpus"

    evil_bypassed = []
    clean_modified = []

    for ef in evil_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            shutil.copy(os.path.join(EVIL_CORPUS, ef), tmpdir)
            result = subprocess.run([SANITIZER_PATH, tmpdir], capture_output=True)
            if result.returncode != 1:
                evil_bypassed.append(ef)

    for cf in clean_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            shutil.copy(os.path.join(CLEAN_CORPUS, cf), tmpdir)
            result = subprocess.run([SANITIZER_PATH, tmpdir], capture_output=True)
            if result.returncode != 0:
                clean_modified.append(cf)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified[:5])}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))

def test_end_to_end_api():
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.elf')]
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.elf')]

    if not evil_files or not clean_files:
        pytest.skip("Corpus files not found")

    evil_file = os.path.join(EVIL_CORPUS, evil_files[0])
    clean_file = os.path.join(CLEAN_CORPUS, clean_files[0])

    def upload_file(filepath):
        url = "http://localhost:8080/upload"
        with open(filepath, "rb") as f:
            file_data = f.read()

        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(filepath)}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode('utf-8') + file_data + f"\r\n--{boundary}--\r\n".encode('utf-8')

        req = urllib.request.Request(url, data=body)
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status
        except urllib.error.HTTPError as e:
            return e.code
        except Exception as e:
            pytest.fail(f"HTTP Request failed: {e}")

    # Test clean file
    clean_status = upload_file(clean_file)
    assert clean_status == 200, f"Clean file upload failed, expected HTTP 200 but got {clean_status}"

    # Test evil file
    evil_status = upload_file(evil_file)
    assert evil_status == 403, f"Evil file upload bypassed, expected HTTP 403 but got {evil_status}"