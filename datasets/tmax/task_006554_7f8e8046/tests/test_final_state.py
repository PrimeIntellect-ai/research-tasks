# test_final_state.py

import os
import json

def test_api_mocks_and_baseline_exist():
    """Verify the api_mocks directory, its files, and the baseline file exist with correct contents."""
    mocks_dir = "/home/user/api_mocks"
    assert os.path.isdir(mocks_dir), f"Directory {mocks_dir} does not exist."

    expected_payloads = {
        "payload_a.json": {"api_version": "1.2.5", "data": [45, 60, 32]},
        "payload_b.json": {"api_version": "1.4.1", "data": [55, 42, 88]},
        "payload_c.json": {"api_version": "1.5.0", "data": [12, 18]},
        "payload_d.json": {"api_version": "2.0.1", "data": [99, 100, 101]},
        "payload_e.json": {"api_version": "1.9.9", "data": [77, 81]}
    }

    for filename, expected_content in expected_payloads.items():
        filepath = os.path.join(mocks_dir, filename)
        assert os.path.isfile(filepath), f"Mock file {filepath} is missing."
        with open(filepath, 'r') as f:
            content = json.load(f)
        assert content == expected_content, f"Content of {filepath} does not match expected."

    baseline_path = "/home/user/baseline_latencies.txt"
    assert os.path.isfile(baseline_path), f"Baseline file {baseline_path} is missing."
    with open(baseline_path, 'r') as f:
        baseline_content = f.read().strip().split('\n')
    assert baseline_content == ["12", "15", "18", "42", "55", "77", "88"], "Baseline content is incorrect."

def test_rust_project_exists():
    """Verify the Rust project directory and basic files exist."""
    project_dir = "/home/user/latency_analyzer"
    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."
    assert os.path.isfile(os.path.join(project_dir, "Cargo.toml")), "Cargo.toml is missing."
    assert os.path.isfile(os.path.join(project_dir, "src", "main.rs")), "src/main.rs is missing."

def test_merged_latencies_correct():
    """Verify the merged_latencies.txt file has the correct sorted integers."""
    merged_path = "/home/user/merged_latencies.txt"
    assert os.path.isfile(merged_path), f"Merged latencies file {merged_path} is missing."

    with open(merged_path, 'r') as f:
        lines = f.read().strip().split('\n')

    expected_lines = ["12", "18", "42", "55", "77", "81", "88"]
    assert lines == expected_lines, f"Content of {merged_path} is incorrect. Expected {expected_lines}, got {lines}."

def test_latency_diff_patch_correct():
    """Verify the latency_diff.patch file exists and contains the correct diff."""
    patch_path = "/home/user/latency_diff.patch"
    assert os.path.isfile(patch_path), f"Diff patch file {patch_path} is missing."

    with open(patch_path, 'r') as f:
        patch_content = f.read()

    # Check for unified diff headers
    assert "--- /home/user/baseline_latencies.txt" in patch_content, "Patch missing baseline file header."
    assert "+++ /home/user/merged_latencies.txt" in patch_content, "Patch missing merged file header."

    # Check for specific additions and deletions
    lines = patch_content.split('\n')
    assert "-15" in lines, "Patch is missing the removed line '-15'."
    assert "+81" in lines, "Patch is missing the added line '+81'."