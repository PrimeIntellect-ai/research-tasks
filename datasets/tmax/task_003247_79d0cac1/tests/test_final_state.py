# test_final_state.py

import os
import subprocess
import pytest

def test_overflow_report_exists_and_correct():
    report_path = "/home/user/perf_profiling/overflow_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "log_37.txt 2500000000"
    assert content == expected_content, f"Content of {report_path} is incorrect. Expected '{expected_content}', got '{content}'."

def test_fixed_summarize_exists_and_executable():
    script_path = "/home/user/perf_profiling/fixed_summarize.sh"
    assert os.path.isfile(script_path), f"Script file {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script file {script_path} is not executable."

def test_fixed_summarize_does_not_use_binary():
    script_path = "/home/user/perf_profiling/fixed_summarize.sh"
    with open(script_path, "r") as f:
        content = f.read()

    assert "metric_filter" not in content, "The fixed_summarize.sh script should not use the buggy metric_filter binary."

def test_fixed_summarize_execution_and_results():
    script_path = "/home/user/perf_profiling/fixed_summarize.sh"
    results_path = "/home/user/perf_profiling/results.txt"

    # Remove results.txt if it exists to ensure we are testing the new script's output
    if os.path.exists(results_path):
        os.remove(results_path)

    # Run the fixed script
    result = subprocess.run([script_path], cwd="/home/user/perf_profiling", capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed to execute properly. Stderr: {result.stderr}"

    assert os.path.isfile(results_path), f"The script did not generate {results_path}."

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 50, f"Expected 50 lines in {results_path}, but got {len(lines)}."

    results_dict = {}
    for line in lines:
        parts = line.split(":")
        assert len(parts) == 2, f"Invalid format in results.txt line: {line}"
        filename = parts[0].strip()
        total = parts[1].strip()
        results_dict[filename] = total

    for i in range(1, 51):
        filename = f"log_{i:02d}.txt"
        assert filename in results_dict, f"Missing result for {filename} in {results_path}."

        if i == 37:
            expected_total = "2500000000"
        else:
            expected_total = "1000000000"

        actual_total = results_dict[filename]
        assert actual_total == expected_total, f"Incorrect total for {filename}. Expected {expected_total}, got {actual_total}."