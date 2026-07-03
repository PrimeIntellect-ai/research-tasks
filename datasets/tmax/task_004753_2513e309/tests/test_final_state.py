# test_final_state.py

import os
import json
import re
import subprocess
import pytest

EVIL_CORPUS_DIR = "/home/user/verifier/evil_corpus"
CLEAN_CORPUS_DIR = "/home/user/verifier/clean_corpus"
EVIL_OUT_DIR = "/home/user/verifier/evil_out"
CLEAN_OUT_DIR = "/home/user/verifier/clean_out"
ETL_SCRIPT = "/home/user/etl_pipeline.py"
LOG_FILE = "/home/user/etl.log"
MAGIC_STRING = "[MASKED_PII_STRICT_v9]"
SSN_REGEX = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

def get_expected_records(corpus_dir, mask=False):
    records = {}
    if not os.path.isdir(corpus_dir):
        return []

    for filename in os.listdir(corpus_dir):
        if not filename.endswith('.json'):
            continue
        filepath = os.path.join(corpus_dir, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            for record in data:
                rec_id = record.get('record_id')
                timestamp = record.get('timestamp', 0)

                if mask:
                    if 'notes' in record and isinstance(record['notes'], str):
                        record['notes'] = SSN_REGEX.sub(MAGIC_STRING, record['notes'])
                    if 'user_data' in record and isinstance(record['user_data'], str):
                        record['user_data'] = SSN_REGEX.sub(MAGIC_STRING, record['user_data'])

                if rec_id not in records or records[rec_id]['timestamp'] < timestamp:
                    records[rec_id] = record

    return list(records.values())

def test_cron_job():
    """Test that the cron job is correctly configured."""
    try:
        output = subprocess.check_output(['crontab', '-l', '-u', 'user'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to retrieve crontab for user 'user'.")

    expected_cron = r"\*/5\s+\*\s+\*\s+\*\s+\*\s+python3\s+/home/user/etl_pipeline\.py\s+/home/user/incoming\s+/home/user/processed"
    assert re.search(expected_cron, output), f"Cron job not found or incorrectly configured. Crontab: {output}"

def test_evil_corpus():
    """Test the ETL script against the evil corpus."""
    assert os.path.isfile(ETL_SCRIPT), f"ETL script {ETL_SCRIPT} does not exist."
    os.makedirs(EVIL_OUT_DIR, exist_ok=True)

    try:
        subprocess.run(['python3', ETL_SCRIPT, EVIL_CORPUS_DIR, EVIL_OUT_DIR], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"ETL script failed on evil corpus: {e.stderr}")

    output_file = os.path.join(EVIL_OUT_DIR, 'processed_batch.json')
    assert os.path.isfile(output_file), f"Output file {output_file} was not created."

    with open(output_file, 'r') as f:
        actual_records = json.load(f)

    expected_records = get_expected_records(EVIL_CORPUS_DIR, mask=True)

    actual_dict = {r.get('record_id'): r for r in actual_records}
    expected_dict = {r.get('record_id'): r for r in expected_records}

    bypassed = []
    for rec_id, expected_rec in expected_dict.items():
        if rec_id not in actual_dict:
            bypassed.append(f"Missing record_id {rec_id}")
            continue

        actual_rec = actual_dict[rec_id]
        if actual_rec != expected_rec:
            bypassed.append(f"Record {rec_id} mismatch. Expected: {expected_rec}, Actual: {actual_rec}")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(expected_dict)} evil records bypassed or incorrect:\n" + "\n".join(bypassed[:10]))

def test_clean_corpus():
    """Test the ETL script against the clean corpus."""
    assert os.path.isfile(ETL_SCRIPT), f"ETL script {ETL_SCRIPT} does not exist."
    os.makedirs(CLEAN_OUT_DIR, exist_ok=True)

    try:
        subprocess.run(['python3', ETL_SCRIPT, CLEAN_CORPUS_DIR, CLEAN_OUT_DIR], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"ETL script failed on clean corpus: {e.stderr}")

    output_file = os.path.join(CLEAN_OUT_DIR, 'processed_batch.json')
    assert os.path.isfile(output_file), f"Output file {output_file} was not created."

    with open(output_file, 'r') as f:
        actual_records = json.load(f)

    expected_records = get_expected_records(CLEAN_CORPUS_DIR, mask=False)

    actual_dict = {r.get('record_id'): r for r in actual_records}
    expected_dict = {r.get('record_id'): r for r in expected_records}

    modified = []
    for rec_id, expected_rec in expected_dict.items():
        if rec_id not in actual_dict:
            modified.append(f"Missing record_id {rec_id}")
            continue

        actual_rec = actual_dict[rec_id]
        if actual_rec != expected_rec:
            modified.append(f"Record {rec_id} mismatch. Expected: {expected_rec}, Actual: {actual_rec}")

    if modified:
        pytest.fail(f"{len(modified)} of {len(expected_dict)} clean records modified or incorrect:\n" + "\n".join(modified[:10]))

def test_log_file():
    """Test that the log file is correctly formatted."""
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."

    with open(LOG_FILE, 'r') as f:
        logs = f.readlines()

    log_regex = re.compile(r'^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Processed \d+ valid records\.$')
    valid_logs = [line.strip() for line in logs if log_regex.match(line.strip())]

    assert len(valid_logs) >= 2, f"Expected at least 2 valid log lines, found {len(valid_logs)}."