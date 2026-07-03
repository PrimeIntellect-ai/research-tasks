# test_final_state.py
import os
import sqlite3
import pytest

def test_audit_results_exists_and_correct():
    results_path = "/home/user/audit_results.txt"
    assert os.path.exists(results_path), f"Expected output file {results_path} is missing."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    with open(results_path, 'r') as f:
        content = f.read().strip().split('\n')

    expected_content = [
        "101,RES-A,APPROVED",
        "102,RES-A,APPROVED",
        "103,RES-A,APPROVED",
        "104,RES-B,DENIED",
        "102,RES-B,APPROVED",
        "103,RES-B,APPROVED",
        "102,RES-C,DENIED",
        "103,RES-C,APPROVED",
        "104,RES-C,DENIED",
        "101,RES-D,APPROVED"
    ]

    assert content == expected_content, f"Content of {results_path} does not match the expected audit results."

def test_cpp_source_code_exists():
    cpp_path = "/home/user/audit_processor.cpp"
    assert os.path.exists(cpp_path), f"C++ source file {cpp_path} is missing."
    assert os.path.isfile(cpp_path), f"{cpp_path} is not a file."

    with open(cpp_path, 'r') as f:
        code = f.read()

    assert "sqlite3.h" in code, "The C++ source code does not seem to include the sqlite3 header."

def test_database_unchanged():
    db_path = "/home/user/corp_auth.db"
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees;")
    assert cursor.fetchone()[0] == 4, "The employees table was modified."

    cursor.execute("SELECT COUNT(*) FROM departments;")
    assert cursor.fetchone()[0] == 6, "The departments table was modified."

    cursor.execute("SELECT COUNT(*) FROM resource_policies;")
    assert cursor.fetchone()[0] == 4, "The resource_policies table was modified."

    conn.close()

def test_access_requests_unchanged():
    req_path = "/home/user/access_requests.txt"
    assert os.path.exists(req_path), f"Access requests file {req_path} is missing."

    with open(req_path, 'r') as f:
        content = f.read().strip().split('\n')

    expected_content = [
        "101,RES-A",
        "102,RES-A",
        "103,RES-A",
        "104,RES-B",
        "102,RES-B",
        "103,RES-B",
        "102,RES-C",
        "103,RES-C",
        "104,RES-C",
        "101,RES-D"
    ]

    assert content == expected_content, f"Content of {req_path} was modified."