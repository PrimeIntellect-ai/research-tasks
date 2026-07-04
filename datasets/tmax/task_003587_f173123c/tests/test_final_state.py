# test_final_state.py

import os
import json
import pytest

def test_report_exists_and_content():
    report_path = '/home/user/optimizer_report.json'
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, 'r', encoding='utf-8') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {report_path} is not valid JSON.")

    assert report.get('total_files_processed') == 5, "total_files_processed should be 5."
    assert report.get('csv_to_json_conversions') == 2, "csv_to_json_conversions should be 2."
    assert report.get('hard_links_created') == 2, "hard_links_created should be 2."

def test_csv_files_deleted():
    assert not os.path.exists('/home/user/logs/appA/log1.csv'), "log1.csv should have been deleted."
    assert not os.path.exists('/home/user/logs/appA/log3.csv'), "log3.csv should have been deleted."

def test_json_files_exist_and_utf8():
    expected_files = [
        '/home/user/logs/appA/log1.json',
        '/home/user/logs/appB/log2.json',
        '/home/user/logs/appA/log3.json',
        '/home/user/logs/appB/log4.json',
        '/home/user/logs/appA/log5.json'
    ]

    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Expected JSON file {file_path} is missing."

        # Verify it's valid UTF-8 JSON
        with open(file_path, 'rb') as f:
            raw_content = f.read()
            try:
                text_content = raw_content.decode('utf-8')
            except UnicodeDecodeError:
                pytest.fail(f"File {file_path} is not valid UTF-8.")

            try:
                json.loads(text_content)
            except json.JSONDecodeError:
                pytest.fail(f"File {file_path} does not contain valid JSON.")

def test_hard_links_created():
    log1_path = '/home/user/logs/appA/log1.json'
    log2_path = '/home/user/logs/appB/log2.json'
    log3_path = '/home/user/logs/appA/log3.json'
    log4_path = '/home/user/logs/appB/log4.json'
    log5_path = '/home/user/logs/appA/log5.json'

    assert os.path.exists(log1_path), f"{log1_path} does not exist."
    assert os.path.exists(log2_path), f"{log2_path} does not exist."
    assert os.path.exists(log3_path), f"{log3_path} does not exist."
    assert os.path.exists(log4_path), f"{log4_path} does not exist."
    assert os.path.exists(log5_path), f"{log5_path} does not exist."

    stat1 = os.stat(log1_path)
    stat2 = os.stat(log2_path)
    stat3 = os.stat(log3_path)
    stat4 = os.stat(log4_path)
    stat5 = os.stat(log5_path)

    assert stat1.st_ino == stat2.st_ino, "log1.json and log2.json should be hard-linked (same inode)."
    assert stat3.st_ino == stat4.st_ino, "log3.json and log4.json should be hard-linked (same inode)."
    assert stat5.st_nlink == 1, "log5.json should not have any additional hard links (nlink == 1)."