# test_final_state.py
import os
import json
import pytest
import stat

def test_matrix_csv_patched():
    file_path = "/home/user/matrix.csv"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip().replace("\r\n", "\n")

    expected_content = "1.0, 2.0, 3.0\n4.0, 10.0, 6.0\n7.0, 8.0, 9.0"
    assert content == expected_content, f"Content of {file_path} does not match the expected patched state. Found:\n{content}"

def test_result_json_exists_and_correct():
    file_path = "/home/user/result.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The e2e_test.sh script might not have generated it."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    assert "trace" in data, "JSON result is missing the 'trace' key."
    assert "frobenius" in data, "JSON result is missing the 'frobenius' key."

    trace_val = float(data["trace"])
    frob_val = float(data["frobenius"])

    assert abs(trace_val - 20.0) < 1e-4, f"Expected trace to be 20.0, got {trace_val}"
    assert abs(frob_val - 18.9737) < 1e-4, f"Expected frobenius to be 18.9737, got {frob_val}"

def test_e2e_test_script_exists_and_executable():
    file_path = "/home/user/e2e_test.sh"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {file_path} is not executable."

def test_server_py_modified():
    file_path = "/home/user/server.py"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    # Just a simple check that they likely implemented it
    assert "TODO" not in content or len(content.splitlines()) > 25, "server.py doesn't seem to be fully implemented."