# test_final_state.py
import os
import json
import pytest

APP_DIR = "/home/user/app"
RECOMMENDATIONS_FILE = os.path.join(APP_DIR, "recommendations.json")
EXPERIMENT_LOG_FILE = os.path.join(APP_DIR, "experiment_log.json")

def test_recommendations_file_exists_and_correct():
    assert os.path.isfile(RECOMMENDATIONS_FILE), f"The file {RECOMMENDATIONS_FILE} was not generated."

    with open(RECOMMENDATIONS_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RECOMMENDATIONS_FILE} does not contain valid JSON.")

    expected_mapping = {
        "q1": "t1",
        "q2": "t3"
    }

    assert data == expected_mapping, f"The recommendations mapping is incorrect. Expected {expected_mapping}, but got {data}."

def test_experiment_log_exists_and_logged():
    assert os.path.isfile(EXPERIMENT_LOG_FILE), f"The file {EXPERIMENT_LOG_FILE} was not generated. Did you run track_experiment.sh?"

    with open(EXPERIMENT_LOG_FILE, 'r') as f:
        content = f.read()

    # Since track_experiment.sh appends the JSON, we can check if the expected output is part of the log
    assert '"q1"' in content and '"t1"' in content, f"The experiment log does not seem to contain the expected 'q1' -> 't1' mapping."
    assert '"q2"' in content and '"t3"' in content, f"The experiment log does not seem to contain the expected 'q2' -> 't3' mapping."