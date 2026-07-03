# test_final_state.py
import os
import re

def test_crashed_txt_exists_and_correct():
    path = "/home/user/microservices/crashed.txt"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert set(lines) == {"db_backend", "payment_gateway"}, (
        f"Contents of {path} do not match the expected crashed services. Found: {lines}"
    )

def test_auto_extract_exp_exists():
    path = "/home/user/microservices/auto_extract.exp"
    assert os.path.isfile(path), f"Expect script {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "secret_vault" in content, f"Expect script {path} does not seem to contain the correct password."

def test_restore_manager_cpp_exists():
    path = "/home/user/microservices/restore_manager.cpp"
    assert os.path.isfile(path), f"C++ source file {path} is missing."

def test_restore_manager_executable_exists():
    path = "/home/user/microservices/restore_manager"
    assert os.path.isfile(path), f"Compiled executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_recovery_log_exists_and_correct():
    path = "/home/user/microservices/recovery.log"
    assert os.path.isfile(path), f"Recovery log {path} is missing."
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "RESTORED db_backend TO /home/user/microservices/vols/db",
        "RESTORED payment_gateway TO /home/user/microservices/vols/pay"
    }

    assert set(lines) == expected_lines, (
        f"Contents of {path} do not match expected recovery log entries. Found: {lines}"
    )

def test_restored_data_files():
    db_restored = "/home/user/microservices/vols/db/restored_data.txt"
    pay_restored = "/home/user/microservices/vols/pay/restored_data.txt"
    auth_restored = "/home/user/microservices/vols/auth/restored_data.txt"

    assert os.path.isfile(db_restored), f"Expected restored data file missing: {db_restored}"
    assert os.path.isfile(pay_restored), f"Expected restored data file missing: {pay_restored}"
    assert not os.path.exists(auth_restored), f"File {auth_restored} should not exist (auth service did not crash)."