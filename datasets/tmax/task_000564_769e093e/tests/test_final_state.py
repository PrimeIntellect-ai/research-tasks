# test_final_state.py
import os
import json
import pytest

def test_process_subs_cpp_exists():
    assert os.path.exists("/home/user/process_subs.cpp"), "/home/user/process_subs.cpp does not exist. You must write your solution in this file."

def test_subs_normalized_jsonl():
    output_file = "/home/user/subs_normalized.jsonl"
    assert os.path.exists(output_file), f"{output_file} does not exist. Did you run your compiled program?"

    expected = [
        {"start_sec": 0, "end_sec": 3, "speaker": "NARRATOR", "text": "hola mundo we begin now"},
        {"start_sec": 3, "end_sec": 6, "speaker": "NARRATOR", "text": "welcome to the lección"},
        {"start_sec": 6, "end_sec": 9, "speaker": "SYS", "text": "[SILENCE]"},
        {"start_sec": 9, "end_sec": 11, "speaker": "GUEST", "text": "this is emocionante right"},
        {"start_sec": 11, "end_sec": 14, "speaker": "GUEST", "text": "i am listo"},
        {"start_sec": 14, "end_sec": 17, "speaker": "SYS", "text": "[SILENCE]"},
        {"start_sec": 17, "end_sec": 20, "speaker": "NARRATOR", "text": "let us continuar"}
    ]

    with open(output_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected), f"Expected {len(expected)} records in {output_file}, but found {len(lines)}."

    for i, (line, exp) in enumerate(zip(lines, expected)):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {output_file} is not valid JSON: {line}")

        assert parsed == exp, f"Line {i+1} mismatch.\nExpected: {exp}\nGot:      {parsed}"