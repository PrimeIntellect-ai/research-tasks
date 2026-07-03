# test_final_state.py

import os
import tarfile
import csv

def test_integrity_txt():
    """Verify that integrity.txt exists and contains evidence of a successful zip test."""
    path = "/home/user/integrity.txt"
    assert os.path.exists(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read().lower()
    # unzip -t usually outputs "no errors detected" or "ok"
    assert "no errors" in content or "ok" in content, "integrity.txt does not seem to contain successful zip test output."

def test_raw_docs_extracted():
    """Verify that the archive was extracted to /home/user/raw_docs/."""
    path = "/home/user/raw_docs/system.log"
    assert os.path.exists(path), f"{path} does not exist. Archive might not be extracted correctly."

def test_errors_csv():
    """Verify the contents of errors.csv."""
    path = "/home/user/errors.csv"
    assert os.path.exists(path), f"{path} does not exist."

    expected_rows = [
        ["Timestamp", "Message"],
        ["2023-10-01 10:05:23", "Failed to connect to database. Connection timeout on port 5432. Retrying in 5 seconds..."],
        ["2023-10-01 10:12:45", "NullPointerException caught in MainModule. Stack trace:   at MainModule.run(MainModule.java:45)   at Application.main(Application.java:20)"]
    ]

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in errors.csv, found {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected: {expected}, Actual: {actual}"

def test_final_docs_tar_gz():
    """Verify that final_docs.tar.gz exists and contains the correct files."""
    path = "/home/user/final_docs.tar.gz"
    assert os.path.exists(path), f"{path} does not exist."
    assert tarfile.is_tarfile(path), f"{path} is not a valid tar archive."

    with tarfile.open(path, "r:gz") as tar:
        members = tar.getnames()

    # Paths should be relative to /home/user/
    expected_files = {
        "errors.csv",
        "raw_docs/notes/2023/meeting_notes.md",
        "raw_docs/drafts/api_v2.md"
    }

    # Check that all expected files are in the tarball
    for expected in expected_files:
        # Sometimes paths in tar might have a leading './'
        found = any(m == expected or m == f"./{expected}" for m in members)
        assert found, f"Expected file {expected} not found in {path}."

    # Check that no absolute paths were included
    for member in members:
        assert not member.startswith("/"), f"Absolute path found in tarball: {member}"