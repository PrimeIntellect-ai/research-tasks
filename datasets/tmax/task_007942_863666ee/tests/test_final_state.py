# test_final_state.py
import os
import csv
import json

def test_valid_translations_jsonl():
    """Test that valid_translations.jsonl contains the correct JSON objects."""
    filepath = "/home/user/valid_translations.jsonl"
    assert os.path.exists(filepath), f"File {filepath} is missing."

    expected = [
        {"id": "str_001", "locale": "en-US", "word_count": 2},
        {"id": "str_002", "locale": "fr-FR", "word_count": 3},
        {"id": "str_006", "locale": "it-IT", "word_count": 4}
    ]

    actual = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    actual.append(json.loads(line))
                except json.JSONDecodeError as e:
                    assert False, f"Invalid JSON in {filepath}: {line} ({e})"

    expected_sorted = sorted(expected, key=lambda x: x.get("id", ""))
    actual_sorted = sorted(actual, key=lambda x: x.get("id", ""))

    assert actual_sorted == expected_sorted, f"Content of {filepath} does not match expected output. Expected: {expected_sorted}, Actual: {actual_sorted}"

def test_anomalies_csv():
    """Test that anomalies.csv contains the correct rows and preserves formatting."""
    filepath = "/home/user/anomalies.csv"
    assert os.path.exists(filepath), f"File {filepath} is missing."

    expected_rows = [
        ['string_id', 'locale', 'translation', 'status'],
        ['str_004', 'pt-BR', '', 'approved'],
        ['str_005', 'de-DE', 'Ein sehr langes Wort das eigentlich ein Satz ist und mehr als zwanzig Worte enthält um die Anomalieerkennung zu triggern eins zwei drei vier fünf sechs sieben acht neun zehn elf zwölf dreizehn vierzehn fünfzehn sechzehn siebzehn achtzehn neunzehn zwanzig einundzwanzig', 'approved']
    ]

    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) > 0, f"{filepath} is empty."
    assert actual_rows[0] == expected_rows[0], f"CSV header in {filepath} is missing or incorrect. Expected: {expected_rows[0]}, Actual: {actual_rows[0]}"

    expected_data = sorted(expected_rows[1:], key=lambda x: x[0])
    actual_data = sorted(actual_rows[1:], key=lambda x: x[0])

    assert actual_data == expected_data, f"Data rows in {filepath} do not match expected anomalies. Expected: {expected_data}, Actual: {actual_data}"