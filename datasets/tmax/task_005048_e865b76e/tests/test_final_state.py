# test_final_state.py

import os
import json
import subprocess
import pytest

EVIL_DIR = "/app/data/evil"
CLEAN_DIR = "/app/data/clean"
PROCESSED_DIR = "/home/user/processed"

def get_redis_results():
    """Fetch the contents of the pipeline:results list from Redis."""
    try:
        out = subprocess.check_output(
            ['redis-cli', 'LRANGE', 'pipeline:results', '0', '-1'], 
            text=True
        )
        results = []
        for line in out.strip().split('\n'):
            if line.strip():
                try:
                    results.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    pass
        return results
    except Exception as e:
        return []

def test_adversarial_corpus_results():
    evil_files = set(os.listdir(EVIL_DIR)) if os.path.exists(EVIL_DIR) else set()
    clean_files = set(os.listdir(CLEAN_DIR)) if os.path.exists(CLEAN_DIR) else set()

    processed_files = set(os.listdir(PROCESSED_DIR)) if os.path.exists(PROCESSED_DIR) else set()

    redis_results = get_redis_results()
    redis_status_map = {}
    for item in redis_results:
        if 'filename' in item and 'status' in item:
            redis_status_map[item['filename']] = item['status']

    # Check evil corpus
    evil_bypassed = []
    for ef in evil_files:
        if ef in processed_files:
            evil_bypassed.append(ef)
        elif redis_status_map.get(ef) != "REJECTED":
            evil_bypassed.append(f"{ef} (not marked REJECTED in Redis)")

    # Check clean corpus
    clean_modified_or_rejected = []
    for cf in clean_files:
        if cf not in processed_files:
            clean_modified_or_rejected.append(f"{cf} (missing from processed)")
        elif redis_status_map.get(cf) != "ACCEPTED":
            clean_modified_or_rejected.append(f"{cf} (not marked ACCEPTED in Redis)")

    # Summary of failures
    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified_or_rejected:
        errors.append(f"{len(clean_modified_or_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified_or_rejected)}")

    assert not errors, " | ".join(errors)

def test_clean_files_utf8():
    clean_files = os.listdir(CLEAN_DIR) if os.path.exists(CLEAN_DIR) else []
    for cf in clean_files:
        processed_path = os.path.join(PROCESSED_DIR, cf)
        if os.path.exists(processed_path):
            try:
                with open(processed_path, 'r', encoding='utf-8') as f:
                    f.read()
            except UnicodeDecodeError:
                pytest.fail(f"Clean file {cf} was not saved as valid UTF-8 in {PROCESSED_DIR}")

def test_webhook_log_contains_clean_data():
    webhook_log_path = "/app/webhook.log"
    assert os.path.exists(webhook_log_path), f"Webhook log not found at {webhook_log_path}"

    with open(webhook_log_path, 'r', encoding='utf-8', errors='replace') as f:
        log_content = f.read()

    assert len(log_content) > 0, "Webhook log is empty, meaning no data was forwarded to the webhook endpoint."