# test_final_state.py
import os
import json
import pytest

RAW_FILE = "/home/user/raw_configs.jsonl"
CLEAN_FILE = "/home/user/clean_configs.jsonl"

def test_clean_configs_exists():
    """Verify that the clean configuration output file exists."""
    assert os.path.exists(CLEAN_FILE), f"Output file {CLEAN_FILE} does not exist."
    assert os.path.isfile(CLEAN_FILE), f"{CLEAN_FILE} is not a file."
    assert os.path.getsize(CLEAN_FILE) > 0, f"{CLEAN_FILE} is empty."

def test_unicode_unescaped():
    """Verify that Unicode characters are not escaped in the output file."""
    with open(CLEAN_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # If ensure_ascii=True was used, we would see \uXXXX instead of actual characters
    # We know the input has characters like Веб-сервер, 缓存, قاعدة البيانات
    assert "Веб-сервер" in content or "缓存" in content or "قاعدة البيانات" in content, \
        "Output file does not contain literal Unicode characters. Did you use ensure_ascii=False?"

def test_output_correctness_and_sorting():
    """Verify the deduplication, filtering, and sorting logic against the raw file."""
    assert os.path.exists(RAW_FILE), f"{RAW_FILE} is missing, cannot verify."

    # 1. Compute expected truth
    records = []
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    valid = [r for r in records if r.get("config_data", {}).get("app_name") is not None]

    dedup = {}
    for r in valid:
        cd_str = json.dumps(r["config_data"], sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        key = r["server_id"] + "||" + cd_str

        if key not in dedup:
            dedup[key] = r
        else:
            if r["timestamp"] < dedup[key]["timestamp"]:
                dedup[key] = r

    expected_records = list(dedup.values())
    expected_records.sort(key=lambda x: (x["server_id"], x["timestamp"]))

    # 2. Read actual output
    actual_records = []
    with open(CLEAN_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                actual_records.append(json.loads(line))
            except json.JSONDecodeError:
                pytest.fail(f"Line {i+1} in {CLEAN_FILE} is not valid JSON.")

    # 3. Compare lengths
    assert len(actual_records) == len(expected_records), \
        f"Expected {len(expected_records)} records, but found {len(actual_records)}."

    # 4. Compare records and their order
    for i, (actual, expected) in enumerate(zip(actual_records, expected_records)):
        assert actual == expected, \
            f"Record mismatch at line {i+1}.\nExpected: {expected}\nActual: {actual}\n" \
            "Make sure records are deduplicated correctly (minimum timestamp) and sorted by server_id then timestamp."

    # 5. Check validation checkpoint explicitly on actual records
    for i, r in enumerate(actual_records):
        config_data = r.get("config_data", {})
        assert "app_name" in config_data, f"Record at line {i+1} is missing 'app_name' in 'config_data'."
        assert config_data["app_name"] is not None, f"Record at line {i+1} has null 'app_name'."