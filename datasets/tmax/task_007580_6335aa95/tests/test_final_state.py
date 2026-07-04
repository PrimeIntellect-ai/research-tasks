# test_final_state.py
import os
import sqlite3
import subprocess

def test_source_file_exists():
    assert os.path.isfile("/home/user/process_audit.c"), "The C source file /home/user/process_audit.c is missing."

def test_executable_exists():
    assert os.path.isfile("/home/user/process_audit"), "The compiled executable /home/user/process_audit is missing."
    assert os.access("/home/user/process_audit", os.X_OK), "/home/user/process_audit is not executable."

def test_index_created():
    db_path = "/home/user/audit.db"
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    # Run the program to ensure the index gets created (in case it wasn't run yet)
    subprocess.run(["/home/user/process_audit", "1", "0"], capture_output=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND name='idx_audit_aid';")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 1, "The index 'idx_audit_aid' was not created in the database."

def test_program_output_1():
    result = subprocess.run(["/home/user/process_audit", "2", "0"], capture_output=True, text=True)
    assert result.returncode == 0, "The program /home/user/process_audit returned a non-zero exit code."

    expected_output = "bob,PublicWeb,InternalPortal,2023-10-01 10:20:00\ncharlie,InternalPortal,CustomerDB,2023-10-01 10:10:00\n"
    actual_output = result.stdout.replace('\r\n', '\n')

    assert actual_output.strip() == expected_output.strip(), f"Output mismatch for limit 2, offset 0.\nExpected:\n{expected_output}\nGot:\n{actual_output}"

def test_program_output_2():
    result = subprocess.run(["/home/user/process_audit", "10", "2"], capture_output=True, text=True)
    assert result.returncode == 0, "The program /home/user/process_audit returned a non-zero exit code."

    expected_output = "bob,InternalPortal,CustomerDB,2023-10-01 10:05:00\nalice,PublicWeb,InternalPortal,2023-10-01 10:00:00\n"
    actual_output = result.stdout.replace('\r\n', '\n')

    assert actual_output.strip() == expected_output.strip(), f"Output mismatch for limit 10, offset 2.\nExpected:\n{expected_output}\nGot:\n{actual_output}"