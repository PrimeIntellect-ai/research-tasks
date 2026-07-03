# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_vendored_package_fixed():
    makefile_path = "/app/vendor/sqlite_bulk_loader-1.0.0/Makefile"
    load_csv_path = "/app/vendor/sqlite_bulk_loader-1.0.0/load_csv.sh"

    assert os.path.isfile(makefile_path), "Makefile is missing."
    assert os.path.isfile(load_csv_path), "load_csv.sh is missing."

    with open(load_csv_path, "r") as f:
        content = f.read()
    assert "/root/forbidden.db" not in content, "load_csv.sh still contains the forbidden DB_PATH."

    # Check if make install works
    result = subprocess.run(["make", "install"], cwd="/app/vendor/sqlite_bulk_loader-1.0.0", capture_output=True, text=True)
    assert result.returncode == 0, f"make install failed: {result.stderr}"

    # Check if load_csv.sh works
    test_csv = "/tmp/test_load.csv"
    with open(test_csv, "w") as f:
        f.write("2023-10-01T12:00:00Z,999,test,test_msg\n")

    # We pass the file as an argument
    result = subprocess.run(["./load_csv.sh", test_csv], cwd="/app/vendor/sqlite_bulk_loader-1.0.0", capture_output=True, text=True)
    assert result.returncode == 0, f"load_csv.sh failed: {result.stderr}"

    # Check if DB was created
    db_path = "/home/user/metrics.db"
    assert os.path.isfile(db_path), f"Database {db_path} was not created by load_csv.sh."

    # Check if data was inserted
    result = subprocess.run(["sqlite3", db_path, "SELECT * FROM logs WHERE user_id=999;"], capture_output=True, text=True)
    assert "2023-10-01T12:00:00Z|999|test|test_msg" in result.stdout, "Data was not correctly loaded into the database."

def test_sanitizer_executable():
    sanitizer_path = "/home/user/sanitize_logs"
    assert os.path.isfile(sanitizer_path), f"Sanitizer not found at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer at {sanitizer_path} is not executable."

def test_sanitizer_clean_corpus():
    sanitizer_path = "/home/user/sanitize_logs"
    clean_files = glob.glob("/app/corpora/clean/*.jsonl")
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []

    for file_path in clean_files:
        with open(file_path, "r") as f:
            input_data = f.read()

        result = subprocess.run([sanitizer_path], input=input_data, capture_output=True, text=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(file_path))
            continue

        output_lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        input_lines = [line.strip() for line in input_data.strip().split("\n") if line.strip()]

        if len(output_lines) != len(input_lines):
            failed_files.append(os.path.basename(file_path))
            continue

        # Specific check for 1.jsonl
        if os.path.basename(file_path) == "1.jsonl":
            assert output_lines[0] == "2023-10-01T12:00:00Z,1,login,Success", f"Unexpected output: {output_lines[0]}"
            assert output_lines[1] == "2023-10-01T12:00:00Z,2,logout,Normal A logout", f"Unexpected output: {output_lines[1]}"

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/failed: {', '.join(failed_files)}")

def test_sanitizer_evil_corpus():
    sanitizer_path = "/home/user/sanitize_logs"
    evil_files = glob.glob("/app/corpora/evil/*.jsonl")
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed_files = []

    for file_path in evil_files:
        with open(file_path, "r") as f:
            input_data = f.read()

        result = subprocess.run([sanitizer_path], input=input_data, capture_output=True, text=True)

        output_lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

        # All evil lines must be rejected
        if len(output_lines) > 0:
            bypassed_files.append(os.path.basename(file_path))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")