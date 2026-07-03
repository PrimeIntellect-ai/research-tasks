# test_final_state.py

import os
import re
import json
from collections import defaultdict
import pytest

def compute_expected():
    original_file = '/home/user/chat_logs.txt'
    if not os.path.exists(original_file):
        return [], {}

    with open(original_file, 'r') as f:
        lines = f.readlines()

    anonymized_lines = []
    stats = defaultdict(lambda: {"total_messages": 0, "total_words": 0, "total_pii_masked": 0})

    email_pattern = re.compile(r'\S+@\S+\.\S+')
    phone_pattern = re.compile(r'\d{3}-\d{3}-\d{4}')

    for line in lines:
        if not line.strip():
            continue

        match = re.match(r'^(\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]) ([^:]+): (.*)$', line)
        if not match:
            anonymized_lines.append(line)
            continue

        timestamp, user_id, message = match.groups()

        # Word count calculation using default .split()
        word_count = len(message.split())

        # PII count
        emails = email_pattern.findall(message)
        phones = phone_pattern.findall(message)
        pii_count = len(emails) + len(phones)

        # Masking
        masked_message = email_pattern.sub('[EMAIL]', message)
        masked_message = phone_pattern.sub('[PHONE]', masked_message)

        anonymized_lines.append(f"{timestamp} {user_id}: {masked_message}\n")

        stats[user_id]["total_messages"] += 1
        stats[user_id]["total_words"] += word_count
        stats[user_id]["total_pii_masked"] += pii_count

    final_stats = {}
    for uid, s in stats.items():
        avg_words = round(s["total_words"] / s["total_messages"], 2)
        final_stats[uid] = {
            "total_messages": s["total_messages"],
            "average_word_count": avg_words,
            "total_pii_masked": s["total_pii_masked"]
        }

    return anonymized_lines, final_stats

def test_anonymized_logs_created_and_correct():
    expected_lines, _ = compute_expected()
    output_file = '/home/user/anonymized_logs.txt'

    assert os.path.exists(output_file), f"Expected output file {output_file} was not created."

    with open(output_file, 'r') as f:
        actual_lines = f.readlines()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in anonymized logs, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual.strip() == expected.strip(), f"Mismatch on line {i+1} of anonymized logs.\nExpected: {expected.strip()}\nActual: {actual.strip()}"

def test_user_stats_json_created_and_correct():
    _, expected_stats = compute_expected()
    output_file = '/home/user/user_stats.json'

    assert os.path.exists(output_file), f"Expected output file {output_file} was not created."

    with open(output_file, 'r') as f:
        try:
            actual_stats = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_file} is not valid JSON.")

    assert isinstance(actual_stats, dict), f"Expected JSON root to be a dictionary, got {type(actual_stats).__name__}."

    assert set(actual_stats.keys()) == set(expected_stats.keys()), f"User IDs in JSON do not match expected. Expected {list(expected_stats.keys())}, got {list(actual_stats.keys())}."

    for uid, expected_data in expected_stats.items():
        actual_data = actual_stats[uid]
        assert actual_data.get("total_messages") == expected_data["total_messages"], f"Mismatch in total_messages for user {uid}."
        assert actual_data.get("average_word_count") == expected_data["average_word_count"], f"Mismatch in average_word_count for user {uid}. Expected {expected_data['average_word_count']}, got {actual_data.get('average_word_count')}."
        assert actual_data.get("total_pii_masked") == expected_data["total_pii_masked"], f"Mismatch in total_pii_masked for user {uid}. Expected {expected_data['total_pii_masked']}, got {actual_data.get('total_pii_masked')}."