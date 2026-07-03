# test_final_state.py
import os
import re
import hashlib
import csv
import pytest

def get_expected_data():
    log_dir = "/home/user/raw_logs"
    pattern = re.compile(r'\[(.*?)\] INFO Extracted translation -> Key: (.*?) \| Lang: (.*?) \| Value: (.*)')

    entries = {}
    counts = {}

    if not os.path.exists(log_dir):
        return [], []

    for filename in os.listdir(log_dir):
        if not filename.endswith('.log'):
            continue
        filepath = os.path.join(log_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    ts, key, lang, value = match.groups()
                    key_lang = f"{key}_{lang}"

                    if key_lang not in entries:
                        entries[key_lang] = (ts, value)
                        counts[key_lang] = 1
                    else:
                        counts[key_lang] += 1
                        if ts > entries[key_lang][0]:
                            entries[key_lang] = (ts, value)

    final_csv = [["Key", "Lang", "Value"]]
    for key_lang in sorted(entries.keys()):
        key, lang = key_lang.split('_', 1)
        final_csv.append([key, lang, entries[key_lang][1]])

    duplicates = []
    for key_lang, count in counts.items():
        if count > 1:
            md5 = hashlib.md5(key_lang.encode('utf-8')).hexdigest()
            duplicates.append(md5)

    return final_csv, sorted(duplicates)

def test_script_exists():
    script_path = "/home/user/process_locales.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_final_csv_output():
    csv_path = "/home/user/locales/final.csv"
    assert os.path.isfile(csv_path), f"The output file {csv_path} does not exist."

    expected_csv, _ = get_expected_data()

    actual_csv = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_csv.append(row)

    assert actual_csv == expected_csv, "The contents of final.csv do not match the expected deduplicated and sorted output."

def test_duplicate_report_output():
    report_path = "/home/user/locales/duplicate_report.txt"
    assert os.path.isfile(report_path), f"The output file {report_path} does not exist."

    _, expected_duplicates = get_expected_data()

    with open(report_path, 'r', encoding='utf-8') as f:
        actual_duplicates = [line.strip() for line in f if line.strip()]

    assert actual_duplicates == expected_duplicates, "The contents of duplicate_report.txt do not match the expected MD5 hashes."