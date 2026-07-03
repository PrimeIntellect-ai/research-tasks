# test_final_state.py
import os
import subprocess
import pytest

def test_bad_commit_hash():
    actual_path = "/home/user/bad_commit.txt"
    expected_path = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(actual_path), f"File {actual_path} does not exist."
    assert os.path.isfile(expected_path), f"Expected truth file {expected_path} is missing."

    with open(expected_path, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_path, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The commit hash in {actual_path} is incorrect. Expected {expected_hash}, got {actual_hash}."

def test_rust_fix_and_execution():
    project_dir = "/home/user/packet-parser"
    pcap_file = "/home/user/capture.pcap"

    assert os.path.isdir(project_dir), f"Project directory {project_dir} is missing."
    assert os.path.isfile(os.path.join(project_dir, "Cargo.toml")), "Cargo.toml is missing."
    assert os.path.isfile(pcap_file), f"PCAP file {pcap_file} is missing."

    # Run the program with a timeout to catch the infinite loop
    try:
        result = subprocess.run(
            ["cargo", "run", "--", pcap_file],
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The Rust program timed out. The infinite loop/hang bug is likely still present.")

    assert result.returncode == 0, f"The program failed to run successfully.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert "Processed" in result.stdout, "The program did not output the expected 'Processed ... blocks' message."