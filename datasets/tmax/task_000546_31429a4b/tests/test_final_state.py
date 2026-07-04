# test_final_state.py

import os
import json
import csv
import math
import re
from datetime import datetime

def test_final_state():
    csv_file = '/home/user/translation_telemetry.csv'
    invalid_count_file = '/home/user/invalid_count.txt'
    distances_file = '/home/user/distances.json'

    assert os.path.exists(invalid_count_file), f"File {invalid_count_file} does not exist."
    assert os.path.exists(distances_file), f"File {distances_file} does not exist."

    # Compute expected results
    lang_regex = re.compile(r'^[a-z]{2}-[A-Z]{2}$')
    expected_invalid_count = 0

    # Structure for aggregation: language -> hour -> list of latencies
    lang_hour_latencies = {}

    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                latency = float(row['latency_ms'])
                words = int(row['words_translated'])
            except ValueError:
                expected_invalid_count += 1
                continue

            lang = row['language_code']

            is_valid = True
            if latency <= 0:
                is_valid = False
            if words <= 0:
                is_valid = False
            if not lang_regex.match(lang):
                is_valid = False

            if not is_valid:
                expected_invalid_count += 1
            else:
                # Parse hour
                # e.g. 2023-10-01T00:00:00Z
                ts_str = row['timestamp']
                try:
                    dt = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
                    hour = dt.hour
                except ValueError:
                    continue

                if lang not in lang_hour_latencies:
                    lang_hour_latencies[lang] = {h: [] for h in range(24)}
                lang_hour_latencies[lang][hour].append(latency)

    # Compute averages
    lang_vectors = {}
    for lang, hours_data in lang_hour_latencies.items():
        vector = []
        for h in range(24):
            lats = hours_data[h]
            if lats:
                vector.append(sum(lats) / len(lats))
            else:
                vector.append(0.0)
        lang_vectors[lang] = vector

    # Compute distances
    expected_distances = {}
    if 'es-ES' in lang_vectors:
        base_vector = lang_vectors['es-ES']
        for lang, vector in lang_vectors.items():
            if lang == 'es-ES':
                continue
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(base_vector, vector)))
            expected_distances[lang] = round(dist, 4)

    # Verify invalid count
    with open(invalid_count_file, 'r', encoding='utf-8') as f:
        actual_invalid_count_str = f.read().strip()

    assert actual_invalid_count_str.isdigit(), f"{invalid_count_file} does not contain a valid integer."
    assert int(actual_invalid_count_str) == expected_invalid_count, f"Expected invalid count {expected_invalid_count}, got {actual_invalid_count_str}"

    # Verify distances
    with open(distances_file, 'r', encoding='utf-8') as f:
        try:
            actual_distances = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{distances_file} is not a valid JSON file."

    assert 'es-ES' not in actual_distances, "'es-ES' should not be in the output JSON."

    for lang, expected_dist in expected_distances.items():
        assert lang in actual_distances, f"Language {lang} is missing from distances.json."
        actual_dist = actual_distances[lang]
        assert isinstance(actual_dist, (int, float)), f"Distance for {lang} should be a number."
        assert math.isclose(actual_dist, expected_dist, rel_tol=1e-4, abs_tol=1e-4), \
            f"Expected distance for {lang} to be {expected_dist}, got {actual_dist}."

    # Check for unexpected languages
    for lang in actual_distances:
        assert lang in expected_distances, f"Unexpected language {lang} found in distances.json."