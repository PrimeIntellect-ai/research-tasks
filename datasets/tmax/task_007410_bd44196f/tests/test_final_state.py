# test_final_state.py

import os
import pytest

def test_core_c_recovered():
    core_c_path = '/home/user/investigation/core.c'
    assert os.path.isfile(core_c_path), f"The file {core_c_path} was not recovered."
    with open(core_c_path, 'r') as f:
        content = f.read()
    assert "int generate_payload(int key)" in content, "The recovered core.c does not contain the expected function."
    assert "return key * 73 + 1337;" in content, "The recovered core.c does not contain the expected logic."

def test_malware_runner_fixed():
    runner_path = '/home/user/investigation/malware_runner.py'
    assert os.path.isfile(runner_path), f"The script {runner_path} is missing."
    with open(runner_path, 'r') as f:
        content = f.read()
    # It shouldn't crash with TypeError anymore, so typically they cast to int
    # We won't strictly enforce `int(key)` in code, as the report generation proves it works,
    # but we can check that it was modified.
    assert "payload = lib.generate_payload(key)" not in content or "int(key)" in content or "int(os.environ" in content, \
        "The malware_runner.py script does not appear to be fixed to handle the string environment variable."

def test_report_generated_and_correct():
    report_path = '/home/user/investigation/report.txt'
    assert os.path.isfile(report_path), f"The report file {report_path} was not generated."

    with open(report_path, 'r') as f:
        content = f.read().strip()

    expected_output = "PAYLOAD:7248850"
    assert content == expected_output, f"The report file does not contain the correct output. Expected '{expected_output}', got '{content}'."