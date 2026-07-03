# test_final_state.py

import os
import subprocess

def test_bad_commit_hash_identified():
    expected_path = "/tmp/expected_bad_commit.txt"
    actual_path = "/home/user/bad_commit.txt"

    assert os.path.exists(expected_path), f"Truth file {expected_path} is missing."
    assert os.path.exists(actual_path), f"Student file {actual_path} is missing."

    with open(expected_path, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_path, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Incorrect bad commit hash. Expected {expected_hash}, got {actual_hash}."

def test_output_file_contents():
    output_path = "/home/user/output.txt"
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        output = f.read()

    expected_lines = [
        "Window avg ending at index 1: 50",
        "Window avg ending at index 4: 150"
    ]

    for line in expected_lines:
        assert line in output, f"Expected output line '{line}' not found in {output_path}.\nActual output:\n{output}"

def test_rust_code_compiles_and_runs_without_panic():
    repo_path = "/home/user/flow-analyzer"
    pcap_path = "/home/user/trace.pcap"

    # Ensure the code compiles
    build_result = subprocess.run(["cargo", "build"], cwd=repo_path, capture_output=True, text=True)
    assert build_result.returncode == 0, f"Rust project failed to compile:\n{build_result.stderr}"

    # Ensure it runs without panic
    run_result = subprocess.run(["cargo", "run", "--", pcap_path], cwd=repo_path, capture_output=True, text=True)
    assert run_result.returncode == 0, f"Rust project panicked or failed to run:\n{run_result.stderr}"

    # Check that it produces the correct output
    assert "Window avg ending at index 1: 50" in run_result.stdout, "Fixed program did not output correct average for index 1."
    assert "Window avg ending at index 4: 150" in run_result.stdout, "Fixed program did not output correct average for index 4."