# test_final_state.py
import os
import json

def test_final_summary_exists_and_correct():
    summary_path = "/home/user/app/final_summary.json"
    assert os.path.isfile(summary_path), f"{summary_path} does not exist. Did you run the fixed script?"

    with open(summary_path, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{summary_path} does not contain valid JSON."

    assert "500_count" in summary, "final_summary.json is missing the '500_count' key."
    # There are exactly 6 logs with status 500 or "500" in the provided system.log
    assert summary["500_count"] == 6, f"Expected 500_count to be 6, but got {summary['500_count']}. Make sure both integer and string 500s are counted."

def test_skipped_log_exists_and_contains_exceptions():
    skipped_path = "/home/user/app/skipped.log"
    assert os.path.isfile(skipped_path), f"{skipped_path} does not exist. Did you catch the exceptions and write to it?"

    with open(skipped_path, "r") as f:
        content = f.read().strip().split('\n')

    value_error_line = '{"status": 200, "endpoint": "api/v1/legacy", "method": "GET"}'
    memory_error_line = '{"status": 200, "endpoint": "api/v2/users", "method": "POST", "payload_size": 15000, "user_agent": "test"}'

    # Strip whitespace from both sides for robust comparison
    cleaned_content = [line.strip() for line in content if line.strip()]

    assert value_error_line in cleaned_content, f"skipped.log is missing the line that triggers ValueError: {value_error_line}"
    assert memory_error_line in cleaned_content, f"skipped.log is missing the line that triggers MemoryError: {memory_error_line}"

def test_fuzzer_and_regression_tests_exist():
    fuzzer_path = "/home/user/app/fuzzer.py"
    regression_path = "/home/user/app/test_regression.py"

    assert os.path.isfile(fuzzer_path), f"{fuzzer_path} does not exist. You must create the fuzzing script."
    assert os.path.isfile(regression_path), f"{regression_path} does not exist. You must create the regression test file."