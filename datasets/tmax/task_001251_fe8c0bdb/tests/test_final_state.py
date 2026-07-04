# test_final_state.py

import os
import requests
import pytest
import time

def test_extracted_files_exist():
    extracted_dir = "/home/user/data/extracted"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist. Did you extract the archive?"

    file1 = os.path.join(extracted_dir, "intro.md")
    file2 = os.path.join(extracted_dir, "advanced/io.md")

    assert os.path.isfile(file1), f"File {file1} not found. Archive extraction might have failed."
    assert os.path.isfile(file2), f"File {file2} not found. Archive extraction might have failed."

def test_symlinks_created():
    docs_dir = "/home/user/www/docs"
    assert os.path.isdir(docs_dir), f"Directory {docs_dir} does not exist."

    symlink1 = os.path.join(docs_dir, "101.txt")
    symlink2 = os.path.join(docs_dir, "102.txt")

    assert os.path.islink(symlink1), f"{symlink1} is not a symlink."
    assert os.path.islink(symlink2), f"{symlink2} is not a symlink."

    target1 = os.readlink(symlink1)
    target2 = os.readlink(symlink2)

    assert target1 == "/home/user/data/extracted/intro.md", f"Symlink {symlink1} points to {target1}, expected /home/user/data/extracted/intro.md"
    assert target2 == "/home/user/data/extracted/advanced/io.md", f"Symlink {symlink2} points to {target2}, expected /home/user/data/extracted/advanced/io.md"

def test_server_binary_compiled():
    binary_path = "/app/docserve-1.0/server"
    assert os.path.isfile(binary_path), f"Compiled server binary not found at {binary_path}. Did you fix the Makefile and run make?"
    assert os.access(binary_path, os.X_OK), f"Server binary {binary_path} is not executable."

def test_server_responses():
    base_url = "http://127.0.0.1:8080"

    # Check 101.txt
    try:
        resp1 = requests.get(f"{base_url}/docs/101.txt", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {base_url}/docs/101.txt. Is the server running? Error: {e}")

    assert resp1.status_code == 200, f"Expected status code 200 for /docs/101.txt, got {resp1.status_code}"
    assert "Introduction to Data Parsing" in resp1.text, f"Unexpected body for /docs/101.txt: {resp1.text}"

    # Check 102.txt
    try:
        resp2 = requests.get(f"{base_url}/docs/102.txt", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {base_url}/docs/102.txt. Is the server running? Error: {e}")

    assert resp2.status_code == 200, f"Expected status code 200 for /docs/102.txt, got {resp2.status_code}"
    assert "Advanced C++ File I/O" in resp2.text, f"Unexpected body for /docs/102.txt: {resp2.text}"