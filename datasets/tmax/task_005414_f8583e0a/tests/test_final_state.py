# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/restore/base"
INCR_DIR = "/home/user/restore/incr"
LATEST_DIR = "/home/user/restore/latest"
REPORT_FILE = "/home/user/resolution_report.txt"

def test_directories_exist():
    """Check if the required directories exist."""
    assert os.path.isdir(BASE_DIR), f"Directory {BASE_DIR} is missing."
    assert os.path.isdir(INCR_DIR), f"Directory {INCR_DIR} is missing."
    assert os.path.isdir(LATEST_DIR), f"Directory {LATEST_DIR} is missing."

def test_extracted_files_exist():
    """Check if the files are extracted correctly."""
    assert os.path.isfile(os.path.join(BASE_DIR, "fileA.txt")), "fileA.txt missing in base/"
    assert os.path.isfile(os.path.join(BASE_DIR, "fileB.txt")), "fileB.txt missing in base/"
    assert os.path.isfile(os.path.join(BASE_DIR, "config.ini")), "config.ini missing in base/"

    assert os.path.isfile(os.path.join(INCR_DIR, "fileB.txt")), "fileB.txt missing in incr/"
    assert os.path.isfile(os.path.join(INCR_DIR, "config.ini")), "config.ini missing in incr/"
    assert os.path.isfile(os.path.join(INCR_DIR, "fileC.txt")), "fileC.txt missing in incr/"

def test_hard_links_created():
    """Check if identical files are hard linked."""
    base_fileB = os.path.join(BASE_DIR, "fileB.txt")
    incr_fileB = os.path.join(INCR_DIR, "fileB.txt")

    assert os.path.exists(base_fileB), f"{base_fileB} does not exist."
    assert os.path.exists(incr_fileB), f"{incr_fileB} does not exist."

    stat_base = os.stat(base_fileB)
    stat_incr = os.stat(incr_fileB)

    assert stat_base.st_ino == stat_incr.st_ino, f"{incr_fileB} is not a hard link to {base_fileB}."

def test_symlinks_created():
    """Check if symlinks in latest/ point to the correct files."""
    expected_links = {
        "config.ini": os.path.join(INCR_DIR, "config.ini"),
        "fileA.txt": os.path.join(BASE_DIR, "fileA.txt"),
        "fileB.txt": os.path.join(INCR_DIR, "fileB.txt"),
        "fileC.txt": os.path.join(INCR_DIR, "fileC.txt"),
    }

    for filename, expected_target in expected_links.items():
        link_path = os.path.join(LATEST_DIR, filename)
        assert os.path.islink(link_path), f"{link_path} is not a symbolic link."

        # Resolve the symlink to its absolute path
        resolved_target = os.path.realpath(link_path)
        assert resolved_target == expected_target, f"Symlink {link_path} points to {resolved_target}, expected {expected_target}."

def test_resolution_report():
    """Check if the resolution report contains the correct absolute paths."""
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} is missing."

    expected_lines = [
        os.path.join(INCR_DIR, "config.ini"),
        os.path.join(BASE_DIR, "fileA.txt"),
        os.path.join(INCR_DIR, "fileB.txt"),
        os.path.join(INCR_DIR, "fileC.txt")
    ]

    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"Report contents are incorrect. Expected {expected_lines}, got {lines}."