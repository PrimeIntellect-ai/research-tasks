# test_final_state.py

import os
import subprocess
import pytest

def test_cron_schedule():
    """Test that the cron schedule file exists and contains the correct entry."""
    cron_file = "/home/user/cron_schedule.txt"
    assert os.path.isfile(cron_file), f"Cron schedule file {cron_file} is missing."

    with open(cron_file, 'r') as f:
        content = f.read().strip()

    expected_cron = "0 2 * * * /home/user/pipeline.sh"
    assert content == expected_cron, f"Cron schedule is incorrect. Expected '{expected_cron}', got '{content}'."

def test_cpp_source_exists():
    """Test that the C++ source file exists."""
    cpp_file = "/home/user/src/dedup.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."

def test_pipeline_execution_and_output():
    """Test that the pipeline script is executable, runs successfully, and produces the correct output."""
    pipeline_script = "/home/user/pipeline.sh"
    report_file = "/home/user/deduped_report.tsv"

    assert os.path.isfile(pipeline_script), f"Pipeline script {pipeline_script} is missing."
    assert os.access(pipeline_script, os.X_OK), f"Pipeline script {pipeline_script} is not executable."

    # Remove the report file if it exists to ensure the pipeline creates it
    if os.path.exists(report_file):
        os.remove(report_file)

    # Run the pipeline
    result = subprocess.run([pipeline_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}.\nStderr: {result.stderr}"

    # Check the output file
    assert os.path.isfile(report_file), f"Output report {report_file} was not created by the pipeline."

    with open(report_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "138118029\terr_network\tNetwork error",
        "139556272\tbil_invoice\tInvoice",
        "188282004\tbil_cancel_sub\tCancel",
        "421396301\tbil_submit_payment\tSubmit",
        "627196884\terr_auth\tAuthentication failed",
        "878036087\tlbl_welcome\tWelcome back!"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in report, got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nGot:      {actual}"