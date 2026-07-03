# test_final_state.py
import os
import csv
import re
import pytest

def test_pipeline_script_exists():
    assert os.path.exists("/home/user/pipeline.sh"), "pipeline.sh is missing"
    assert os.access("/home/user/pipeline.sh", os.X_OK), "pipeline.sh is not executable"

def test_analyzer_go_exists():
    assert os.path.exists("/home/user/analyzer.go"), "analyzer.go is missing"

def test_analyzer_executable_exists():
    assert os.path.exists("/home/user/analyzer"), "Compiled analyzer executable is missing"
    assert os.access("/home/user/analyzer", os.X_OK), "analyzer is not executable"

def test_raw_logs_csv_extracted():
    assert os.path.exists("/home/user/raw_logs.csv"), "raw_logs.csv was not extracted"

def test_reshaped_logs_csv():
    csv_path = "/home/user/reshaped_logs.csv"
    assert os.path.exists(csv_path), f"{csv_path} is missing"

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["EventID", "Date", "Node", "Language", "Message"], "CSV header is incorrect"

        rows = list(reader)
        assert len(rows) == 14, f"Expected 14 long records, but found {len(rows)}"

        # Check a specific multiline message
        multiline_beta = [r for r in rows if r[2] == "Beta" and r[3] == "EN" and "\n" in r[4]]
        assert len(multiline_beta) >= 1, "Multiline message for Beta(EN) not found or newline not preserved"

def test_report_txt():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"{report_path} is missing"

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert re.search(r"Total Events Processed:\s*7", content), "Total Events Processed should be 7"
    assert re.search(r"Total Long Records:\s*14", content), "Total Long Records should be 14"
    assert re.search(r"Multiline Messages:\s*5", content), "Multiline Messages should be 5"
    assert re.search(r"Node with most multiline messages:\s*Beta", content), "Node with most multiline messages should be Beta"