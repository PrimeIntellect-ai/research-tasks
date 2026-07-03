# test_final_state.py

import os
import pytest

def test_malware_timeline_exists():
    path = "/home/user/malware_timeline.log"
    assert os.path.isfile(path), f"The file {path} does not exist. Did you run the script?"

def test_malware_timeline_contents():
    path = "/home/user/malware_timeline.log"
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Oct 12 10:01:22 testhost suspicious_bin[1234]: Connection to 198.51.100.22 established.",
        "Oct 12 10:01:25 testhost kernel: DROP SRC=203.0.113.5 DST=10.0.0.5"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"

def test_internal_ips_excluded():
    path = "/home/user/malware_timeline.log"
    with open(path, "r") as f:
        content = f.read()

    # Check that logs associated only with internal IPs are not present
    assert "Connection to 10.0.0.8 closed." not in content, "Internal IPs (e.g. 10.0.0.8) should be excluded from the timeline."