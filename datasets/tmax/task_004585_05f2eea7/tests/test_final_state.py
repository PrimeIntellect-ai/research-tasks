# test_final_state.py

import os
import json
import hashlib
import subprocess
import pytest

def test_pipeline_script_exists():
    script_path = "/home/user/clean_pipeline.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_cron_job_configured():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it configured for the user?")

    expected_cron = "0 2 * * * /usr/bin/python3 /home/user/clean_pipeline.py"

    # Check if the expected cron job is in the crontab output
    cron_lines = [line.strip() for line in crontab_output.strip().split("\n")]
    assert any(expected_cron in line for line in cron_lines), "The expected cron job is not configured correctly."

def test_output_file_exists_and_correct():
    output_path = "/home/user/clean_data/deduped_output.jsonl"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    expected_texts = {
        "Hello World",
        "Data Science",
        "Café",
        "Hola",
        "Python",
        "おはよう"
    }

    actual_texts = set()
    records = []

    with open(output_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {output_path} is not valid JSON.")

            assert "hash" in record, f"Record on line {line_num} missing 'hash' key."
            assert "text" in record, f"Record on line {line_num} missing 'text' key."
            assert len(record) == 2, f"Record on line {line_num} has extra keys."

            text = record["text"]
            text_hash = record["hash"]

            expected_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
            assert text_hash == expected_hash, f"Hash for text '{text}' is incorrect. Expected {expected_hash}, got {text_hash}."

            actual_texts.add(text)
            records.append(record)

    assert len(records) == len(expected_texts), f"Expected exactly {len(expected_texts)} records, but found {len(records)}."
    assert actual_texts == expected_texts, f"The deduplicated texts do not match the expected set. Missing: {expected_texts - actual_texts}. Unexpected: {actual_texts - expected_texts}."