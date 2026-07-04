# test_final_state.py

import os
import json
import csv
import re

def compute_expected_data(csv_path):
    # Regex for email: preceded and followed by at least one alphanumeric character
    # non-whitespace containing @ 
    # Actually, a simpler regex matching the spec:
    # "any sequence of non-whitespace characters containing an @ symbol, preceded and followed by at least one alphanumeric character"
    email_pattern = re.compile(r'[a-zA-Z0-9][^\s]*@[^\s]*[a-zA-Z0-9]')

    def mask_email(text):
        return email_pattern.sub('[EMAIL]', text)

    def get_words(text):
        return set(re.findall(r'[a-zA-Z0-9]+', text.lower()))

    expected = []
    user_prev_words = {}

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            masked_msg = mask_email(row['message'])
            words = get_words(masked_msg)

            user_id = row['user_id']
            is_anomaly = False

            if user_id in user_prev_words:
                prev_words = user_prev_words[user_id]
                if not prev_words and not words:
                    jaccard = 1.0
                elif not prev_words or not words:
                    jaccard = 0.0
                else:
                    intersection = len(words.intersection(prev_words))
                    union = len(words.union(prev_words))
                    jaccard = intersection / union if union > 0 else 0.0

                if jaccard >= 0.8:
                    is_anomaly = True

            user_prev_words[user_id] = words

            expected.append({
                'timestamp': row['timestamp'],
                'user_id': user_id,
                'cleaned_message': masked_msg,
                'is_anomaly': is_anomaly
            })

    return expected

def test_processed_logs_exist():
    output_path = "/home/user/processed_logs.jsonl"
    assert os.path.exists(output_path), f"Expected output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_processed_logs_format_and_content():
    input_path = "/home/user/raw_chat_logs.csv"
    output_path = "/home/user/processed_logs.jsonl"

    assert os.path.exists(input_path), "Input CSV file is missing, cannot verify."

    expected_data = compute_expected_data(input_path)

    actual_data = []
    with open(output_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_data.append(record)
            except json.JSONDecodeError:
                assert False, f"Line {line_num} in {output_path} is not valid JSON."

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        # Check keys
        expected_keys = {'timestamp', 'user_id', 'cleaned_message', 'is_anomaly'}
        assert set(actual.keys()) == expected_keys, f"Row {i+1} keys mismatch. Expected {expected_keys}, got {set(actual.keys())}."

        assert actual['timestamp'] == expected['timestamp'], f"Row {i+1} timestamp mismatch."
        assert actual['user_id'] == expected['user_id'], f"Row {i+1} user_id mismatch."
        assert actual['cleaned_message'] == expected['cleaned_message'], f"Row {i+1} cleaned_message mismatch. Expected {repr(expected['cleaned_message'])}, got {repr(actual['cleaned_message'])}."
        assert actual['is_anomaly'] == expected['is_anomaly'], f"Row {i+1} is_anomaly mismatch. Expected {expected['is_anomaly']}, got {actual['is_anomaly']}."