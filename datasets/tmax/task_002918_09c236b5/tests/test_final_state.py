# test_final_state.py

import os
import pytest

WORKSPACE = '/home/user/workspace'

def test_pipeline_script_exists():
    script_path = os.path.join(WORKSPACE, 'pipeline.sh')
    assert os.path.isfile(script_path), f"Missing shell script: {script_path}"

def test_c_program_exists():
    c_path = os.path.join(WORKSPACE, 'calc_drift.c')
    assert os.path.isfile(c_path), f"Missing C program: {c_path}"

def test_executable_exists():
    exe_path = os.path.join(WORKSPACE, 'calc_drift')
    assert os.path.isfile(exe_path), f"Missing compiled executable: {exe_path}"
    assert os.access(exe_path, os.X_OK), f"Executable {exe_path} is not executable"

def test_normalized_server1_txt():
    txt_path = os.path.join(WORKSPACE, 'server1.txt')
    assert os.path.isfile(txt_path), f"Missing normalized file: {txt_path}"

    with open(txt_path, 'r') as f:
        lines = f.readlines()

    expected_lines = [
        "max_connections=100\n",
        "mode=dev\n",
        "port=8080\n"
    ]
    assert lines == expected_lines, f"Content of {txt_path} does not match expected sorted format."

def test_normalized_server2_txt():
    txt_path = os.path.join(WORKSPACE, 'server2.txt')
    assert os.path.isfile(txt_path), f"Missing normalized file: {txt_path}"

    with open(txt_path, 'r') as f:
        lines = f.readlines()

    expected_lines = [
        "max_connections=150\n",
        "mode=prod\n",
        "port=8081\n"
    ]
    assert lines == expected_lines, f"Content of {txt_path} does not match expected sorted format."

def test_drift_report_csv():
    csv_path = os.path.join(WORKSPACE, 'drift_report.csv')
    assert os.path.isfile(csv_path), f"Missing CSV report: {csv_path}"

    with open(csv_path, 'r') as f:
        content = [line.strip() for line in f.readlines() if line.strip()]

    expected_entries = ['server1,4', 'server2,3']

    for entry in expected_entries:
        assert entry in content, f"Expected entry '{entry}' not found in {csv_path}"

def test_pipeline_log():
    log_path = os.path.join(WORKSPACE, 'pipeline.log')
    assert os.path.isfile(log_path), f"Missing log file: {log_path}"

    with open(log_path, 'r') as f:
        content = f.read()

    expected_logs = [
        "[START] Processing server1",
        "[END] Processed server1",
        "[START] Processing server2",
        "[END] Processed server2"
    ]

    for log in expected_logs:
        assert log in content, f"Expected log line '{log}' not found in {log_path}"