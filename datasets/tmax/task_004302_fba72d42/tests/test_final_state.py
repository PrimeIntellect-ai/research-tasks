# test_final_state.py

import os
import json

def test_deadlock_report_exists_and_correct():
    report_path = "/home/user/deadlock_report.json"

    # Check if the output file exists
    assert os.path.isfile(report_path), f"The output file {report_path} was not found."

    # Read and parse the JSON file
    try:
        with open(report_path, 'r') as f:
            actual_data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"The file {report_path} does not contain valid JSON."
    except Exception as e:
        assert False, f"Error reading {report_path}: {e}"

    # Verify the structure and content
    assert isinstance(actual_data, list), f"The JSON in {report_path} should be an array."

    expected_cycle = ["TXN-209", "TXN-314", "TXN-402", "TXN-550", "TXN-881"]

    # Verify it matches the expected cycle exactly (including sorted order)
    assert actual_data == expected_cycle, (
        f"The deadlock report content is incorrect.\n"
        f"Expected: {expected_cycle}\n"
        f"Actual:   {actual_data}"
    )