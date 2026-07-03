# test_final_state.py

import os
import json
import hashlib
from collections import Counter
import pytest

RAW_LOGS_PATH = "/home/user/raw_logs.jsonl"
CLEAN_LOGS_PATH = "/home/user/clean_logs.jsonl"
TEMPLATE_PATH = "/home/user/report_template.html"
SUMMARY_PATH = "/home/user/summary.html"

def get_expected_data():
    if not os.path.exists(RAW_LOGS_PATH):
        pytest.fail(f"Input file {RAW_LOGS_PATH} is missing.")

    with open(RAW_LOGS_PATH, 'r') as f:
        lines = f.read().strip().splitlines()

    total_raw = len(lines)

    seen_hashes = set()
    unique_logs = []
    actions = []

    for line in lines:
        if not line.strip():
            continue
        entry = json.loads(line)

        # Deduplication key
        action = entry.get("action", "")
        status = entry.get("status", "")
        email = entry.get("email", "")

        key_str = f"{action}-{status}-{email}"
        key_hash = hashlib.sha256(key_str.encode('utf-8')).hexdigest()

        if key_hash not in seen_hashes:
            seen_hashes.add(key_hash)

            # Masking
            ip = entry.get("ip", "")
            if ip.count('.') == 3:
                last_octet = ip.split('.')[-1]
                entry["ip"] = f"XXX.XXX.XXX.{last_octet}"

            if "@" in email:
                domain = email.split('@')[1]
                entry["email"] = f"***@{domain}"

            unique_logs.append(entry)
            actions.append(action)

    total_unique = len(unique_logs)

    # Top action
    if actions:
        action_counts = Counter(actions)
        top_action = action_counts.most_common(1)[0][0]
    else:
        top_action = ""

    return total_raw, total_unique, top_action, unique_logs

def test_clean_logs():
    assert os.path.isfile(CLEAN_LOGS_PATH), f"Output file {CLEAN_LOGS_PATH} was not created."

    _, _, _, expected_unique_logs = get_expected_data()

    with open(CLEAN_LOGS_PATH, 'r') as f:
        actual_lines = f.read().strip().splitlines()

    assert len(actual_lines) == len(expected_unique_logs), f"Expected {len(expected_unique_logs)} unique logs, but found {len(actual_lines)} in {CLEAN_LOGS_PATH}."

    for i, (actual_line, expected_entry) in enumerate(zip(actual_lines, expected_unique_logs)):
        try:
            actual_entry = json.loads(actual_line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {CLEAN_LOGS_PATH} is not valid JSON.")

        assert actual_entry == expected_entry, f"Log entry at line {i+1} does not match expected masked/deduplicated entry.\nExpected: {expected_entry}\nActual: {actual_entry}"

def test_summary_html():
    assert os.path.isfile(SUMMARY_PATH), f"Output file {SUMMARY_PATH} was not created."
    assert os.path.isfile(TEMPLATE_PATH), f"Template file {TEMPLATE_PATH} is missing."

    total_raw, total_unique, top_action, _ = get_expected_data()

    with open(TEMPLATE_PATH, 'r') as f:
        template_content = f.read()

    expected_summary = template_content.replace("{{TOTAL_RAW}}", str(total_raw))
    expected_summary = expected_summary.replace("{{TOTAL_UNIQUE}}", str(total_unique))
    expected_summary = expected_summary.replace("{{TOP_ACTION}}", top_action)

    with open(SUMMARY_PATH, 'r') as f:
        actual_summary = f.read()

    assert actual_summary.strip() == expected_summary.strip(), f"Content of {SUMMARY_PATH} does not match expected output with replaced placeholders."