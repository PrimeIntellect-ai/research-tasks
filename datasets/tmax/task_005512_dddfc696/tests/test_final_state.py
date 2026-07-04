# test_final_state.py

import os
import subprocess
import pytest

def test_calc_sh_exists_and_executable():
    path = "/home/user/calc.sh"
    assert os.path.isfile(path), f"Expected Bash script not found at {path}"
    assert os.access(path, os.X_OK), f"Script {path} is not executable"

def test_test_pipeline_sh_exists_and_executable():
    path = "/home/user/test_pipeline.sh"
    assert os.path.isfile(path), f"Expected pipeline script not found at {path}"
    assert os.access(path, os.X_OK), f"Pipeline script {path} is not executable"

def test_pipeline_log_success():
    path = "/home/user/pipeline.log"
    assert os.path.isfile(path), f"Pipeline log not found at {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "PIPELINE SUCCESS", f"Expected 'PIPELINE SUCCESS' in {path}, got '{content}'"

def test_calc_sh_functionality():
    path = "/home/user/calc.sh"

    # Test cases: (expression, expected_output)
    test_cases = [
        ("2 3 +", "5"),
        ("10 5 /", "2"),
        ("7 3 %", "1"),
        ("5 1 2 + 4 * + 3 -", "14"),
        ("100 10 5 * - 2 /", "25"),
        ("15 7 1 1 + - / 3 * 2 %", "1"), # Secret input
        ("0 5 -", "-5") # Negative number
    ]

    for expr, expected in test_cases:
        result = subprocess.run([path, expr], capture_output=True, text=True)
        assert result.returncode == 0, f"Execution of {path} failed on expression '{expr}'"
        output = result.stdout.strip()
        assert output == expected, f"For expression '{expr}', expected '{expected}', but got '{output}'"

def test_pipeline_failure_behavior(tmp_path):
    # Create a temporary TSV with a failing test case
    failing_tsv = tmp_path / "test_cases.tsv"
    failing_tsv.write_text("2 3 +\t999\n")

    pipeline_script = "/home/user/test_pipeline.sh"

    # Run pipeline script from the directory containing the temporary TSV, 
    # or modify it if it hardcodes the path. 
    # Since the instructions say "reads test cases from /home/user/test_cases.tsv",
    # we can temporarily overwrite it to test failure behavior.

    tsv_path = "/home/user/test_cases.tsv"
    log_path = "/home/user/pipeline.log"

    # Backup original TSV
    with open(tsv_path, "r") as f:
        original_tsv = f.read()

    try:
        # Write failing TSV
        with open(tsv_path, "w") as f:
            f.write("2 3 +\t999\n")

        # Run pipeline
        result = subprocess.run([pipeline_script], capture_output=True)
        assert result.returncode != 0, "Pipeline script should exit with non-zero status on failure"

        # Check log
        with open(log_path, "r") as f:
            content = f.read().strip()
        assert content == "PIPELINE FAILED", f"Expected 'PIPELINE FAILED' in {log_path}, got '{content}'"

    finally:
        # Restore original TSV
        with open(tsv_path, "w") as f:
            f.write(original_tsv)
        # Restore success log
        with open(log_path, "w") as f:
            f.write("PIPELINE SUCCESS\n")