# test_final_state.py

import os
import json
import pytest

def test_lineage_script_exists():
    """Verify that the lineage.py script was created."""
    script_path = "/home/user/lineage.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_report_json_exists():
    """Verify that the report.json file was generated."""
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"The output file {report_path} was not created."

def test_report_json_content():
    """Verify the content of the generated report.json file."""
    report_path = "/home/user/report.json"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert "shortest_time" in data, "The key 'shortest_time' is missing from report.json."
    assert "ancestors" in data, "The key 'ancestors' is missing from report.json."

    expected_shortest_time = 27
    expected_ancestors = ["Alpha", "Beta", "Delta", "Epsilon", "Gamma"]

    assert data["shortest_time"] == expected_shortest_time, \
        f"Expected shortest_time to be {expected_shortest_time}, but got {data['shortest_time']}."

    assert isinstance(data["ancestors"], list), "The 'ancestors' value should be a list."
    assert sorted(data["ancestors"]) == expected_ancestors, \
        f"Expected ancestors to be {expected_ancestors}, but got {sorted(data['ancestors'])}."