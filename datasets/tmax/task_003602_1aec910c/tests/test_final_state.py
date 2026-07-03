# test_final_state.py

import os
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_pipeline_execution():
    script_path = "/home/user/run_pipeline.sh"
    # Execute the script to ensure the pipeline runs
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nStderr: {result.stderr}"

def test_clean_logs_content():
    clean_dir = "/home/user/logs/clean"
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} does not exist."

    server_01 = os.path.join(clean_dir, "server_01.log")
    assert os.path.isfile(server_01), f"File {server_01} does not exist."
    with open(server_01, "r") as f:
        content_01 = f.read().strip()

    expected_01 = (
        '[2023-10-12T10:00:00Z] 192.168.1.XXX GET /api/user?email=***@example.com 200 {"cc": "****-****-****-3456"}\n'
        '[2023-10-12T10:01:00Z] 10.0.0.XXX POST /checkout 201 {"email": "***@test.org", "cc": "****-****-****-4444"}\n'
        '[2023-10-12T10:02:00Z] 172.16.254.XXX GET /index.html 404 {}'
    ).strip()
    assert content_01 == expected_01, f"Content of {server_01} is incorrect. Masking rules may not have been applied properly."

    server_02 = os.path.join(clean_dir, "server_02.log")
    assert os.path.isfile(server_02), f"File {server_02} does not exist."
    with open(server_02, "r") as f:
        content_02 = f.read().strip()

    expected_02 = (
        '[2023-10-12T10:05:00Z] 8.8.8.XXX GET /api/data 500 {"error": "bad payload"}\n'
        '[2023-10-12T10:06:00Z] 192.168.1.XXX PUT /update?user=***@domain.net 200 {"cc": "****-****-****-6666"}\n'
        '[2023-10-12T10:07:00Z] 10.1.2.XXX GET /health 200 {}'
    ).strip()
    assert content_02 == expected_02, f"Content of {server_02} is incorrect. Masking rules may not have been applied properly."

def test_summary_csv():
    summary_path = "/home/user/logs/summary.csv"
    assert os.path.isfile(summary_path), f"File {summary_path} does not exist."
    with open(summary_path, "r") as f:
        content = f.read().strip()

    expected_csv = (
        "status_code,count\n"
        "200,3\n"
        "201,1\n"
        "404,1\n"
        "500,1"
    ).strip()

    assert content == expected_csv, (
        f"Content of {summary_path} is incorrect. "
        "Ensure the header is correct and the sorting is descending by count, then ascending by status_code."
    )