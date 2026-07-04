# test_final_state.py
import os
import json

def test_result_json_exists():
    result_path = '/home/user/scheduler_service/result.json'
    assert os.path.exists(result_path), f"{result_path} does not exist. The task was not completed properly."

def test_result_json_content():
    result_path = '/home/user/scheduler_service/result.json'
    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{result_path} does not contain valid JSON."

    assert 'scheduled_jobs' in data, "The key 'scheduled_jobs' is missing from the JSON result."
    assert 'hash' in data, "The key 'hash' is missing from the JSON result."

    expected_jobs = ["J2", "J3", "J5"]
    assert data['scheduled_jobs'] == expected_jobs, f"Expected scheduled_jobs to be {expected_jobs}, but got {data['scheduled_jobs']}"

    # Compute expected hash to avoid hardcoding opaque constants where possible
    # 'J'=74, '2'=50 -> 124
    # 'J'=74, '3'=51 -> 125
    # 'J'=74, '5'=53 -> 127
    # Sum = 376
    expected_hash = sum(sum(ord(c) for c in job_id) for job_id in expected_jobs)
    assert data['hash'] == expected_hash, f"Expected hash to be {expected_hash}, but got {data['hash']}"

def test_server_py_exists():
    server_path = '/home/user/scheduler_service/server.py'
    assert os.path.exists(server_path), f"{server_path} does not exist. The API server script is missing."

def test_c_extension_fixed():
    c_file_path = '/home/user/scheduler_service/job_hasher.c'
    assert os.path.exists(c_file_path), f"{c_file_path} does not exist."
    with open(c_file_path, 'r') as f:
        content = f.read()

    assert "PyBytes_AsString" not in content, "The C-extension still contains PyBytes_AsString, which causes segfaults in Python 3."
    assert "PyUnicode_AsUTF8" in content or "PyUnicode_AsUTF8AndSize" in content, "The C-extension does not seem to use a valid Python 3 Unicode C-API function (like PyUnicode_AsUTF8)."