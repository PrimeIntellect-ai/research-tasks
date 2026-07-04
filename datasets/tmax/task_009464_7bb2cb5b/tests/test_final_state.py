# test_final_state.py

import os
import json
import stat

def test_merged_output_exists_and_content():
    output_path = '/home/user/merged_output.jsonl'
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    with open(output_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {output_path}, found {len(lines)}"

    expected_data = {
        101: {
            "review_timestamp_iso": "2023-01-05T14:00:00Z",
            "text_decoded": "Great app! ❤",
            "log_action": "login"
        },
        102: {
            "review_timestamp_iso": "2023-01-05T15:30:00Z",
            "text_decoded": "Broken 😭",
            "log_action": "update"
        },
        103: {
            "review_timestamp_iso": "2023-01-05T16:45:00Z",
            "text_decoded": "Me gusta la aplicación",
            "log_action": "logout"
        }
    }

    found_users = set()
    for line in lines:
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line in {output_path} is not valid JSON: {line}"

        assert "user_id" in obj, "Missing 'user_id' in output object"
        user_id = obj["user_id"]
        assert user_id in expected_data, f"Unexpected user_id {user_id} in output"
        found_users.add(user_id)

        expected = expected_data[user_id]
        assert obj.get("review_timestamp_iso") == expected["review_timestamp_iso"], f"Incorrect timestamp for user {user_id}"
        assert obj.get("text_decoded") == expected["text_decoded"], f"Incorrect decoded text for user {user_id}"
        assert obj.get("log_action") == expected["log_action"], f"Incorrect log action for user {user_id}"

        # Ensure exactly these keys are present
        expected_keys = {"user_id", "review_timestamp_iso", "text_decoded", "log_action"}
        assert set(obj.keys()) == expected_keys, f"Object for user {user_id} has incorrect keys: {set(obj.keys())}"

    assert found_users == set(expected_data.keys()), "Missing expected users in output"

def test_run_pipeline_script():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"Wrapper script missing: {script_path}"

    # Check if executable
    assert os.access(script_path, os.X_OK), f"Wrapper script is not executable: {script_path}"

    # Check content roughly
    with open(script_path, 'r') as f:
        content = f.read()

    assert "python" in content, "Wrapper script does not seem to invoke python"
    assert "pipeline.py" in content, "Wrapper script does not seem to invoke pipeline.py"

def test_crontab_txt():
    crontab_path = '/home/user/crontab.txt'
    assert os.path.isfile(crontab_path), f"Crontab file missing: {crontab_path}"

    with open(crontab_path, 'r') as f:
        content = f.read().strip()

    # The expected cron expression is 30 2 * * * /home/user/run_pipeline.sh
    parts = content.split()
    assert len(parts) >= 6, "Crontab entry does not have enough fields"
    assert parts[0] == "30", "Minute field in crontab should be 30"
    assert parts[1] == "2", "Hour field in crontab should be 2"
    assert parts[2] == "*", "Day of month field should be *"
    assert parts[3] == "*", "Month field should be *"
    assert parts[4] == "*", "Day of week field should be *"

    command = " ".join(parts[5:])
    assert "/home/user/run_pipeline.sh" in command, "Command in crontab does not execute the wrapper script"