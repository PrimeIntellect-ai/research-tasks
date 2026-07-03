# test_final_state.py
import os
import time
import subprocess
import hashlib
import pytest

def test_c_program_exists():
    assert os.path.exists("/home/user/doc_parser.c"), "C program /home/user/doc_parser.c is missing."

def test_compile_and_executable():
    # Compile if not present, as requested in verification script logic
    if not os.path.exists("/home/user/doc_parser"):
        subprocess.run(["gcc", "/home/user/doc_parser.c", "-o", "/home/user/doc_parser"], check=False)

    assert os.path.exists("/home/user/doc_parser"), "Compiled binary /home/user/doc_parser is missing."
    assert os.access("/home/user/doc_parser", os.X_OK), "/home/user/doc_parser is not executable."

def test_watch_script_exists():
    assert os.path.exists("/home/user/watch.sh"), "Bash script /home/user/watch.sh is missing."
    assert os.access("/home/user/watch.sh", os.X_OK), "/home/user/watch.sh is not executable."

def test_system_integration():
    # Clear manifest for clean test
    with open("/home/user/manifest.txt", "w") as f:
        f.write("")

    # Start watcher
    watcher = subprocess.Popen(["/home/user/watch.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) # Wait for inotifywait to initialize

    try:
        # Create valid gzip file
        valid_content = b"Valid data"
        valid_gz_path = "/home/user/docs/valid_doc.gz"

        # We can use gzip command to create a valid gzip file
        subprocess.run(f"echo 'Valid data' | gzip > {valid_gz_path}", shell=True, check=True)

        with open(valid_gz_path, "rb") as f:
            valid_gz_data = f.read()
            valid_hash = hashlib.sha256(valid_gz_data).hexdigest()

        # Create invalid file
        invalid_path = "/home/user/docs/bad_doc.gz"
        with open(invalid_path, "w") as f:
            f.write("Not a gzip file\n")

        time.sleep(3) # Wait for watcher and C program to process

        # Read manifest
        with open("/home/user/manifest.txt", "r") as f:
            manifest_content = f.read()

        expected_valid_line = f"valid_doc.gz {valid_hash} VALID"
        expected_invalid_line = "bad_doc.gz INVALID"

        assert expected_valid_line in manifest_content, f"Expected valid line '{expected_valid_line}' not found in manifest."
        assert expected_invalid_line in manifest_content, f"Expected invalid line '{expected_invalid_line}' not found in manifest."

    finally:
        watcher.terminate()
        watcher.wait()