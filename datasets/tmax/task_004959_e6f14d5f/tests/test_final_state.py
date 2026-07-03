# test_final_state.py
import os
import subprocess
import pytest

APP_DIR = "/app/tiny_vm_grpc"
BENCHMARK_RESULT_PATH = os.path.join(APP_DIR, "benchmark_result.txt")
TEST_FILE_PATH = os.path.join(APP_DIR, "tests", "test_vm.py")

def test_benchmark_result():
    assert os.path.exists(BENCHMARK_RESULT_PATH), f"Benchmark result file not found at {BENCHMARK_RESULT_PATH}"

    with open(BENCHMARK_RESULT_PATH, 'r') as f:
        content = f.read().strip()

    try:
        execution_time = float(content)
    except ValueError:
        pytest.fail(f"Benchmark result file does not contain a valid float. Content: {content}")

    threshold = 0.5
    assert execution_time <= threshold, f"Execution time {execution_time} is not <= {threshold} seconds"

def test_unit_tests_pass():
    assert os.path.exists(TEST_FILE_PATH), f"Test file not found at {TEST_FILE_PATH}"

    # Run pytest on the tests directory
    result = subprocess.run(
        ["pytest", TEST_FILE_PATH],
        cwd=APP_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Unit tests failed. Pytest output:\n{result.stdout}\n{result.stderr}"