# test_final_state.py

import os
import pytest

def test_report_a_content():
    report_a_path = "/home/user/report_A.csv"
    assert os.path.exists(report_a_path), f"Missing file: {report_a_path}"

    expected_a = [
        "APIGateway,LogDB",
        "APIGateway,UserDB",
        "BackgroundWorker,LogDB",
        "BackgroundWorker,TxDB",
        "BackgroundWorker,UserDB",
        "WebSrv1,TxDB",
        "WebSrv1,UserDB",
        "WebSrv2,UserDB"
    ]

    with open(report_a_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_a, f"Content mismatch in {report_a_path}. Expected {expected_a}, but got {lines}."

def test_report_b_content():
    report_b_path = "/home/user/report_B.csv"
    assert os.path.exists(report_b_path), f"Missing file: {report_b_path}"

    expected_b = [
        "1,3,AuthService,5",
        "2,4,PaymentService,4",
        "3,5,UserDB,3",
        "3,8,NotificationService,3",
        "4,1,WebSrv1,2"
    ]

    with open(report_b_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Check if the student interpreted it as top 5 rows (LIMIT 5) or all nodes with rank <= 5.
    # The prompt strictly says "return ONLY the top 5 highest-ranked nodes ... sort them secondarily by the node's id".
    # This implies exactly 5 rows.
    assert len(lines) == 5, f"Expected exactly 5 rows in {report_b_path}, but got {len(lines)}."
    assert lines == expected_b, f"Content mismatch in {report_b_path}. Expected {expected_b}, but got {lines}."

def test_c_program_compiled():
    program_path = "/home/user/verify_graph"
    assert os.path.exists(program_path), f"C program executable not found at {program_path}"
    assert os.access(program_path, os.X_OK), f"File at {program_path} is not executable"