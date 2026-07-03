# test_final_state.py

import os
import json
import csv
import pytest

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def compute_expected_stats(raw_logs_path, sensors_path):
    with open(sensors_path, 'r', encoding='utf-8') as f:
        sensors_data = json.load(f)

    sensor_to_region = {item['sensor_id']: item['region'] for item in sensors_data}

    sensor_messages = {}
    with open(raw_logs_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensor_id = row['sensor_id']
            message = row['message']
            if sensor_id not in sensor_messages:
                sensor_messages[sensor_id] = set()
            sensor_messages[sensor_id].add(message)

    region_messages = {}
    for sensor_id, messages in sensor_messages.items():
        region = sensor_to_region.get(sensor_id)
        if region:
            if region not in region_messages:
                region_messages[region] = set()
            region_messages[region].update(messages)

    stats = []
    for region in sorted(region_messages.keys()):
        msgs = list(region_messages[region])
        unique_count = len(msgs)
        if unique_count < 2:
            min_dist = -1
        else:
            min_dist = float('inf')
            for i in range(len(msgs)):
                for j in range(i + 1, len(msgs)):
                    dist = levenshtein(msgs[i], msgs[j])
                    if dist < min_dist:
                        min_dist = dist
        stats.append({
            'region': region,
            'unique_message_count': str(unique_count),
            'min_levenshtein_distance': str(min_dist)
        })
    return stats

def test_region_stats_csv():
    output_file = "/home/user/region_stats.csv"
    raw_logs_file = "/home/user/raw_logs.csv"
    sensors_file = "/home/user/sensors.json"

    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    expected_stats = compute_expected_stats(raw_logs_file, sensors_file)

    with open(output_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        actual_stats = list(reader)

    assert reader.fieldnames == ['region', 'unique_message_count', 'min_levenshtein_distance'], \
        f"CSV headers do not match expected. Got: {reader.fieldnames}"

    assert len(actual_stats) == len(expected_stats), \
        f"Expected {len(expected_stats)} rows, got {len(actual_stats)}"

    for i, (actual, expected) in enumerate(zip(actual_stats, expected_stats)):
        assert actual['region'] == expected['region'], \
            f"Row {i+1}: expected region {expected['region']}, got {actual['region']}"
        assert actual['unique_message_count'] == expected['unique_message_count'], \
            f"Row {i+1} ({expected['region']}): expected unique_message_count {expected['unique_message_count']}, got {actual['unique_message_count']}"
        assert actual['min_levenshtein_distance'] == expected['min_levenshtein_distance'], \
            f"Row {i+1} ({expected['region']}): expected min_levenshtein_distance {expected['min_levenshtein_distance']}, got {actual['min_levenshtein_distance']}"