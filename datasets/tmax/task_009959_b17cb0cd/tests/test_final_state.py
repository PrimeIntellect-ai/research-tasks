# test_final_state.py

import os
import sys
import json
import subprocess
import pytest

def test_leak_report_contents():
    report_path = "/home/user/service/leak_report.txt"
    assert os.path.isfile(report_path), f"The file {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 non-empty lines in {report_path}, found {len(lines)}."
    assert lines[0] == "_decode_cache", f"Line 1 in {report_path} is incorrect."
    assert lines[1] == "SELECT id, metadata FROM records", f"Line 2 in {report_path} is incorrect."

def test_serializer_fixed():
    pyc_path = "/home/user/service/serializer.pyc"
    py_path = "/home/user/service/serializer.py"

    assert not os.path.exists(pyc_path), f"The compiled bytecode file {pyc_path} should have been deleted."
    assert os.path.isfile(py_path), f"The fixed source file {py_path} is missing."

    with open(py_path, "r") as f:
        content = f.read()

    assert "_decode_cache" not in content, "The fixed serializer.py still contains the _decode_cache variable."
    assert "def deserialize(" in content, "The fixed serializer.py is missing the deserialize function."

def test_query_engine_fixed():
    file_path = "/home/user/service/query_engine.py"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    assert "SELECT id, metadata FROM records" not in content, "The flawed query is still present in query_engine.py."
    assert "fetchall()" not in content, "The fetchall() call is still present in query_engine.py."
    assert "?" in content or "%s" in content or "WHERE id" in content, "The query does not appear to be parameterized or filtered."

def test_main_execution_and_output():
    # Run main.py
    result = subprocess.run(
        [sys.executable, "/home/user/service/main.py", "--run"],
        cwd="/home/user/service",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"main.py failed to run successfully. Output: {result.stdout}\nErrors: {result.stderr}"
    assert "Success" in result.stdout, "main.py did not print 'Success', indicating memory limits may have been exceeded."

    output_path = "/home/user/service/output.json"
    assert os.path.isfile(output_path), f"The file {output_path} was not generated."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    assert len(data) == 3, f"Expected 3 items in output.json, found {len(data)}."

    expected_data = [
        {"user_id": 1, "action": "login", "metadata": {"status": "active", "tier": "premium"}},
        {"user_id": 2, "action": "logout", "metadata": {"status": "inactive", "tier": "free"}},
        {"user_id": 3, "action": "update", "metadata": {"status": "active", "tier": "standard"}}
    ]

    assert data == expected_data, f"The contents of {output_path} do not match the expected transformed data."