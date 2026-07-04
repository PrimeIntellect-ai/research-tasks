# test_final_state.py

import os
import base64
import pytest

def test_encoder_script_exists_and_uses_flock():
    script_path = "/home/user/encoder.py"
    assert os.path.isfile(script_path), f"The file {script_path} does not exist."
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "fcntl.flock" in content, f"The script {script_path} does not seem to use fcntl.flock."

def test_process_docs_script_exists():
    script_path = "/home/user/process_docs.sh"
    assert os.path.isfile(script_path), f"The file {script_path} does not exist."

def test_compiled_docs_content():
    compiled_path = "/home/user/compiled_docs.txt"
    assert os.path.isfile(compiled_path), f"The file {compiled_path} does not exist."

    # Recompute the expected concatenated utf-8 text
    docs_dir = "/home/user/docs"
    expected_text = ""
    if os.path.isdir(docs_dir):
        files = sorted([f for f in os.listdir(docs_dir) if f.endswith(".txt")])
        for file in files:
            with open(os.path.join(docs_dir, file), "rb") as f:
                content = f.read()
                expected_text += content.decode("windows-1252")

    with open(compiled_path, "r", encoding="utf-8") as f:
        actual_text = f.read()

    assert actual_text == expected_text, "The content of compiled_docs.txt does not match the expected concatenated UTF-8 text."

def test_compressed_archive_content():
    archive_path = "/home/user/compressed_archive.b64"
    assert os.path.isfile(archive_path), f"The file {archive_path} does not exist."

    # Recompute the expected base64 output
    docs_dir = "/home/user/docs"
    expected_lines = []
    if os.path.isdir(docs_dir):
        files = sorted([f for f in os.listdir(docs_dir) if f.endswith(".txt")])
        for file in files:
            with open(os.path.join(docs_dir, file), "rb") as f:
                content = f.read()
                utf8_text = content.decode("windows-1252")
                reversed_text = utf8_text[::-1]
                b64_encoded = base64.b64encode(reversed_text.encode("utf-8")).decode("ascii")
                expected_lines.append(b64_encoded)

    expected_output = "\n".join(expected_lines) + "\n"

    with open(archive_path, "r", encoding="utf-8") as f:
        actual_output = f.read()

    # Allow missing trailing newline in actual output
    assert actual_output.strip() == expected_output.strip(), "The content of compressed_archive.b64 does not match the expected base64 output."