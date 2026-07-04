# test_final_state.py

import os
import gzip

def test_service_b_untouched():
    """Verify that serviceB.log, which is <= 10,000 lines, was not modified."""
    file_path = "/home/user/logs/serviceB.log"
    assert os.path.isfile(file_path), f"Expected {file_path} to exist."
    with open(file_path, "r") as f:
        lines = f.readlines()
    assert len(lines) == 8000, f"serviceB.log should have exactly 8000 lines, found {len(lines)}."
    assert "### LOG ROTATED ###" not in lines[0], "serviceB.log should not have a rotation header."

def test_service_a_rotated():
    """Verify that serviceA.log was rotated correctly."""
    file_path = "/home/user/logs/serviceA.log"
    assert os.path.isfile(file_path), f"Expected {file_path} to exist."
    with open(file_path, "r") as f:
        lines = f.readlines()

    assert len(lines) == 1001, f"serviceA.log should have exactly 1001 lines, found {len(lines)}."
    assert lines[0] == "### LOG ROTATED ###\n", "The first line of serviceA.log must be the exact header."
    assert "Line 14001" in lines[1], "The second line of serviceA.log should be the 14001st line from the original file."
    assert "Line 15000" in lines[-1], "The last line of serviceA.log should be the 15000th line from the original file."

def test_service_c_rotated():
    """Verify that serviceC.log was rotated correctly."""
    file_path = "/home/user/logs/serviceC.log"
    assert os.path.isfile(file_path), f"Expected {file_path} to exist."
    with open(file_path, "r") as f:
        lines = f.readlines()

    assert len(lines) == 1001, f"serviceC.log should have exactly 1001 lines, found {len(lines)}."
    assert lines[0] == "### LOG ROTATED ###\n", "The first line of serviceC.log must be the exact header."
    assert "Line 24001" in lines[1], "The second line of serviceC.log should be the 24001st line from the original file."
    assert "Line 25000" in lines[-1], "The last line of serviceC.log should be the 25000th line from the original file."

def test_service_a_archive():
    """Verify that serviceA.log.gz was created correctly."""
    archive_path = "/home/user/archive/serviceA.log.gz"
    assert os.path.isfile(archive_path), f"Expected archive {archive_path} to exist."

    with gzip.open(archive_path, "rt") as f:
        archived_lines = f.readlines()

    assert len(archived_lines) == 11200, f"Expected 11200 lines in serviceA.log archive, found {len(archived_lines)}."

    has_ignore = any("[IGNORE]" in line for line in archived_lines)
    assert not has_ignore, "Archive for serviceA.log must not contain any lines with '[IGNORE]'."

def test_service_c_archive():
    """Verify that serviceC.log.gz was created correctly."""
    archive_path = "/home/user/archive/serviceC.log.gz"
    assert os.path.isfile(archive_path), f"Expected archive {archive_path} to exist."

    with gzip.open(archive_path, "rt") as f:
        archived_lines = f.readlines()

    assert len(archived_lines) == 21600, f"Expected 21600 lines in serviceC.log archive, found {len(archived_lines)}."

    has_ignore = any("[IGNORE]" in line for line in archived_lines)
    assert not has_ignore, "Archive for serviceC.log must not contain any lines with '[IGNORE]'."

def test_summary_report():
    """Verify that the summary report was generated correctly."""
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"Expected {summary_path} to exist."

    with open(summary_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == 2, f"Expected exactly 2 lines in summary.txt, found {len(content)}."
    assert content[0] == "serviceA.log: 11200", f"Expected 'serviceA.log: 11200', got {content[0]}."
    assert content[1] == "serviceC.log: 21600", f"Expected 'serviceC.log: 21600', got {content[1]}."