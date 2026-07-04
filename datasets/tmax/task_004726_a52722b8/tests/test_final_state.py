# test_final_state.py
import os
import json
import pytest

def test_output_exists_and_correct():
    path = "/home/user/output.jsonl"
    assert os.path.exists(path), f"Output file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    expected = [
        {"session_id": "S1", "normalized_message": "Hello こんにちは", "chat_ts": 1696154400, "tx_sum": 15.5},
        {"session_id": "S2", "normalized_message": "Foo IV", "chat_ts": 1696154460, "tx_sum": 20.0},
        {"session_id": "S1", "normalized_message": "Bye", "chat_ts": 1696154700, "tx_sum": 9.9}
    ]

    actual = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    actual.append(json.loads(line))
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON line in {path}: {line}")

    assert len(actual) == len(expected), f"Expected {len(expected)} lines in output, got {len(actual)}."

    for i, (act, exp) in enumerate(zip(actual, expected)):
        assert act.get("session_id") == exp["session_id"], \
            f"Line {i+1}: expected session_id '{exp['session_id']}', got '{act.get('session_id')}'"
        assert act.get("normalized_message") == exp["normalized_message"], \
            f"Line {i+1}: expected normalized_message '{exp['normalized_message']}', got '{act.get('normalized_message')}'"
        assert act.get("chat_ts") == exp["chat_ts"], \
            f"Line {i+1}: expected chat_ts {exp['chat_ts']}, got {act.get('chat_ts')}"
        assert act.get("tx_sum") == pytest.approx(exp["tx_sum"]), \
            f"Line {i+1}: expected tx_sum {exp['tx_sum']}, got {act.get('tx_sum')}"