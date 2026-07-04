# test_final_state.py
import os
import subprocess
import shutil
import pytest

WORKSPACE = "/home/user/ticket_8492"

def test_recovered_txt_contents():
    recovered_path = os.path.join(WORKSPACE, "recovered.txt")
    assert os.path.isfile(recovered_path), f"Expected file {recovered_path} does not exist. Did you run the daemon?"

    with open(recovered_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Type: A Payload: TEST",
        "Type: B Payload: OK"
    ]

    assert lines == expected_lines, f"Contents of recovered.txt do not match the expected output. Got: {lines}"

def test_regression_test_script_exists_and_executable():
    script_path = os.path.join(WORKSPACE, "regression_test.sh")
    assert os.path.isfile(script_path), f"Regression test script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Regression test script {script_path} is not executable."

def test_regression_test_script_success_on_fixed_code():
    script_path = os.path.join(WORKSPACE, "regression_test.sh")

    # Run the script with the fixed code
    result = subprocess.run([script_path], cwd=WORKSPACE, capture_output=True, text=True)
    assert result.returncode == 0, f"regression_test.sh failed (exit code {result.returncode}) on the fixed code. Output:\n{result.stdout}\n{result.stderr}"

def test_regression_test_script_fails_on_buggy_code():
    script_path = os.path.join(WORKSPACE, "regression_test.sh")
    cpp_path = os.path.join(WORKSPACE, "wal_parser.cpp")
    backup_path = os.path.join(WORKSPACE, "wal_parser.cpp.bak")

    # Backup the fixed code
    shutil.copy(cpp_path, backup_path)

    buggy_code = """#include "wal_parser.h"
#include <fstream>
#include <iostream>

std::vector<Record> WalParser::parse(const std::string& filepath) {
    std::ifstream file(filepath, std::ios::binary);
    std::vector<unsigned char> data((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());

    std::vector<Record> records;
    if (!data.empty()) {
        parse_record(data, 0, records);
    }
    return records;
}

void WalParser::parse_record(const std::vector<unsigned char>& data, size_t offset, std::vector<Record>& records) {
    if (offset >= data.size()) {
        return;
    }

    char type = data[offset];

    if (offset + 2 >= data.size()) return;
    uint16_t length = data[offset + 1] | (data[offset + 2] << 8);

    if (length > data.size() - offset - 3) {
        return;
    }

    if (type != 0) {
        std::string payload(data.begin() + offset + 3, data.begin() + offset + 3 + length);
        records.push_back({type, payload});
    }

    size_t next_offset = offset + 3 + length;

    if (type == 0 && length == 0) {
        next_offset = offset; // INFINITE RECURSION
    }

    parse_record(data, next_offset, records);
}
"""
    try:
        # Write the buggy code
        with open(cpp_path, "w") as f:
            f.write(buggy_code)

        # Run the script with the buggy code
        # We use a timeout to prevent actual infinite hanging if the script doesn't handle it
        try:
            result = subprocess.run([script_path], cwd=WORKSPACE, capture_output=True, text=True, timeout=5)
            assert result.returncode != 0, "regression_test.sh should return a non-zero exit code when the daemon crashes, but it returned 0."
        except subprocess.TimeoutExpired:
            # If it times out, it means the script didn't handle the infinite recursion properly
            # and just hung forever. The script should ideally fail or timeout itself.
            pytest.fail("regression_test.sh timed out. It should run the daemon and return a non-zero exit code upon failure, but it hung (likely due to infinite recursion).")

    finally:
        # Restore the fixed code
        shutil.move(backup_path, cpp_path)
        # Recompile the fixed code so we leave the workspace in the correct state
        subprocess.run(["make"], cwd=WORKSPACE, capture_output=True)