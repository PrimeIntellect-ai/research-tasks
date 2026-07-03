# test_final_state.py

import os
import json
import stat
import pytest
import re

def test_pipeline_script_executable():
    script_path = '/home/user/pipeline.sh'
    assert os.path.isfile(script_path), f"Pipeline script not found at {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Pipeline script {script_path} is not executable"

def test_crontab_entry():
    crontab_path = '/home/user/crontab.txt'
    assert os.path.isfile(crontab_path), f"Crontab file not found at {crontab_path}"

    with open(crontab_path, 'r') as f:
        content = f.read().strip()

    # Check for every 5 minutes schedule
    # Accept formats like "*/5 * * * * /home/user/pipeline.sh" or "0,5,10... * * * * /home/user/pipeline.sh"
    # A simple regex for */5 * * * * /home/user/pipeline.sh
    match = re.search(r'(?:\*/5|0,5,10,15,20,25,30,35,40,45,50,55)\s+\*\s+\*\s+\*\s+\*\s+/home/user/pipeline\.sh', content)
    assert match is not None, f"Crontab entry does not match the expected schedule for /home/user/pipeline.sh every 5 minutes. Found: {content}"

def test_stats_json_correctness():
    stats_path = '/home/user/stats.json'
    assert os.path.isfile(stats_path), f"Stats JSON file not found at {stats_path}"

    with open(stats_path, 'r') as f:
        try:
            stats = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {stats_path} is not valid JSON")

    expected_stats = {
        "2023-10-01T10:00:00Z": {
            "total_requests": 1,
            "error_rate": 0.0000,
            "avg_response_size": 500.0
        },
        "2023-10-01T10:01:00Z": {
            "total_requests": 2,
            "error_rate": 0.5000,
            "avg_response_size": 350.0
        },
        "2023-10-01T10:02:00Z": {
            "total_requests": 3,
            "error_rate": 0.3333,
            "avg_response_size": 566.7
        },
        "2023-10-01T10:03:00Z": {
            "total_requests": 4,
            "error_rate": 0.2500,
            "avg_response_size": 575.0
        },
        "2023-10-01T10:04:00Z": {
            "total_requests": 5,
            "error_rate": 0.4000,
            "avg_response_size": 510.0
        },
        "2023-10-01T10:05:00Z": {
            "total_requests": 5,
            "error_rate": 0.4000,
            "avg_response_size": 630.0
        }
    }

    for minute, expected in expected_stats.items():
        assert minute in stats, f"Missing expected minute key {minute} in stats.json"
        actual = stats[minute]

        assert actual.get("total_requests") == expected["total_requests"], \
            f"Incorrect total_requests for {minute}. Expected {expected['total_requests']}, got {actual.get('total_requests')}"

        assert abs(actual.get("error_rate", -1) - expected["error_rate"]) < 0.0002, \
            f"Incorrect error_rate for {minute}. Expected {expected['error_rate']}, got {actual.get('error_rate')}"

        assert abs(actual.get("avg_response_size", -1) - expected["avg_response_size"]) < 0.2, \
            f"Incorrect avg_response_size for {minute}. Expected {expected['avg_response_size']}, got {actual.get('avg_response_size')}"