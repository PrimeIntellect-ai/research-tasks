# test_final_state.py
import os
import re
import json
import urllib.request
import pytest

def test_corruption_report():
    report_path = "/home/user/corruption_report.txt"
    assert os.path.exists(report_path), f"File {report_path} does not exist."

    archive_dir = "/home/user/dataset_archive"
    expected_lines = []

    for root, _, files in os.walk(archive_dir):
        for f in files:
            if f.endswith('.log'):
                with open(os.path.join(root, f), 'r') as log_f:
                    for line in log_f:
                        if line.startswith("ERROR: CORRUPT_RECORD ID="):
                            m = re.search(r"ID=(\d+).*?\[(.*?)\]", line)
                            if m:
                                expected_lines.append((int(m.group(1)), m.group(1), m.group(2)))

    expected_lines.sort(key=lambda x: x[0])
    expected_text = "\n".join(f"{x[1]} - {x[2]}" for x in expected_lines)

    with open(report_path, 'r') as f:
        actual_text = f.read().strip()

    assert actual_text == expected_text, (
        f"Content of {report_path} is incorrect.\n"
        f"Expected:\n{expected_text}\n"
        f"Got:\n{actual_text}"
    )

def test_meta_files():
    script_path = "/home/user/generate_meta.py"
    assert os.path.exists(script_path), f"Python script {script_path} does not exist."

    archive_dir = "/home/user/dataset_archive"
    for root, _, files in os.walk(archive_dir):
        for f in files:
            if f.endswith('.dat'):
                dat_path = os.path.join(root, f)
                meta_path = dat_path[:-4] + ".meta"
                assert os.path.exists(meta_path), f"Missing meta file {meta_path} for {dat_path}."

                with open(dat_path, 'rb') as df:
                    expected_hex = df.read(8).hex()

                with open(meta_path, 'r') as mf:
                    actual_hex = mf.read().strip()

                assert actual_hex == expected_hex, (
                    f"Content of {meta_path} is incorrect. "
                    f"Expected {expected_hex}, got {actual_hex}."
                )

def test_final_summary():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Bash script {script_path} does not exist."

    json_path = "/home/user/final_summary.json"
    assert os.path.exists(json_path), f"JSON summary file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "corrupt_records" in data, "Missing key 'corrupt_records' in JSON."
    assert "new_meta_files" in data, "Missing key 'new_meta_files' in JSON."

    assert data["corrupt_records"] == 3, f"Expected 3 corrupt records, got {data['corrupt_records']}."
    assert data["new_meta_files"] == 3, f"Expected 3 new meta files, got {data['new_meta_files']}."

def test_server_running():
    pid_file = "/home/user/server.pid"
    assert os.path.exists(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: '{pid_str}'."
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} (from {pid_file}) is not running.")

    try:
        req = urllib.request.urlopen("http://localhost:8080/", timeout=2)
        assert req.status == 200, f"Server returned status {req.status} instead of 200."
        body = req.read().decode('utf-8')
        assert "exp_A" in body and "exp_B" in body, (
            "Server is reachable but does not seem to be serving the correct directory "
            "(/home/user/dataset_archive)."
        )
    except Exception as e:
        pytest.fail(f"Could not connect to HTTP server on port 8080 or verify content: {e}")