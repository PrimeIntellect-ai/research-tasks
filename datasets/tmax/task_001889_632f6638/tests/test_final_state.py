# test_final_state.py

import os
import re
import sqlite3
import glob
import subprocess

def test_script_exists_and_executable():
    script_path = "/home/user/process_dataset.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_benchmark_log():
    log_path = "/home/user/benchmark.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {log_path}, found {len(lines)}."

    expected_concurrencies = {"1", "2", "4"}
    found_concurrencies = set()

    pattern = re.compile(r"^Concurrency ([124]): ([0-9]+(?:\.[0-9]+)?) seconds$")

    for line in lines:
        match = pattern.match(line)
        assert match, f"Line '{line}' does not match the expected format 'Concurrency X: Y seconds'."
        found_concurrencies.add(match.group(1))

    assert found_concurrencies == expected_concurrencies, f"Expected concurrencies 1, 2, and 4. Found: {found_concurrencies}"

def test_database_exists():
    db_path = "/home/user/dataset.db"
    assert os.path.exists(db_path), f"Database {db_path} does not exist."

def test_database_content():
    db_path = "/home/user/dataset.db"
    raw_data_dir = "/home/user/raw_data"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents';")
    assert cursor.fetchone() is not None, "Table 'documents' does not exist in the database."

    # Check row count
    cursor.execute("SELECT count(*) FROM documents;")
    count = cursor.fetchone()[0]
    assert count == 50, f"Expected exactly 50 rows in 'documents' table, found {count}."

    # Fetch all rows
    cursor.execute("SELECT filename, word_count, embedding FROM documents;")
    rows = cursor.fetchall()
    conn.close()

    db_data = {row[0]: {"word_count": row[1], "embedding": row[2]} for row in rows}

    # Verify against actual files
    files = glob.glob(os.path.join(raw_data_dir, "doc_*.txt"))
    assert len(files) == 50, "Expected 50 raw data files."

    for file_path in files:
        filename = os.path.basename(file_path)
        assert filename in db_data, f"File {filename} is missing from the database."

        # Calculate expected word count
        try:
            out = subprocess.check_output(["wc", "-w", file_path])
            expected_word_count = int(out.split()[0])
        except Exception as e:
            pytest.fail(f"Could not calculate word count for {file_path}: {e}")

        # Calculate expected embedding
        try:
            out = subprocess.check_output(["wc", "-c", file_path])
            file_len = int(out.split()[0])
            expected_embedding = f"[{file_len}, 0.5, -0.1]"
        except Exception as e:
            pytest.fail(f"Could not calculate length for {file_path}: {e}")

        actual_word_count = db_data[filename]["word_count"]
        actual_embedding = db_data[filename]["embedding"]

        assert actual_word_count == expected_word_count, f"Word count mismatch for {filename}: expected {expected_word_count}, got {actual_word_count}."
        assert actual_embedding == expected_embedding, f"Embedding mismatch for {filename}: expected '{expected_embedding}', got '{actual_embedding}'."