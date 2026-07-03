# test_final_state.py

import os
import json
import pytest

def test_merged_timeline_exists():
    assert os.path.isfile('/home/user/merged_timeline.json'), "The file /home/user/merged_timeline.json does not exist. Did the script run successfully?"

def test_merged_timeline_content():
    with open('/home/user/merged_timeline.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/merged_timeline.json does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output should be a list of records."

    # Check length: 10 from service_A + 9 valid from service_B = 19
    assert len(data) == 19, f"Expected 19 records in the merged timeline, but found {len(data)}."

    # Check for no negative timestamps and no value 999 (the corrupted record)
    for record in data:
        assert 'timestamp' in record, "Record is missing 'timestamp' key."
        assert 'value' in record, "Record is missing 'value' key."
        assert record['timestamp'] >= 0, f"Found a record with a negative timestamp: {record}"
        assert record['value'] != 999, f"Found the corrupted record with value 999: {record}"

    # Check sorting
    timestamps = [record['timestamp'] for record in data]
    assert timestamps == sorted(timestamps), "The records in the merged timeline are not sorted by timestamp in ascending order."