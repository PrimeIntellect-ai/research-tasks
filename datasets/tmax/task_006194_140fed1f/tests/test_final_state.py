# test_final_state.py
import os
import subprocess
import sqlite3

WORKDIR = "/home/user/dataport"
MAKEFILE_PATH = os.path.join(WORKDIR, "Makefile")
PROCESSOR_STATIC_PATH = os.path.join(WORKDIR, "processor_static")
LOG_PATH = os.path.join(WORKDIR, "minimal_run.log")
DB_PATH = os.path.join(WORKDIR, "data.db")

def test_makefile_exists_and_targets():
    """Verify Makefile exists and has default and minimal targets."""
    assert os.path.exists(MAKEFILE_PATH), f"{MAKEFILE_PATH} does not exist."
    with open(MAKEFILE_PATH, "r") as f:
        content = f.read()
    assert "default:" in content or "default :" in content or ".PHONY: default" in content or "all:" in content, "Makefile missing 'default' target."
    assert "minimal:" in content or "minimal :" in content, "Makefile missing 'minimal' target."

def test_processor_static_exists_and_statically_linked():
    """Verify processor_static exists and is a statically linked ELF file."""
    assert os.path.exists(PROCESSOR_STATIC_PATH), f"{PROCESSOR_STATIC_PATH} does not exist."

    # Check if it's statically linked using the `file` command
    result = subprocess.run(["file", PROCESSOR_STATIC_PATH], capture_output=True, text=True)
    assert "statically linked" in result.stdout, f"{PROCESSOR_STATIC_PATH} is not statically linked."

def test_minimal_run_log():
    """Verify minimal_run.log exists and contains the exact string."""
    assert os.path.exists(LOG_PATH), f"{LOG_PATH} does not exist."
    with open(LOG_PATH, "r") as f:
        content = f.read().strip()
    assert "Processed 1000 records." in content, f"Log file does not contain expected output. Found: {content}"

def test_database_updated():
    """Verify the database was updated with the new column and correct values."""
    assert os.path.exists(DB_PATH), f"{DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if column exists
    cursor.execute("PRAGMA table_info(records);")
    columns = [row[1] for row in cursor.fetchall()]
    assert "processed_value" in columns, "Column 'processed_value' was not added to 'records' table."

    # Check the updated values
    cursor.execute("SELECT count(*) FROM records WHERE processed_value = value || '_processed';")
    count = cursor.fetchone()[0]
    assert count == 1000, f"Expected 1000 updated records, but found {count}."

    conn.close()