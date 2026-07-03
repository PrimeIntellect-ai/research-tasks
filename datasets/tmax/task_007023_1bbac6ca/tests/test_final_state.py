# test_final_state.py

import os
import re

def test_script_exists_and_executable():
    script_path = '/home/user/organize_datasets.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_report_exists():
    report_path = '/home/user/validation_report.txt'
    assert os.path.isfile(report_path), f"Report file {report_path} was not generated."

def test_report_content_invalid_datasets():
    report_path = '/home/user/validation_report.txt'
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."
    with open(report_path, 'r') as f:
        content = f.read()

    # Check for the expected invalid datasets line
    expected_line = "Invalid Datasets: dataset_3"
    assert re.search(r'^Invalid Datasets:\s*dataset_3$', content, re.MULTILINE), \
        f"Expected to find '{expected_line}' in {report_path}. Found:\n{content}"

def test_report_content_most_similar_pair():
    report_path = '/home/user/validation_report.txt'
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."
    with open(report_path, 'r') as f:
        content = f.read()

    # Check for the expected most similar pair line
    expected_line = "Most Similar Pair: dataset_1, dataset_2"
    assert re.search(r'^Most Similar Pair:\s*dataset_1,\s*dataset_2$', content, re.MULTILINE), \
        f"Expected to find '{expected_line}' in {report_path}. Found:\n{content}"