# test_final_state.py
import os
import re
import subprocess
import pytest

def test_cargo_check_success():
    repo_path = "/home/user/pipeline_repo"
    assert os.path.isdir(repo_path), f"Repository directory {repo_path} is missing."

    result = subprocess.run(
        ["cargo", "check"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo check failed with output:\n{result.stderr}"

def test_crash_timestamp():
    dump_path = "/home/user/crash_dump.bin"
    assert os.path.isfile(dump_path), f"File {dump_path} is missing."

    with open(dump_path, "rb") as f:
        content = f.read()

    # Extract the true timestamp dynamically from the dump
    match = re.search(rb'{"timestamp":\s*"([^"]+)"', content)
    assert match is not None, "Could not find timestamp pattern in crash_dump.bin"
    expected_ts = match.group(1).decode('utf-8')

    ts_file = "/home/user/crash_timestamp.txt"
    assert os.path.isfile(ts_file), f"File {ts_file} is missing."

    with open(ts_file, "r") as f:
        actual_ts = f.read().strip()

    assert actual_ts == expected_ts, f"Expected timestamp '{expected_ts}', but got '{actual_ts}'"

def test_source_ip():
    ip_file = "/home/user/source_ip.txt"
    assert os.path.isfile(ip_file), f"File {ip_file} is missing."

    with open(ip_file, "r") as f:
        actual_ip = f.read().strip()

    expected_ip = "192.168.1.105"
    assert actual_ip == expected_ip, f"Expected Source IP '{expected_ip}', but got '{actual_ip}'"

def test_bad_commit():
    expected_file = "/tmp/expected_bad_commit.txt"
    assert os.path.isfile(expected_file), f"Truth file {expected_file} is missing."

    with open(expected_file, "r") as f:
        expected_commit = f.read().strip()

    bad_commit_file = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_file), f"File {bad_commit_file} is missing."

    with open(bad_commit_file, "r") as f:
        actual_commit = f.read().strip()

    assert actual_commit == expected_commit, f"Expected bad commit '{expected_commit}', but got '{actual_commit}'"