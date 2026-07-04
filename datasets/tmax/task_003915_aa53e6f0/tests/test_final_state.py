# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/firewall_validator_oracle"
STUDENT_BINARY = "/home/user/validator"
STUDENT_SOURCE = "/home/user/validator.c"
SERVICE_FILE = "/home/user/validator.service"

def test_student_files_exist():
    assert os.path.isfile(STUDENT_SOURCE), f"Source file {STUDENT_SOURCE} does not exist."
    assert os.path.isfile(STUDENT_BINARY), f"Compiled binary {STUDENT_BINARY} does not exist."
    assert os.access(STUDENT_BINARY, os.X_OK), f"Compiled binary {STUDENT_BINARY} is not executable."
    assert os.path.isfile(SERVICE_FILE), f"Service file {SERVICE_FILE} does not exist."

def test_service_file_content():
    with open(SERVICE_FILE, 'r') as f:
        content = f.read()

    assert "ExecStart=/home/user/validator" in content and "\"test_string\"" in content, \
        "Service file missing correct ExecStart directive."
    assert "Restart=always" in content, "Service file missing Restart=always directive."
    assert "RestartSec=5" in content, "Service file missing RestartSec=5 directive."

def test_fuzz_equivalence():
    random.seed(42)
    printable_chars = string.printable

    num_tests = 10000

    for i in range(num_tests):
        length = random.randint(0, 255)
        test_string = "".join(random.choice(printable_chars) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH, test_string],
            capture_output=True,
            text=True
        )
        oracle_out = oracle_proc.stdout.strip()

        # Run student binary
        student_proc = subprocess.run(
            [STUDENT_BINARY, test_string],
            capture_output=True,
            text=True
        )
        student_out = student_proc.stdout.strip()

        assert oracle_out == student_out, (
            f"Mismatch on input {repr(test_string)}.\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Student output: {repr(student_out)}"
        )