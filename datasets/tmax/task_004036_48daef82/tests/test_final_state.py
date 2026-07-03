# test_final_state.py

import os
import re

def test_venv_exists():
    venv_python = '/home/user/venv/bin/python'
    assert os.path.exists('/home/user/venv'), "Virtual environment directory /home/user/venv does not exist."
    assert os.path.exists(venv_python) or os.path.exists('/home/user/venv/bin/python3'), "Python executable not found in /home/user/venv/bin/."

def test_pipeline_script_exists():
    script_path = '/home/user/pipeline.py'
    assert os.path.exists(script_path), f"Script not found at {script_path}."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_outliers_txt():
    outliers_path = '/home/user/outliers.txt'
    assert os.path.exists(outliers_path), f"Expected {outliers_path} to exist."

    with open(outliers_path, 'r') as f:
        content = f.read().strip()

    assert content, f"{outliers_path} is empty."

    lines = content.split('\n')
    # Contamination is 0.1 on 89 records -> 8 outliers expected
    assert len(lines) == 8, f"Expected exactly 8 lines in {outliers_path}, but found {len(lines)}."

    ids = []
    for line in lines:
        assert line.isdigit(), f"Expected each line to be an integer ID, but found '{line}'."
        ids.append(int(line))

    assert ids == sorted(ids), f"Expected IDs in {outliers_path} to be sorted in ascending order."
    assert len(set(ids)) == len(ids), f"Expected all IDs in {outliers_path} to be unique."

def test_metrics_txt():
    metrics_path = '/home/user/metrics.txt'
    assert os.path.exists(metrics_path), f"Expected {metrics_path} to exist."

    with open(metrics_path, 'r') as f:
        content = f.read().strip()

    # Check exact format requirement: "Accuracy: 0.XXXX" (or 1.0000)
    match = re.match(r'^Accuracy:\s*(0\.\d{4}|1\.0{4})$', content)
    assert match, f"Content '{content}' in {metrics_path} does not match the required format 'Accuracy: 0.XXXX'."

    accuracy = float(match.group(1))
    assert 0.0 <= accuracy <= 1.0, f"Parsed accuracy {accuracy} is not between 0 and 1."
    # Given the clear separation of the dataset, accuracy should be very high
    assert accuracy > 0.8, f"Expected a high accuracy (>0.8) for this simple task, but got {accuracy}."