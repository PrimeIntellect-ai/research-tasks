# test_final_state.py

import os
import subprocess
import tempfile

WORKSPACE_DIR = "/home/user/workspace"
CWE_PATH = os.path.join(WORKSPACE_DIR, "cwe.txt")
ATTACKER_PATH = os.path.join(WORKSPACE_DIR, "attacker.txt")
DETECT_PY_PATH = os.path.join(WORKSPACE_DIR, "detect.py")
ACCESS_LOG_PATH = os.path.join(WORKSPACE_DIR, "access.log")

def test_cwe_file_content():
    assert os.path.isfile(CWE_PATH), f"File {CWE_PATH} does not exist."
    with open(CWE_PATH, "r") as f:
        content = f.read().strip()
    assert content == "CWE-601", f"Expected 'CWE-601' in {CWE_PATH}, but got '{content}'."

def test_attacker_file_content():
    assert os.path.isfile(ATTACKER_PATH), f"File {ATTACKER_PATH} does not exist."
    with open(ATTACKER_PATH, "r") as f:
        content = f.read().strip()
    assert content == "10.10.10.10", f"Expected '10.10.10.10' in {ATTACKER_PATH}, but got '{content}'."

def test_detect_script_exists():
    assert os.path.isfile(DETECT_PY_PATH), f"File {DETECT_PY_PATH} does not exist."

def test_detect_script_output_original_log():
    result = subprocess.run(
        ["python3", DETECT_PY_PATH, ACCESS_LOG_PATH],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"detect.py exited with code {result.returncode}. Error: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    expected_lines = ["10.10.10.10", "192.168.1.51"]

    assert output_lines == expected_lines, f"Expected output {expected_lines}, but got {output_lines}"

def test_detect_script_output_custom_log():
    custom_log_content = """1.1.1.1 - - [10/Oct/2023:13:55:36 -0700] "GET /login?next=/dashboard HTTP/1.1" 200 2326
2.2.2.2 - - [10/Oct/2023:13:56:10 -0700] "GET /login?next=http://bad.com HTTP/1.1" 302 2326
3.3.3.3 - - [10/Oct/2023:13:57:36 -0700] "GET /login?next=https://worse.org HTTP/1.1" 302 2326
4.4.4.4 - - [10/Oct/2023:13:58:00 -0700] "POST /login?next=http://evil.com HTTP/1.1" 302 2326
2.2.2.2 - - [10/Oct/2023:13:56:10 -0700] "GET /login?next=http://bad.com HTTP/1.1" 302 2326
5.5.5.5 - - [10/Oct/2023:13:59:00 -0700] "GET /other?next=http://evil.com HTTP/1.1" 200 1234
"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_log:
        tmp_log.write(custom_log_content)
        tmp_log_path = tmp_log.name

    try:
        result = subprocess.run(
            ["python3", DETECT_PY_PATH, tmp_log_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"detect.py exited with code {result.returncode} on custom log."

        output_lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        expected_lines = ["2.2.2.2", "3.3.3.3"]

        assert output_lines == expected_lines, (
            f"detect.py did not correctly parse the custom log. "
            f"Expected {expected_lines}, but got {output_lines}."
        )
    finally:
        os.remove(tmp_log_path)