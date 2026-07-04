# test_final_state.py

import os
import re

def test_indexes_sql():
    """Verify that indexes.sql exists and contains appropriate CREATE INDEX statements."""
    filepath = "/home/user/indexes.sql"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read().lower()

    assert "create index" in content, "indexes.sql does not contain 'CREATE INDEX'."
    assert "communications" in content, "indexes.sql does not reference the 'communications' table."
    assert "sender_id" in content or "receiver_id" in content, "indexes.sql does not reference sender_id or receiver_id."

def test_c_program_exists():
    """Verify that the C program source file exists."""
    filepath = "/home/user/audit_analyzer.c"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

def test_flagged_contractors_output():
    """Verify the contents of flagged_contractors.txt."""
    filepath = "/home/user/flagged_contractors.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1, f"Expected exactly 1 flagged contractor, found {len(lines)}."
    assert lines[0] == "2,Bob,4,500", f"Unexpected content in flagged_contractors.txt: {lines[0]}"

def test_audit_summary_output():
    """Verify the contents of audit_summary.txt."""
    filepath = "/home/user/audit_summary.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_content = "Total Suspicious Contractors: 1\nMax OutDegree: 4"

    # Normalize line endings and whitespace for comparison
    normalized_content = "\n".join([line.strip() for line in content.splitlines() if line.strip()])

    assert normalized_content == expected_content, f"Unexpected content in audit_summary.txt:\n{content}"