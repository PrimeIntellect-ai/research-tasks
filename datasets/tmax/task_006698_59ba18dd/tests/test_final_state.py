# test_final_state.py

import os
import json
import subprocess

def test_run_pipeline_success():
    """
    Ensure the pipeline script runs successfully without errors.
    """
    script_path = '/home/user/pipeline/run_pipeline.sh'
    assert os.path.isfile(script_path), f"Pipeline script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Pipeline script at {script_path} is not executable"

    # Run the pipeline script
    result = subprocess.run(
        [script_path],
        cwd='/home/user/pipeline',
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"Pipeline script failed with return code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

def test_summary_report_generated_and_correct():
    """
    Ensure the summary report is generated and contains the correct counts.
    """
    report_path = '/home/user/pipeline/data/summary_report.json'
    assert os.path.isfile(report_path), f"Summary report missing at {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Summary report is not valid JSON: {e}"

    assert isinstance(data, dict), "Summary report JSON should be a dictionary"

    assert 'CRITICAL' in data, "Summary report is missing the 'CRITICAL' log level count"
    assert data['CRITICAL'] == 1, f"Expected 1 CRITICAL log, but found {data['CRITICAL']}"

    assert 'INFO' in data, "Summary report is missing the 'INFO' log level count"
    assert data['INFO'] >= 3, f"Expected at least 3 INFO logs, but found {data['INFO']}"