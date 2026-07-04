# test_final_state.py

import os
import json
import pytest

def test_output_json_exists_and_valid():
    output_file = '/home/user/output.json'
    assert os.path.isfile(output_file), f"The output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_file} does not contain valid JSON.")

    assert isinstance(data, list), "The output JSON should be a list of user objects."
    assert len(data) == 5, f"The output JSON should contain exactly 5 users, but found {len(data)}."

def test_output_json_content():
    output_file = '/home/user/output.json'
    assert os.path.isfile(output_file), f"The output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        data = json.load(f)

    users_by_id = {str(user.get('id')): user for user in data}

    # Check Charlie (id 3)
    assert '3' in users_by_id, "User with id '3' (Charlie) is missing from the output."
    assert users_by_id['3'].get('theme') == 'light', "User with id '3' (Charlie) should have theme 'light'."

    # Check Eve (id 5)
    assert '5' in users_by_id, "User with id '5' (Eve) is missing from the output."
    assert users_by_id['5'].get('theme') == 'light', "User with id '5' (Eve) should have theme 'light'."

def test_bug_report_txt():
    bug_report_file = '/home/user/bug_report.txt'
    assert os.path.isfile(bug_report_file), f"The file {bug_report_file} does not exist."

    with open(bug_report_file, 'r') as f:
        content = f.read().strip()

    assert content == '3', f"The bug_report.txt should contain exactly '3', but found '{content}'."