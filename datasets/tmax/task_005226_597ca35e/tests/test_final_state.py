# test_final_state.py
import os
import json
import re

def test_output_json_exists_and_correct():
    output_path = "/home/user/output/region_stats.json"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {output_path} does not contain valid JSON."

    expected = {
        "NA": 5.0,
        "EU": 3.0,
        "APAC": 2.0
    }

    # Check if keys match
    assert set(data.keys()) == set(expected.keys()), f"Keys in JSON do not match expected regions. Got {list(data.keys())}"

    # Check values with a small tolerance for floating point issues, though it should be exact
    for region, expected_val in expected.items():
        val = data[region]
        assert isinstance(val, (int, float)), f"Value for {region} is not a number."
        assert abs(val - expected_val) < 0.01, f"Average word count for {region} is incorrect. Expected {expected_val}, got {val}"

def test_cron_backup_exists_and_correct():
    backup_path = "/home/user/cron_backup.txt"
    assert os.path.isfile(backup_path), f"Cron backup file {backup_path} does not exist."

    with open(backup_path, "r") as f:
        content = f.read().strip()

    # Look for 0 2 * * * and python3 /home/user/etl_pipeline.py
    # Allowing multiple spaces
    pattern = r"0\s+2\s+\*\s+\*\s+\*\s+python3\s+/home/user/etl_pipeline\.py"
    match = re.search(pattern, content)
    assert match is not None, f"Cron backup does not contain the correct cron schedule and command. Got: {content}"

def test_etl_script_exists_and_uses_multiprocessing():
    script_path = "/home/user/etl_pipeline.py"
    assert os.path.isfile(script_path), f"ETL script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "multiprocessing" in content or "Pool" in content, "ETL script does not appear to use the multiprocessing module."