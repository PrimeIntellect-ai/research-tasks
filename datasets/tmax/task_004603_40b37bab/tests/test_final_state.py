# test_final_state.py

import os
import csv
import subprocess
from collections import defaultdict

def compute_expected_output(raw_file):
    with open(raw_file, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # 1. Deduplication
    dedup = {}
    for row in data:
        key = (row['JobId'], row['StringId'])
        ts = int(row['Timestamp'])
        if key not in dedup or ts > int(dedup[key]['Timestamp']):
            dedup[key] = row

    # 2. Calculate WPM and group by TranslatorId
    translators = defaultdict(list)
    for row in dedup.values():
        wpm = int(row['WordCount']) / (int(row['DurationSeconds']) / 60.0)
        translators[row['TranslatorId']].append({
            'Timestamp': int(row['Timestamp']),
            'JobId': row['JobId'],
            'StringId': row['StringId'],
            'WPM': wpm
        })

    # 3. Sort and calculate rolling avg
    output = []
    for tid in sorted(translators.keys()):
        records = sorted(translators[tid], key=lambda x: x['Timestamp'])
        for i, rec in enumerate(records):
            start = max(0, i - 2)
            window = records[start:i+1]
            avg_wpm = sum(x['WPM'] for x in window) / len(window)
            output.append({
                'TranslatorId': tid,
                'Timestamp': str(rec['Timestamp']),
                'JobId': rec['JobId'],
                'StringId': rec['StringId'],
                'WPM': f"{rec['WPM']:.2f}",
                'RollingAvgWPM': f"{avg_wpm:.2f}"
            })

    return output

def test_pipeline_execution_and_output():
    script_path = "/home/user/pipeline/run_dag.sh"
    raw_file = "/home/user/data/raw_translations.csv"
    output_file = "/home/user/data/rolling_stats.csv"
    cpp_file = "/home/user/pipeline/transform.cpp"

    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."
    assert os.path.isfile(script_path), f"Shell script {script_path} is missing."
    assert os.access(script_path, os.X_OK) or os.path.isfile(script_path), f"Shell script {script_path} should be executable or able to be run by bash."
    assert os.path.isfile(raw_file), f"Raw data file {raw_file} is missing."

    # Remove the output file if it exists to ensure the script actually creates it
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run the pipeline script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_dag.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert os.path.isfile(output_file), f"Output file {output_file} was not created by the pipeline."

    # Compute expected results dynamically
    expected_records = compute_expected_output(raw_file)

    # Read the actual output
    with open(output_file, "r") as f:
        reader = csv.DictReader(f)
        actual_records = list(reader)

    expected_header = ["TranslatorId", "Timestamp", "JobId", "StringId", "WPM", "RollingAvgWPM"]
    assert reader.fieldnames == expected_header, f"Output CSV header is incorrect. Expected {expected_header}, got {reader.fieldnames}"

    assert len(actual_records) == len(expected_records), f"Expected {len(expected_records)} rows in output, but got {len(actual_records)}."

    for i, (actual, expected) in enumerate(zip(actual_records, expected_records)):
        assert actual['TranslatorId'] == expected['TranslatorId'], f"Row {i+1}: Expected TranslatorId {expected['TranslatorId']}, got {actual['TranslatorId']}"
        assert actual['Timestamp'] == expected['Timestamp'], f"Row {i+1}: Expected Timestamp {expected['Timestamp']}, got {actual['Timestamp']}"
        assert actual['JobId'] == expected['JobId'], f"Row {i+1}: Expected JobId {expected['JobId']}, got {actual['JobId']}"
        assert actual['StringId'] == expected['StringId'], f"Row {i+1}: Expected StringId {expected['StringId']}, got {actual['StringId']}"

        # Allow small floating point variations if they formatted differently, but exact string match is preferred
        assert actual['WPM'] == expected['WPM'], f"Row {i+1}: Expected WPM {expected['WPM']}, got {actual['WPM']}"
        assert actual['RollingAvgWPM'] == expected['RollingAvgWPM'], f"Row {i+1}: Expected RollingAvgWPM {expected['RollingAvgWPM']}, got {actual['RollingAvgWPM']}"