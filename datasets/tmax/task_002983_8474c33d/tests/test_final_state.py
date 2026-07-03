# test_final_state.py
import os
import subprocess
import tempfile
import zipfile

def extract_corpus(temp_dir):
    zip_path = "/app/audit_logs.zip"
    password = b"739284"
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(path=temp_dir, pwd=password)

def test_sanitizer_binary_exists():
    binary_path = "/home/user/sanitizer"
    assert os.path.isfile(binary_path), f"Sanitizer binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Sanitizer at {binary_path} is not executable"

def test_adversarial_corpus():
    binary_path = "/home/user/sanitizer"

    with tempfile.TemporaryDirectory() as temp_dir:
        extract_corpus(temp_dir)

        evil_dir = os.path.join(temp_dir, "evil")
        clean_dir = os.path.join(temp_dir, "clean")

        evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
        clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

        evil_bypassed = []
        clean_modified = []

        for evil_file in evil_files:
            result = subprocess.run([binary_path, evil_file], capture_output=True, text=True)
            if result.returncode != 1 or result.stdout.strip() != "EVIL":
                evil_bypassed.append(os.path.basename(evil_file))

        for clean_file in clean_files:
            result = subprocess.run([binary_path, clean_file], capture_output=True, text=True)
            if result.returncode != 0 or result.stdout.strip() != "CLEAN":
                clean_modified.append(os.path.basename(clean_file))

        error_messages = []
        if evil_bypassed:
            error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

        if error_messages:
            assert False, " | ".join(error_messages)