# test_final_state.py

import os
import sqlite3
import re
import stat

def test_pipeline_script_exists_and_executable():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"Pipeline script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Pipeline script {path} is not executable."

def test_working_data_copied():
    path = "/home/user/local_processing/working_data.csv"
    assert os.path.isfile(path), f"Working data file {path} does not exist."

def test_cleaned_data_correct():
    path = "/home/user/local_processing/cleaned_data.csv"
    assert os.path.isfile(path), f"Cleaned data file {path} does not exist."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 5, f"Expected 5 lines (1 header + 4 data rows) in cleaned_data.csv, found {len(lines)}."
    assert lines[0] == "ID,Name,Email,Score,Department", "Header is missing or incorrect in cleaned_data.csv."

    for line in lines[1:]:
        parts = line.split(',')
        assert len(parts) == 5, "Each row must have exactly 5 columns."
        # Check no leading/trailing spaces
        for part in parts:
            assert part == part.strip(), f"Found leading/trailing spaces in field '{part}'."
        # Check email is lowercase
        email = parts[2]
        assert email == email.lower(), f"Email '{email}' is not strictly lowercase."
        # Check score is not empty
        score = parts[3]
        assert score != "", "Score field is completely empty in a row."

def test_database_and_table():
    db_path = "/home/user/db/analytics.sqlite"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM employee_stats;")
    count = cursor.fetchone()[0]
    assert count == 4, f"Expected 4 records in employee_stats, found {count}."

    cursor.execute("SELECT email FROM employee_stats WHERE id=1;")
    email = cursor.fetchone()[0]
    assert email == "alice@example.com", f"Expected 'alice@example.com' for id=1, found '{email}'."

    conn.close()

def test_final_report():
    path = "/home/user/reports/final_report.md"
    assert os.path.isfile(path), f"Report file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "Total valid records processed: 4" in content, "Report does not contain the correct total record count."
    assert re.search(r"Engineering:\s*88\.5", content), "Report does not contain correct Engineering average (88.5)."
    assert re.search(r"HR:\s*78(?:\.0)?", content), "Report does not contain correct HR average (78 or 78.0)."
    assert re.search(r"Sales:\s*82(?:\.0)?", content), "Report does not contain correct Sales average (82 or 82.0)."

def test_cron_conf():
    path = "/home/user/cron.conf"
    assert os.path.isfile(path), f"Cron config file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert "30 3 * * * /home/user/pipeline.sh" in content, "cron.conf does not contain the correct schedule."