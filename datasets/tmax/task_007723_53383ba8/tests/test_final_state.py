# test_final_state.py
import os
import re
import subprocess
import pytest

def test_diagnostic_report():
    report_path = "/home/user/diagnostic_report.txt"
    assert os.path.isfile(report_path), "Diagnostic report not found at /home/user/diagnostic_report.txt"

    with open(report_path, "r") as f:
        content = f.read().strip()
        lines = [line.strip() for line in content.split('\n') if line.strip() != ""]

    assert len(lines) == 2, f"Diagnostic report must have exactly 2 lines, found {len(lines)}"

    expected_commit_path = "/tmp/expected_bad_commit.txt"
    assert os.path.isfile(expected_commit_path), f"Expected commit file {expected_commit_path} is missing"

    with open(expected_commit_path, "r") as f:
        expected_commit = f.read().strip()

    assert lines[0] == expected_commit, f"Line 1 of report is '{lines[0]}', expected '{expected_commit}'"
    assert lines[1] == "50", f"Line 2 of report is '{lines[1]}', expected '50'"

def test_aggregate_logs_fixed():
    script_path = "/home/user/log_aggregator/aggregate_logs.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    # Run the script on test logs to ensure it computes the correct integer sum
    output_file = "/tmp/test_output_fixed.txt"
    result = subprocess.run([script_path, "/home/user/log_aggregator/test_logs", output_file], capture_output=True, text=True)
    assert result.returncode == 0, f"aggregate_logs.sh failed to run on test logs. Stderr: {result.stderr}"

    assert os.path.isfile(output_file), "aggregate_logs.sh did not create the output file"
    with open(output_file, "r") as f:
        output = f.read().strip()
    assert output == "Total Errors: 7", f"Script did not compute the correct sum. Expected 'Total Errors: 7', got '{output}'"

def test_aggregate_logs_assertion_behavior():
    script_path = "/home/user/log_aggregator/aggregate_logs.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"

    with open(script_path, "r") as f:
        content = f.read()

    assert "exit 2" in content, "aggregate_logs.sh does not contain 'exit 2' for the assertion failure"

    # Inject a non-digit value into total_errors right after the loop to test the assertion logic
    # We replace the loop with a hardcoded bad value to ensure the assertion catches it.
    modified_content = re.sub(r'for f in.*?\bdone\b', 'total_errors="123 bad"', content, flags=re.DOTALL)

    if modified_content == content:
        # If regex replacement fails, fallback to checking for regex/glob matching in the script
        has_validation = re.search(r'\[\[.*=~.*\]\]', content) or re.search(r'[^0-9]', content) or re.search(r'case.*in', content)
        assert has_validation, "aggregate_logs.sh does not seem to contain a check for non-digits in total_errors"
    else:
        test_script = "/tmp/test_agg_assertion.sh"
        with open(test_script, "w") as f:
            f.write(modified_content)
        os.chmod(test_script, 0o755)

        result = subprocess.run([test_script, "/home/user/log_aggregator/test_logs", "/tmp/out_bad.txt"], capture_output=True, text=True)
        assert result.returncode == 2, f"Script did not exit with status 2 when total_errors contains non-digits. Exited with {result.returncode}"
        assert result.stderr.strip() != "", "Script did not print an error message to stderr when the assertion failed"