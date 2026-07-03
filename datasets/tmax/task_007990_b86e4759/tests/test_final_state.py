# test_final_state.py

import os
import subprocess
import statistics
import pytest
from scapy.all import rdpcap

def get_bad_commit():
    result = subprocess.run(
        ["git", "-C", "/home/user/sla-monitor", "log", "--format=%H", "--grep=Optimize jitter calculation"],
        capture_output=True, text=True, check=True
    )
    commit = result.stdout.strip()
    if not commit:
        pytest.fail("Could not find the bad commit in git history.")
    return commit

def get_expected_jitter():
    try:
        packets = rdpcap("/home/user/sla-monitor/prod.pcap")
    except Exception as e:
        pytest.fail(f"Could not read prod.pcap: {e}")

    times = [float(p.time) for p in packets]
    intervals = [times[i] - times[i-1] for i in range(1, len(times))]
    return statistics.variance(intervals)

def test_resolution_file_exists():
    assert os.path.exists("/home/user/resolution.txt"), "/home/user/resolution.txt does not exist."

def test_resolution_content():
    with open("/home/user/resolution.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "/home/user/resolution.txt must contain at least two lines."

    expected_commit = get_bad_commit()
    expected_jitter = get_expected_jitter()

    assert lines[0] == expected_commit, f"Line 1 should be the bad commit hash. Expected {expected_commit}, got {lines[0]}."

    try:
        actual_jitter = float(lines[1])
        assert abs(actual_jitter - expected_jitter) < 1e-8, f"Line 2 should be the expected jitter. Expected ~{expected_jitter}, got {actual_jitter}."
    except ValueError:
        pytest.fail("Line 2 in /home/user/resolution.txt is not a valid float.")

def test_final_jitter_file():
    assert os.path.exists("/home/user/final_jitter.txt"), "/home/user/final_jitter.txt does not exist."
    with open("/home/user/final_jitter.txt", "r") as f:
        content = f.read().strip()

    expected_jitter = get_expected_jitter()
    try:
        actual_jitter = float(content)
        assert abs(actual_jitter - expected_jitter) < 1e-8, f"/home/user/final_jitter.txt expected ~{expected_jitter}, got {actual_jitter}."
    except ValueError:
        pytest.fail("/home/user/final_jitter.txt does not contain a valid float.")