# test_final_state.py

import os
import json
import tarfile
import tempfile

def test_transform_script_exists():
    """Check if the transform script was created."""
    assert os.path.isfile("/home/user/transform.py"), "/home/user/transform.py is missing."

def test_final_logs_archive_exists():
    """Check if the final tar.gz archive exists."""
    assert os.path.isfile("/home/user/final_logs.tar.gz"), "/home/user/final_logs.tar.gz is missing."

def test_final_logs_contents():
    """Check the contents of the final tar.gz archive."""
    archive_path = "/home/user/final_logs.tar.gz"
    assert os.path.isfile(archive_path), "Archive missing"

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()
        # Should contain exactly consolidated.jsonl at the root
        file_names = [m.name for m in members if m.isfile()]
        assert "consolidated.jsonl" in file_names, "consolidated.jsonl not found in the archive."

        # Extract and verify the contents
        f = tar.extractfile("consolidated.jsonl")
        assert f is not None, "Could not extract consolidated.jsonl from archive."

        lines = f.read().decode("utf-8").strip().split("\n")

        parsed_lines = []
        for line in lines:
            if not line.strip():
                continue
            try:
                parsed_lines.append(json.loads(line))
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON line found: {line}")

    expected_logs = [
        {"timestamp": "2023-10-01 12:00:00", "severity": "ERROR", "message": "Disk full"},
        {"timestamp": "2023-10-01 12:05:00", "severity": "INFO", "message": "Cleanup started"},
        {"timestamp": "2023-10-01 12:10:00", "severity": "WARN", "message": "High memory usage"},
        {"timestamp": "2023-10-01 12:15:00", "severity": "INFO", "message": "Process killed"}
    ]

    assert len(parsed_lines) == len(expected_logs), f"Expected {len(expected_logs)} log entries, found {len(parsed_lines)}."

    # Order might vary depending on concatenation order, so check independently of order
    for expected in expected_logs:
        assert expected in parsed_lines, f"Expected log entry not found in output: {expected}"