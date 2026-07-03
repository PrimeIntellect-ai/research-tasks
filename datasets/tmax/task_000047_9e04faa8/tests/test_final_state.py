# test_final_state.py
import os
import pytest

def test_safe_files_extracted():
    expected_files = {
        "/home/user/extracted/data/sensor1.csv": b"timestamp,value\n1,10.5",
        "/home/user/extracted/data/sensor2.csv": b"timestamp,value\n1,20.1",
        "/home/user/extracted/notes.txt": b"experiment notes",
        "/home/user/extracted/nested/safe.txt": b"safe content"
    }

    for path, expected_content in expected_files.items():
        assert os.path.exists(path), f"Safe file {path} was not extracted."
        assert os.path.isfile(path), f"{path} is not a file."
        with open(path, "rb") as f:
            content = f.read()
        assert content == expected_content, f"Content of {path} does not match expected."

def test_malicious_files_not_extracted():
    malicious_paths = [
        "/home/user/overwritten_secret.txt",
        "/home/user/etc/shadow",
        "/home/user/extracted/../overwritten_secret.txt",
        "/home/user/extracted/data/../../etc/shadow"
    ]

    for path in malicious_paths:
        normalized_path = os.path.normpath(path)
        assert not os.path.exists(normalized_path), f"Malicious file was extracted to {normalized_path}"

def test_malicious_log_contents():
    log_path = "/home/user/malicious.log"
    assert os.path.exists(log_path), f"Log file {log_path} was not created."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "../overwritten_secret.txt",
        "data/../../etc/shadow"
    ]

    assert lines == expected_lines, f"Contents of {log_path} do not match the expected malicious paths. Got: {lines}"

def test_no_extra_files_in_extracted():
    expected_paths = {
        "/home/user/extracted/data/sensor1.csv",
        "/home/user/extracted/data/sensor2.csv",
        "/home/user/extracted/notes.txt",
        "/home/user/extracted/nested/safe.txt"
    }

    actual_files = set()
    for root, _, files in os.walk("/home/user/extracted"):
        for file in files:
            actual_files.add(os.path.normpath(os.path.join(root, file)))

    extra_files = actual_files - expected_paths
    assert not extra_files, f"Found unexpected files in /home/user/extracted/: {extra_files}"