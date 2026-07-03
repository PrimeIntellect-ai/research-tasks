# test_final_state.py
import os
import json
import hashlib
import re

LOG_DIR = "/home/user/logs"
OUTPUT_FILE = "/home/user/hourly_errors.json"
SCRIPT_FILE = "/home/user/analyze_logs.py"

def test_script_exists_and_uses_parallelism():
    assert os.path.isfile(SCRIPT_FILE), f"Script {SCRIPT_FILE} does not exist."
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    has_multiprocessing = "multiprocessing" in content
    has_concurrent = "concurrent.futures" in content
    assert has_multiprocessing or has_concurrent, "Script must use 'multiprocessing' or 'concurrent.futures' for parallel processing."

def test_json_output_content_and_format():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."

    # Compute expected output dynamically from the actual log files
    expected = {}
    pattern = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}):\d{2}:\d{2}\]\s+(\w+)\s+(.*)$")

    if os.path.isdir(LOG_DIR):
        for filename in os.listdir(LOG_DIR):
            if not filename.endswith(".log"):
                continue
            filepath = os.path.join(LOG_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    match = pattern.match(line.strip())
                    if match:
                        hour_prefix, level, message = match.groups()
                        if level == "ERROR":
                            bucket = f"{hour_prefix}:00:00"
                            msg_hash = hashlib.md5(message.strip().encode('utf-8')).hexdigest()
                            if bucket not in expected:
                                expected[bucket] = set()
                            expected[bucket].add(msg_hash)

    # Format expected data structure
    expected_formatted = {k: sorted(list(v)) for k, v in expected.items()}

    # Read actual JSON
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        raw_content = f.read()
        try:
            actual = json.loads(raw_content)
        except json.JSONDecodeError:
            assert False, f"{OUTPUT_FILE} is not a valid JSON file."

    # Assert data correctness
    assert actual == expected_formatted, f"JSON content does not match expected output.\nExpected: {expected_formatted}\nActual: {actual}"

    # Assert formatting (indent=2, sorted keys)
    expected_str = json.dumps(expected_formatted, indent=2, sort_keys=True)
    assert raw_content.strip() == expected_str.strip(), "JSON formatting does not match expected (ensure indent=2 and sorted keys/lists)."