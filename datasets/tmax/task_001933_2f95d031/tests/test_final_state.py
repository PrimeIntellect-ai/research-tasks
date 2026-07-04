# test_final_state.py
import os
import json

def test_sampled_events_file():
    file_path = '/home/user/sampled_events.jsonl'

    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    line_count = 0
    actions_count = {"view": 0, "click": 0, "purchase": 0}

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    assert False, f"Invalid JSON on line {line_count + 1} in {file_path}."

                assert "user_id" in record, "Missing user_id in sampled record."
                assert "item_id" in record, "Missing item_id in sampled record."
                assert "action" in record, "Missing action in sampled record."
                assert "timestamp" in record, "Missing timestamp in sampled record."

                action = record["action"]
                assert action in actions_count, f"Invalid normalized action '{action}' found."
                actions_count[action] += 1

                line_count += 1

    assert line_count == 280, f"Expected exactly 280 lines in {file_path}, but found {line_count}."
    assert actions_count["view"] == 100, f"Expected 100 views, found {actions_count['view']}."
    assert actions_count["click"] == 100, f"Expected 100 clicks, found {actions_count['click']}."
    assert actions_count["purchase"] == 80, f"Expected 80 purchases, found {actions_count['purchase']}."

def test_pipeline_run_log():
    file_path = '/home/user/pipeline_run.json'

    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    with open(file_path, 'r') as f:
        try:
            log_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {file_path} is not valid JSON."

    expected_data = {
        "records_read": 580,
        "dropped_missing_fields": 20,
        "dropped_unknown_action": 15,
        "duplicates_removed": 15,
        "final_counts": {
            "view": 100,
            "click": 100,
            "purchase": 80
        }
    }

    assert log_data == expected_data, f"Pipeline log data does not match expected output. Got: {log_data}"