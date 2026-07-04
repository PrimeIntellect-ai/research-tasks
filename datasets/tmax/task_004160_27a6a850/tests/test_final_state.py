# test_final_state.py

import os
import zipfile
import pytest

def test_zip_warnings_log():
    """Verify that malicious paths were skipped and logged correctly."""
    log_path = "/home/user/zip_warnings.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_malicious = {
        "../etc/passwd_overwrite",
        "data/../../home/user/.bashrc_override",
        "/absolute/path/test.txt"
    }

    assert set(lines) == expected_malicious, f"Logged warnings do not match expected malicious paths. Found: {lines}"
    assert len(lines) == 3, f"Expected exactly 3 lines in {log_path}, found {len(lines)}"

def test_safe_extraction():
    """Verify that safe files were extracted and malicious files were not."""
    extracted_dir = "/home/user/extracted"
    assert os.path.isdir(extracted_dir), f"{extracted_dir} is missing."

    expected_files = {"scaffold1.gcode", "scaffold2.gcode", "sensor_a.wal", "sensor_b.wal", "sensor_c.wal"}
    extracted_files = set(os.listdir(extracted_dir))

    assert expected_files.issubset(extracted_files), f"Not all safe files were extracted. Found: {extracted_files}"

    # Check that malicious files were NOT extracted to their traversal targets
    assert not os.path.exists("/home/user/etc/passwd_overwrite"), "Malicious file was extracted to /home/user/etc/passwd_overwrite"
    assert not os.path.exists("/etc/passwd_overwrite"), "Malicious file was extracted to /etc/passwd_overwrite"
    assert not os.path.exists("/home/user/.bashrc_override"), "Malicious file was extracted to /home/user/.bashrc_override"
    assert not os.path.exists("/absolute/path/test.txt"), "Malicious file was extracted to /absolute/path/test.txt"

def test_gcode_chunks():
    """Verify that GCode files were cleaned, split, and named correctly."""
    chunks_dir = "/home/user/gcode_chunks"
    assert os.path.isdir(chunks_dir), f"{chunks_dir} is missing."

    chunks = [f for f in os.listdir(chunks_dir) if f.endswith('.gcode')]

    expected_chunks = {
        "scaffold1_part001.gcode": 500,
        "scaffold1_part002.gcode": 500,
        "scaffold1_part003.gcode": 200,
        "scaffold2_part001.gcode": 300
    }

    assert set(chunks) == set(expected_chunks.keys()), f"GCode chunks do not match expected filenames. Found: {chunks}"

    for chunk, expected_lines in expected_chunks.items():
        chunk_path = os.path.join(chunks_dir, chunk)
        with open(chunk_path, "r") as f:
            lines = f.readlines()

        assert len(lines) == expected_lines, f"{chunk} should have {expected_lines} lines, but has {len(lines)}."

        for i, line in enumerate(lines):
            assert ";" not in line, f"Comment found in {chunk} at line {i+1}"
            assert line.strip() != "", f"Empty line found in {chunk} at line {i+1}"

def test_wal_merging():
    """Verify that WAL files were merged in alphabetical order."""
    merged_path = "/home/user/merged_sensors.wal"
    assert os.path.isfile(merged_path), f"{merged_path} is missing."

    zip_path = "/home/user/dataset.zip"
    with zipfile.ZipFile(zip_path, 'r') as zf:
        wal_a = zf.read("sensor_a.wal")
        wal_b = zf.read("sensor_b.wal")
        wal_c = zf.read("sensor_c.wal")

    expected_content = wal_a + wal_b + wal_c
    expected_size = len(expected_content)

    assert os.path.getsize(merged_path) == expected_size, f"Merged WAL file size should be {expected_size} bytes, but is {os.path.getsize(merged_path)}"

    with open(merged_path, "rb") as f:
        actual_content = f.read()

    assert actual_content == expected_content, "Merged WAL content does not match the concatenated original WAL files."

def test_summary_report():
    """Verify that the summary report contains the exact expected text."""
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"{summary_path} is missing."

    with open(summary_path, "r") as f:
        content = f.read().strip()

    expected_content = "Blocked Files: 3\nTotal GCode Lines: 1500\nMerged WAL Size: 3584"
    assert content == expected_content, f"Summary report content is incorrect. Expected:\n{expected_content}\n\nFound:\n{content}"