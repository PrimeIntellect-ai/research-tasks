# test_final_state.py

import os
import subprocess
import pytest
import re

WORKSPACE_DIR = "/home/user/workspace/async_engine"
BUG_REPORT_PATH = "/home/user/workspace/bug_report.txt"
TEST_CPP_PATH = os.path.join(WORKSPACE_DIR, "test_cancellation.cpp")

def test_make_test_passes():
    """Verify that `make test` completes successfully without crashing."""
    try:
        result = subprocess.run(
            ["make", "test"],
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        assert result.returncode == 0, "`make test` did not exit with code 0."
        assert "Test passed" in result.stdout, "Expected 'Test passed' in the output of `make test`."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"`make test` failed to run successfully.\nStdout: {e.stdout}\nStderr: {e.stderr}")

def test_bug_report_exists_and_content():
    """Verify that bug_report.txt exists and contains the required information."""
    assert os.path.isfile(BUG_REPORT_PATH), f"Bug report file {BUG_REPORT_PATH} is missing."

    with open(BUG_REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read().lower()

    assert "get_average_processing_time" in content, (
        "The bug report must contain the name of the function where the crash occurred "
        "('get_average_processing_time')."
    )

    # Check for explanation of mathematical/numerical error
    has_math_error = bool(re.search(r'divis|zero|0', content))
    assert has_math_error, (
        "The bug report must mention the mathematical/numerical error (e.g., division by zero)."
    )

def test_test_cancellation_cpp_not_modified():
    """Verify that test_cancellation.cpp was not modified by the user."""
    expected_content = """#include "engine.h"
#include <iostream>

int main() {
    ExecutionEngine engine;
    engine.start(4);

    // Immediately cancel without completing any tasks
    engine.cancel();

    // Gather stats (this will crash due to divide-by-zero)
    int avg_time = engine.get_average_processing_time();

    std::cout << "Test passed. Average time: " << avg_time << " ms" << std::endl;
    return 0;
}
"""
    assert os.path.isfile(TEST_CPP_PATH), f"File {TEST_CPP_PATH} is missing."

    with open(TEST_CPP_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), (
        "You must not modify the test file (`test_cancellation.cpp`)."
    )