# test_final_state.py
import os
import csv
import re

def test_organizer_script_exists():
    """Check that the organizer.py script exists."""
    assert os.path.exists("/home/user/organizer.py"), "The script /home/user/organizer.py does not exist."

def test_incoming_files_deleted():
    """Check that the original files in the incoming directory were deleted after processing."""
    assert not os.path.exists("/home/user/incoming/test1.json"), "The file test1.json was not deleted from /home/user/incoming/."
    assert not os.path.exists("/home/user/incoming/test2.log"), "The file test2.log was not deleted from /home/user/incoming/."

def test_json_processed_output():
    """Check that the JSON file was processed correctly into a CSV."""
    output_path = "/home/user/processed/test1.json.processed.csv"
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row] # Ignore empty lines

    assert len(rows) >= 3, "JSON CSV output does not have the expected number of rows."
    assert rows[0] == ["id", "status"], f"Expected headers ['id', 'status'], got {rows[0]}"
    assert rows[1] == ["1", "active"], f"Expected row 1 ['1', 'active'], got {rows[1]}"
    assert rows[2] == ["2", "inactive"], f"Expected row 2 ['2', 'inactive'], got {rows[2]}"

def test_log_processed_output():
    """Check that the log file was processed correctly into a CSV."""
    output_path = "/home/user/processed/test2.log.processed.csv"
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row] # Ignore empty lines

    assert len(rows) >= 3, "Log CSV output does not have the expected number of rows."
    assert rows[0] == ["timestamp", "level", "message"], f"Expected headers ['timestamp', 'level', 'message'], got {rows[0]}"
    assert rows[1] == ["2023-10-01 10:00:00", "ERROR", "Database connection failed. Retrying in 5 seconds."], f"Expected row 1 to match log entry 1, got {rows[1]}"
    assert rows[2] == ["2023-10-01 10:00:05", "INFO", "Connection established."], f"Expected row 2 to match log entry 2, got {rows[2]}"

def test_atomic_write_implementation():
    """Check the script source code for atomic write patterns (temp file + rename)."""
    script_path = "/home/user/organizer.py"
    assert os.path.exists(script_path), "Script /home/user/organizer.py is missing."

    with open(script_path, "r") as f:
        code = f.read()

    # Check for temporary file usage
    has_temp = bool(re.search(r'(\.tmp|NamedTemporaryFile|temp)', code, re.IGNORECASE))
    assert has_temp, "No temporary file usage detected in organizer.py for atomic writes."

    # Check for atomic rename
    has_rename = bool(re.search(r'(os\.rename|shutil\.move|os\.replace|Path\.rename)', code))
    assert has_rename, "No atomic rename (e.g., os.rename, shutil.move, os.replace) detected in organizer.py."