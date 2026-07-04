# test_final_state.py
import os
import json
import unicodedata

OUTPUT_PATH = "/home/user/processed_logs.jsonl"

def test_output_file_exists():
    assert os.path.exists(OUTPUT_PATH), f"The output file {OUTPUT_PATH} does not exist."
    assert os.path.isfile(OUTPUT_PATH), f"{OUTPUT_PATH} is not a file."

def test_output_file_content_and_format():
    if not os.path.exists(OUTPUT_PATH):
        return  # Handled by test_output_file_exists

    with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content, f"The output file {OUTPUT_PATH} is empty."
    lines = content.split('\n')

    assert len(lines) == 5, f"Expected exactly 5 lines in the output file, got {len(lines)}."

    expected_data = [
        {"timestamp": "2023-10-01T10:00:00.000Z", "message": "System startup."},
        {"timestamp": "2023-10-01T10:00:01.000Z", "message": "CPU temp is high: 95°C."},
        {"timestamp": "2023-10-01T10:00:02.000Z", "message": "Warning: fan speed – critical!"},
        {"timestamp": "2023-10-01T10:00:03.000Z", "message": "System stabilized."},
        {"timestamp": "2023-10-01T10:00:04.000Z", "message": "User ä logged in."}
    ]

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} is not valid JSON: {line}"

        assert "timestamp" in data, f"Line {i+1} missing 'timestamp' key."
        assert "message" in data, f"Line {i+1} missing 'message' key."
        assert len(data.keys()) == 2, f"Line {i+1} has incorrect number of keys: {list(data.keys())}. Expected exactly 'timestamp' and 'message'."

        actual_ts = data["timestamp"]
        expected_ts = expected_data[i]["timestamp"]
        assert actual_ts == expected_ts, f"Line {i+1} has incorrect timestamp. Expected '{expected_ts}', got '{actual_ts}'."

        actual_msg = data["message"]
        expected_msg = expected_data[i]["message"]
        assert actual_msg == expected_msg, f"Line {i+1} has incorrect message. Expected '{expected_msg}', got '{actual_msg}'."

        # Verify Unicode Normalization Form C (NFC)
        assert unicodedata.is_normalized('NFC', actual_msg), f"Line {i+1} message is not NFC normalized."