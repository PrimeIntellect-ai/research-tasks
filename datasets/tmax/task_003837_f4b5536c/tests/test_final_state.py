# test_final_state.py
import os

def test_restored_hello_txt():
    path = "/home/user/storage_task/restored/hello.txt"
    assert os.path.isfile(path), f"Restored file {path} does not exist"
    with open(path, "rb") as f:
        content = f.read()
    assert content == b"Hello World!", f"Expected 'Hello World!' in {path}, got {content}"

def test_restored_info_bin():
    path = "/home/user/storage_task/restored/data/info.bin"
    assert os.path.isfile(path), f"Restored file {path} does not exist"
    with open(path, "rb") as f:
        content = f.read()
    assert content == b"Data file content", f"Expected 'Data file content' in {path}, got {content}"

def test_rejected_log():
    path = "/home/user/storage_task/rejected.log"
    assert os.path.isfile(path), f"Rejected log file {path} does not exist"
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_rejections = [
        "../escaped.txt",
        "/etc/fake_passwd",
        "data/../../root.txt"
    ]

    assert len(lines) == len(expected_rejections), f"Expected {len(expected_rejections)} rejected entries, got {len(lines)}"

    for expected in expected_rejections:
        assert expected in lines, f"Expected rejected path '{expected}' not found in {path}"

def test_no_escaped_files():
    # Verify that the malicious files were not actually written outside the restored directory
    escaped_paths = [
        "/home/user/storage_task/escaped.txt",
        "/etc/fake_passwd",
        "/home/user/root.txt"
    ]
    for path in escaped_paths:
        assert not os.path.exists(path), f"Malicious file was written to {path} despite security checks"