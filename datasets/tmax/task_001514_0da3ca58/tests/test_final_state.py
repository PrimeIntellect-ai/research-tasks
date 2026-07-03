# test_final_state.py

import os
import json
import pytest

def test_process_script_exists():
    script_path = "/home/user/process.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_symbolic_links_accuracy():
    json_path = "/tmp/expected_mapping.json"
    assert os.path.exists(json_path), f"The expected mapping file {json_path} does not exist."

    with open(json_path, 'r') as f:
        expected = json.load(f)

    correct_links = 0
    total_expected = len(expected)

    assert total_expected > 0, "No expected mappings found in /tmp/expected_mapping.json."

    for exp in expected:
        date_str = exp['date']
        cfg_id = exp['id']
        expected_link = f"/home/user/tracked_configs/{date_str}/config_{cfg_id}.bin"
        expected_target = f"/home/user/compiled/{exp['basename']}.bin"

        if os.path.islink(expected_link):
            target = os.readlink(expected_link)
            if target == expected_target or target == expected_target.replace('//', '/'):
                correct_links += 1
        else:
            # Check if it's a file instead of a link, or doesn't exist
            if not os.path.exists(expected_link):
                pass # Link is missing

    accuracy = correct_links / total_expected

    assert accuracy >= 1.0, f"Expected 100% accuracy, got {accuracy * 100}%. Correct links: {correct_links}/{total_expected}."