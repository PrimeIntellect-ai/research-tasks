# test_final_state.py

import os
import csv
import re
import pytest

def compute_expected():
    raw_path = "/home/user/raw_chat.tsv"
    if not os.path.exists(raw_path):
        return [], []

    processed = []
    sampled = []
    stratum_counts = {'S': 0, 'M': 0, 'L': 0}
    window = []

    with open(raw_path, "r", encoding="latin1") as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar='\\')
        for row in reader:
            if not row or len(row) < 3:
                continue
            msg_id, encoding, raw_message = row[0], row[1], row[2]

            # The file was written with latin1 mapping to preserve bytes.
            raw_bytes = raw_message.encode('latin1')

            if encoding == "LATIN1":
                utf8_str = raw_bytes.decode('latin1')
            else:
                utf8_str = raw_bytes.decode('utf-8')

            # Tokenize by space, period, comma, exclamation, question mark
            tokens = re.split(r'[ \.,!\?]', utf8_str)

            valid_tokens = []
            for t in tokens:
                if t:
                    # Normalizing uppercase to lowercase ASCII does not change byte length
                    valid_tokens.append(len(t.encode('utf-8')))

            for length in valid_tokens:
                window.append(length)
                if len(window) > 100:
                    window.pop(0)

            token_count = len(valid_tokens)

            if token_count <= 5:
                stratum = 'S'
            elif token_count <= 15:
                stratum = 'M'
            else:
                stratum = 'L'

            if len(window) == 0:
                avg = 0.0
            else:
                avg = sum(window) / float(len(window))

            avg_str = f"{avg:.2f}"

            processed_row = [msg_id, str(token_count), avg_str, stratum]
            processed.append(processed_row)

            if stratum_counts[stratum] < 2:
                sampled.append(processed_row)
                stratum_counts[stratum] += 1

    return processed, sampled

def read_tsv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if row:
                rows.append(row)
    return rows

def test_processed_chat_output():
    processed_path = "/home/user/processed_chat.tsv"
    assert os.path.exists(processed_path), f"Expected output file {processed_path} is missing."

    expected_processed, _ = compute_expected()
    actual_processed = read_tsv(processed_path)

    assert len(actual_processed) == len(expected_processed), \
        f"Row count mismatch in {processed_path}. Expected {len(expected_processed)}, got {len(actual_processed)}."

    for i, (actual, expected) in enumerate(zip(actual_processed, expected_processed)):
        assert actual == expected, \
            f"Row {i+1} mismatch in {processed_path}.\nExpected: {expected}\nGot: {actual}"

def test_sampled_chat_output():
    sampled_path = "/home/user/sampled_chat.tsv"
    assert os.path.exists(sampled_path), f"Expected output file {sampled_path} is missing."

    _, expected_sampled = compute_expected()
    actual_sampled = read_tsv(sampled_path)

    assert len(actual_sampled) == len(expected_sampled), \
        f"Row count mismatch in {sampled_path}. Expected {len(expected_sampled)}, got {len(actual_sampled)}."

    for i, (actual, expected) in enumerate(zip(actual_sampled, expected_sampled)):
        assert actual == expected, \
            f"Row {i+1} mismatch in {sampled_path}.\nExpected: {expected}\nGot: {actual}"