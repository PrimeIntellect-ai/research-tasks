# test_final_state.py

import os
import json
import csv
import unicodedata
import pytest

def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in text if c.isalnum() and c.isascii())

def get_bigrams(text):
    if len(text) < 2:
        return set()
    return set(text[i:i+2] for i in range(len(text)-1))

def jaccard_similarity(set1, set2):
    if not set1 and not set2:
        return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0.0

def compute_expected_flags(input_file):
    messages = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            msg = json.loads(line)
            messages.append(msg)

    window = []
    flagged = []

    for msg in messages:
        current_time = msg['timestamp']
        norm_text = normalize_text(msg['text'])
        bigrams = get_bigrams(norm_text)

        # Update window
        window = [m for m in window if current_time - 60 < m['timestamp'] < current_time]

        best_match = None
        best_score = -1.0

        for w_msg in window:
            score = jaccard_similarity(bigrams, w_msg['bigrams'])
            if score >= 0.75:
                if score > best_score:
                    best_score = score
                    best_match = w_msg
                elif score == best_score:
                    if best_match is None or w_msg['timestamp'] < best_match['timestamp']:
                        best_match = w_msg

        if best_match:
            flagged.append({
                'id': msg['id'],
                'matched_id': best_match['id'],
                'similarity_score': f"{best_score:.3f}"
            })

        window.append({
            'id': msg['id'],
            'timestamp': current_time,
            'bigrams': bigrams
        })

    return flagged

def test_flagged_messages_csv():
    input_file = "/home/user/chat_stream.jsonl"
    output_file = "/home/user/flagged_messages.csv"

    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"Path {output_file} is not a file."

    expected_flags = compute_expected_flags(input_file)

    actual_flags = []
    with open(output_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['id', 'matched_id', 'similarity_score'], \
            f"CSV headers are incorrect. Expected ['id', 'matched_id', 'similarity_score'], got {reader.fieldnames}"
        for row in reader:
            actual_flags.append(row)

    assert len(actual_flags) == len(expected_flags), \
        f"Expected {len(expected_flags)} flagged messages, but found {len(actual_flags)}."

    for i, (actual, expected) in enumerate(zip(actual_flags, expected_flags)):
        assert actual['id'] == expected['id'], f"Row {i+1}: Expected id {expected['id']}, got {actual['id']}."
        assert actual['matched_id'] == expected['matched_id'], f"Row {i+1} ({actual['id']}): Expected matched_id {expected['matched_id']}, got {actual['matched_id']}."
        assert actual['similarity_score'] == expected['similarity_score'], f"Row {i+1} ({actual['id']}): Expected similarity_score {expected['similarity_score']}, got {actual['similarity_score']}."