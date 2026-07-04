# test_final_state.py

import os
import sqlite3
import subprocess
import stat
import pytest

def test_sanitizer_c_fixed():
    c_file_path = "/home/user/project/sanitizer.c"
    assert os.path.isfile(c_file_path), f"File {c_file_path} does not exist."
    with open(c_file_path, 'r') as f:
        content = f.read()
    assert "stdio.h" in content, "sanitizer.c does not include stdio.h"
    assert "string.h" in content, "sanitizer.c does not include string.h"

def test_sanitizer_executable():
    exe_path = "/home/user/project/sanitizer"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did the build succeed?"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

    # Test the sanitizer behavior
    result = subprocess.run([exe_path, "a<b>c"], capture_output=True, text=True)
    assert result.stdout.strip() == "a_b_c", "sanitizer did not correctly replace '<' and '>'"

def test_database_schema_migrated():
    db_path = "/home/user/logs.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(access_logs);")
    columns = cursor.fetchall()

    column_names = [col[1] for col in columns]
    assert "threat_level" in column_names, "Column 'threat_level' was not added to access_logs."

    # Check default value and type
    for col in columns:
        if col[1] == "threat_level":
            assert col[2].upper() == "INTEGER", "threat_level column is not of type INTEGER."
            assert str(col[4]) == "0", "threat_level column does not have DEFAULT 0."

    conn.close()

def test_scripts_are_executable():
    scripts = [
        "/home/user/project/migrate.sh",
        "/home/user/project/fuzz.sh",
        "/home/user/project/ci_pipeline.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        st = os.stat(script)
        assert bool(st.st_mode & stat.S_IXUSR), f"Script {script} is not executable."

def test_ci_success_file_exists():
    success_file = "/home/user/project/ci_success"
    assert os.path.isfile(success_file), f"CI success file {success_file} was not created. Did the pipeline complete successfully?"

def test_fuzzing_results():
    results_file = "/home/user/project/test_results.txt"
    assert os.path.isfile(results_file), f"Test results file {results_file} does not exist."
    with open(results_file, 'r') as f:
        content = f.read()
    assert "FUZZING_PASSED" in content, f"{results_file} does not contain 'FUZZING_PASSED'."