# test_final_state.py
import os
import struct
import pytest

def test_timeline_file():
    timeline_path = "/home/user/timeline.txt"
    assert os.path.isfile(timeline_path), f"Timeline file {timeline_path} does not exist."

    with open(timeline_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {timeline_path}, found {len(lines)}."

    expected_lines = [
        "Ingest | 1715049605 | REQ-042",
        "Transform | 1715049607 | REQ-042",
        "Serialize | 1715049609 | REQ-042"
    ]

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} mismatch in timeline.txt. Expected '{expected}', got '{lines[i]}'."

def test_binary_output_file():
    bin_path = "/home/user/data/out_REQ-042.bin"
    assert os.path.isfile(bin_path), f"Output binary file {bin_path} does not exist. Did you run the fixed script on the failing payload?"

    with open(bin_path, "rb") as f:
        data = f.read()

    assert len(data) == 24, f"Binary file should be exactly 24 bytes long, got {len(data)} bytes."

    rec_id, name = struct.unpack('<I20s', data)
    assert rec_id == 42, f"Expected record ID 42, got {rec_id}."

    expected_name = "José".encode('utf-8')
    actual_name = name.rstrip(b'\x00')
    assert actual_name == expected_name, f"Expected name {expected_name} (utf-8 encoded), got {actual_name}."

def test_serializer_script_fixed():
    script_path = "/home/user/app/serializer.py"
    assert os.path.isfile(script_path), f"App file {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert ".encode('ascii')" not in content, "The script still contains the buggy .encode('ascii')."
    assert "utf-8" in content.lower() or "utf8" in content.lower(), "The script does not seem to use utf-8 encoding as requested."