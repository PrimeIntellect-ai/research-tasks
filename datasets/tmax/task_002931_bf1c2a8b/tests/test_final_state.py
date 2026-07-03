# test_final_state.py

import os
import subprocess
import pytest

def test_cycle_report_contents():
    report_path = '/home/user/cycle_report.txt'
    assert os.path.isfile(report_path), f"File {report_path} does not exist. The cycle report was not created."

    with open(report_path, 'r') as f:
        content = f.read().strip()

    expected_cycle = "task_A -> task_B -> task_C -> task_A"
    assert content == expected_cycle, f"Cycle report content is incorrect. Expected '{expected_cycle}', but got '{content}'."

def test_invalid_versions_file_exists():
    invalid_versions_path = '/home/user/invalid_versions.txt'
    assert os.path.isfile(invalid_versions_path), f"File {invalid_versions_path} does not exist."

def test_pipeline_analyzer_exists():
    analyzer_path = '/home/user/pipeline_analyzer.py'
    assert os.path.isfile(analyzer_path), f"File {analyzer_path} does not exist."

def test_test_analyzer_exists_and_passes():
    test_path = '/home/user/test_analyzer.py'
    assert os.path.isfile(test_path), f"File {test_path} does not exist."

    # Run pytest on the test_analyzer.py
    result = subprocess.run(
        ['pytest', test_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"pytest on {test_path} failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"