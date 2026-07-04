# test_final_state.py
import os
import json
import pytest

def test_script_exists_and_uses_atomic_write():
    script_path = "/home/user/process_artifacts.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for atomic write indicators
    atomic_methods = ["os.rename", "os.replace", "shutil.move"]
    has_atomic = any(method in content for method in atomic_methods)
    assert has_atomic, f"Script {script_path} does not appear to use an atomic write method (os.rename, os.replace, or shutil.move)."

def test_output_file_exists_and_content_correct():
    output_path = "/home/user/artifact_repo/magic_numbers.jsonl"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    expected_data = [
        {"file": "/home/user/artifact_repo/image.png", "magic_hex": "89504e47"},
        {"file": "/home/user/artifact_repo/java.class", "magic_hex": "cafebabe"},
        {"file": "/home/user/artifact_repo/binary.elf", "magic_hex": "7f454c46"}
    ]

    actual_data = []
    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                actual_data.append(json.loads(line))
            except json.JSONDecodeError:
                pytest.fail(f"Line in {output_path} is not valid JSON: {line}")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Record at line {i+1} is incorrect. Expected {expected}, got {actual}."