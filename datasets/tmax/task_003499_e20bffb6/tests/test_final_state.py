# test_final_state.py
import os
import json

def test_deadlock_report_exists():
    assert os.path.isfile('/home/user/etl_project/deadlock_report.json'), "The deadlock_report.json file was not found in /home/user/etl_project."

def test_deadlock_report_content():
    with open('/home/user/etl_project/deadlock_report.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "deadlock_report.json is not a valid JSON file."

    assert isinstance(data, list), "The root of the JSON file must be an array."
    assert len(data) == 3, f"Expected 3 cycles in the report, found {len(data)}."

    expected_data = [
        {
            "cycle": ["T10", "T11"],
            "max_wait_tx": "T10",
            "total_wait_ms": 1000
        },
        {
            "cycle": ["T4", "T5", "T6"],
            "max_wait_tx": "T6",
            "total_wait_ms": 800
        },
        {
            "cycle": ["T1", "T2", "T3"],
            "max_wait_tx": "T2",
            "total_wait_ms": 350
        }
    ]

    for i, expected_cycle in enumerate(expected_data):
        actual_cycle = data[i]
        assert "cycle" in actual_cycle, f"Missing 'cycle' key in item {i}."
        assert "max_wait_tx" in actual_cycle, f"Missing 'max_wait_tx' key in item {i}."
        assert "total_wait_ms" in actual_cycle, f"Missing 'total_wait_ms' key in item {i}."

        assert isinstance(actual_cycle["cycle"], list), f"'cycle' should be a list in item {i}."
        assert sorted(actual_cycle["cycle"]) == actual_cycle["cycle"], f"'cycle' array is not sorted alphabetically in item {i}."
        assert actual_cycle["cycle"] == expected_cycle["cycle"], f"Expected cycle {expected_cycle['cycle']}, got {actual_cycle['cycle']} at index {i}."

        assert actual_cycle["max_wait_tx"] == expected_cycle["max_wait_tx"], f"Expected max_wait_tx {expected_cycle['max_wait_tx']}, got {actual_cycle['max_wait_tx']} at index {i}."
        assert actual_cycle["total_wait_ms"] == expected_cycle["total_wait_ms"], f"Expected total_wait_ms {expected_cycle['total_wait_ms']}, got {actual_cycle['total_wait_ms']} at index {i}."