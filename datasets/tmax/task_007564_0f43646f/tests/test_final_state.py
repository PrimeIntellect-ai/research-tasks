# test_final_state.py
import os
import json
from decimal import Decimal

def test_processed_logs_exists():
    path = "/home/user/processed_logs.jsonl"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the script?"

def test_processed_logs_content():
    path = "/home/user/processed_logs.jsonl"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3, f"Expected exactly 3 lines in {path}, found {len(lines)}"

    # We use Decimal to check exact values without float precision loss
    parsed_lines = [json.loads(line, parse_float=Decimal) for line in lines]

    # Line 1
    assert parsed_lines[0]['timestamp'] == Decimal("1700000000.1234567890123456789"), "Precision loss in timestamp on line 1."
    assert parsed_lines[0]['payload'] == {"data": "critical_event_1"}, "Payload not correctly unwrapped on line 1."
    assert parsed_lines[0].get('decoded_msg') == "Hello World", "Base64 decoding failed or incorrect on line 1."

    # Line 2
    assert parsed_lines[1]['timestamp'] == Decimal("1700000005.9876543210987654321"), "Precision loss in timestamp on line 2."
    assert parsed_lines[1]['payload'] == {"data": "critical_event_2"}, "Payload not correctly unwrapped on line 2."
    assert parsed_lines[1].get('decoded_msg') == "agent activated", "Base64 decoding failed or incorrect on line 2."

    # Line 3
    assert parsed_lines[2]['timestamp'] == Decimal("1700000010.5555555555555555555"), "Precision loss in timestamp on line 3."
    assert parsed_lines[2]['payload'] == {"data": "critical_event_3"}, "Payload not correctly unwrapped on line 3."
    assert parsed_lines[2].get('decoded_msg') == "padding issue", "Base64 decoding failed or incorrect on line 3."

def test_processed_logs_raw_strings():
    # Double check that the raw strings contain the exact float representation
    path = "/home/user/processed_logs.jsonl"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3
    assert "1700000000.1234567890123456789" in lines[0], "Exact timestamp string missing in line 1 output."
    assert "1700000005.9876543210987654321" in lines[1], "Exact timestamp string missing in line 2 output."
    assert "1700000010.5555555555555555555" in lines[2], "Exact timestamp string missing in line 3 output."