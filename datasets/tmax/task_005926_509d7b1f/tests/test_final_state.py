# test_final_state.py

import os
import pytest

def test_extracted_files_exist():
    extracted_dir = "/home/user/organizer/extracted"
    expected_files = ["log_1.json", "log_2.json", "log_3.json"]

    for f in expected_files:
        file_path = os.path.join(extracted_dir, f)
        assert os.path.isfile(file_path), f"Expected extracted file {file_path} does not exist."

def test_go_source_exists_and_contains_mechanics():
    go_file = "/home/user/organizer/process.go"
    assert os.path.isfile(go_file), f"Expected Go source file {go_file} does not exist."

    with open(go_file, "r") as f:
        content = f.read()

    assert "Flock" in content, "The Go program does not appear to use file locking (e.g., syscall.Flock)."
    assert "Rename" in content, "The Go program does not appear to use atomic rename (e.g., os.Rename)."

def test_summary_csv_content():
    csv_file = "/home/user/organizer/output/summary.csv"
    assert os.path.isfile(csv_file), f"Expected output file {csv_file} does not exist."

    expected_content = "id,action,user\n1,commit,alice\n2,build,bob\n3,push,charlie\n"

    with open(csv_file, "r") as f:
        actual_content = f.read()

    # Strip trailing newlines for comparison
    assert actual_content.strip() == expected_content.strip(), (
        f"Content of {csv_file} does not match expected output.\n"
        f"Expected:\n{expected_content.strip()}\n"
        f"Actual:\n{actual_content.strip()}"
    )