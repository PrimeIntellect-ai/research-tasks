# test_final_state.py

import os
import json

def test_recovered_file_exists():
    path = '/home/user/recovered_metrics.log'
    assert os.path.exists(path), f"The recovered log file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, 'r') as f:
        content = f.read()

    # Check that it contains at least one of the known valid lines
    assert '{"host": "web-01", "uptime_ms": 5000}' in content, "The recovered log file does not contain the expected metrics data."

def test_total_uptime_json():
    path = '/home/user/total_uptime.json'
    assert os.path.exists(path), f"The output file {path} is missing. Did you run the aggregator script?"

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {path} does not contain valid JSON."

    assert "total_uptime_ms" in data, f"Key 'total_uptime_ms' is missing in {path}."

    expected_uptime = 5000 + 7500 + 12000 + 3000
    actual_uptime = data["total_uptime_ms"]

    assert actual_uptime == expected_uptime, f"Expected total_uptime_ms to be {expected_uptime}, but got {actual_uptime}."