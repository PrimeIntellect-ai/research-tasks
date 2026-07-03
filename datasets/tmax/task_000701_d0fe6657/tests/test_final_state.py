# test_final_state.py

import os
import pytest
import glob

def test_resolved_dependencies():
    resolved_path = "/home/user/project/resolved.txt"
    assert os.path.isfile(resolved_path), f"{resolved_path} does not exist. Did you run build.sh?"

    with open(resolved_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_deps = {"core", "utils", "math", "graphics", "ui", "network_base", "crypto", "network", "app"}
    actual_deps_set = set(lines)

    assert len(lines) == len(actual_deps_set), "resolved.txt contains duplicate entries. Dependencies should only be processed once."
    assert actual_deps_set == expected_deps, f"resolved.txt does not contain the correct set of dependencies. Expected {expected_deps}, got {actual_deps_set}"

def test_anomaly_investigation():
    anomaly_path = "/home/user/anomaly.txt"
    assert os.path.isfile(anomaly_path), f"{anomaly_path} does not exist."

    with open(anomaly_path, "r") as f:
        content = f.read().strip()

    assert content == "lib_heavy_crypto", f"anomaly.txt contains incorrect dependency name. Expected 'lib_heavy_crypto', got '{content}'"

def test_log_timeline_reconstruction():
    timeline_path = "/home/user/timeline.txt"
    assert os.path.isfile(timeline_path), f"{timeline_path} does not exist."

    # Read the actual timeline
    with open(timeline_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    # Reconstruct the expected timeline from original logs
    log_dir = "/home/user/project/logs/"
    expected_lines = []

    for log_file in ["worker1.log", "worker2.log", "download.log"]:
        file_path = os.path.join(log_dir, log_file)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                expected_lines.extend([line.strip() for line in f if line.strip()])

    # Sort the expected lines chronologically
    expected_lines.sort()

    assert len(actual_lines) == len(expected_lines), f"timeline.txt does not contain the correct number of lines. Expected {len(expected_lines)}, got {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1} in timeline.txt. Expected '{expected}', got '{actual}'"