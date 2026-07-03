# test_final_state.py
import os
import csv
import json
import math
import statistics
from datetime import datetime, timedelta

def parse_time(ts_str):
    return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")

def format_time(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_expected_data():
    input_file = '/home/user/input/sensor_data.csv'
    if not os.path.exists(input_file):
        return [], []

    raw_data = []
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_data.append({
                'timestamp': parse_time(row['timestamp']),
                'sensor_id': row['sensor_id'],
                'temperature': float(row['temperature'])
            })

    # Group by sensor_id
    sensors = {}
    for row in raw_data:
        sensors.setdefault(row['sensor_id'], []).append(row)

    all_anomalies = []
    all_hourly = []

    for sensor_id, rows in sensors.items():
        # 2. Resampling to 1-minute frequency
        min_time = min(r['timestamp'] for r in rows).replace(second=0, microsecond=0)
        max_time = max(r['timestamp'] for r in rows).replace(second=0, microsecond=0)

        # Aggregate per minute
        minute_data = {}
        for r in rows:
            minute = r['timestamp'].replace(second=0, microsecond=0)
            minute_data.setdefault(minute, []).append(r['temperature'])

        resampled = []
        curr = min_time
        while curr <= max_time:
            if curr in minute_data:
                avg_temp = sum(minute_data[curr]) / len(minute_data[curr])
                resampled.append({'timestamp': curr, 'temperature': avg_temp})
            else:
                resampled.append({'timestamp': curr, 'temperature': None})
            curr += timedelta(minutes=1)

        # 3. Interpolation up to 5 mins
        for i in range(len(resampled)):
            if resampled[i]['temperature'] is None:
                # Find previous valid
                prev_idx = i - 1
                while prev_idx >= 0 and resampled[prev_idx]['temperature'] is None:
                    prev_idx -= 1
                # Find next valid
                next_idx = i + 1
                while next_idx < len(resampled) and resampled[next_idx]['temperature'] is None:
                    next_idx += 1

                if prev_idx >= 0 and next_idx < len(resampled):
                    gap_size = next_idx - prev_idx - 1
                    if gap_size <= 5:
                        prev_val = resampled[prev_idx]['temperature']
                        next_val = resampled[next_idx]['temperature']
                        step = (next_val - prev_val) / (gap_size + 1)
                        resampled[i]['temperature'] = prev_val + step * (i - prev_idx)

        # 4. Anomaly Detection
        anomalies = []
        for i in range(len(resampled)):
            window = resampled[max(0, i-9):i+1]
            valid_temps = [w['temperature'] for w in window if w['temperature'] is not None]

            if len(valid_temps) >= 3 and resampled[i]['temperature'] is not None:
                mean = sum(valid_temps) / len(valid_temps)
                std = statistics.stdev(valid_temps) if len(valid_temps) > 1 else 0

                if std > 0 and abs(resampled[i]['temperature'] - mean) > 3 * std:
                    anomalies.append({
                        'timestamp': format_time(resampled[i]['timestamp']),
                        'sensor_id': sensor_id,
                        'temperature': resampled[i]['temperature']
                    })
                    # 5. Imputation: mark as anomaly for later ffill
                    resampled[i]['is_anomaly'] = True

        all_anomalies.extend(anomalies)

        # 5. Imputation (ffill)
        last_valid = None
        for i in range(len(resampled)):
            if resampled[i].get('is_anomaly'):
                resampled[i]['temperature'] = last_valid
            elif resampled[i]['temperature'] is not None:
                last_valid = resampled[i]['temperature']
            elif resampled[i]['temperature'] is None and last_valid is not None:
                resampled[i]['temperature'] = last_valid

        # 6. Hourly Aggregation
        hourly_data = {}
        for r in resampled:
            if r['temperature'] is not None:
                hour = r['timestamp'].replace(minute=0, second=0, microsecond=0)
                hourly_data.setdefault(hour, []).append(r['temperature'])

        for hour, temps in hourly_data.items():
            all_hourly.append({
                'timestamp': format_time(hour),
                'sensor_id': sensor_id,
                'mean_temp': sum(temps) / len(temps),
                'min_temp': min(temps),
                'max_temp': max(temps)
            })

    # Sort anomalies
    all_anomalies.sort(key=lambda x: (x['timestamp'], x['sensor_id']))

    # Sort hourly
    all_hourly.sort(key=lambda x: (x['timestamp'], x['sensor_id']))

    return all_anomalies, all_hourly

def test_anomalies_json():
    expected_anomalies, _ = get_expected_data()
    output_file = '/home/user/output/anomalies.json'

    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        try:
            actual_anomalies = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{output_file} is not a valid JSON file."

    assert isinstance(actual_anomalies, list), f"{output_file} should contain a JSON list."
    assert len(actual_anomalies) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies, but found {len(actual_anomalies)}."

    for actual, expected in zip(actual_anomalies, expected_anomalies):
        assert actual['timestamp'] == expected['timestamp'], f"Timestamp mismatch: expected {expected['timestamp']}, got {actual['timestamp']}"
        assert actual['sensor_id'] == expected['sensor_id'], f"Sensor ID mismatch: expected {expected['sensor_id']}, got {actual['sensor_id']}"
        assert math.isclose(actual['temperature'], expected['temperature'], rel_tol=1e-5), f"Temperature mismatch for {expected['timestamp']}: expected {expected['temperature']}, got {actual['temperature']}"

def test_hourly_stats_csv():
    _, expected_hourly = get_expected_data()
    output_file = '/home/user/output/hourly_stats.csv'

    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    actual_hourly = []
    with open(output_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            actual_hourly.append(row)

    assert len(actual_hourly) == len(expected_hourly), f"Expected {len(expected_hourly)} hourly records, but found {len(actual_hourly)}."

    for actual, expected in zip(actual_hourly, expected_hourly):
        assert actual['timestamp'] == expected['timestamp'], f"Timestamp mismatch: expected {expected['timestamp']}, got {actual['timestamp']}"
        assert actual['sensor_id'] == expected['sensor_id'], f"Sensor ID mismatch: expected {expected['sensor_id']}, got {actual['sensor_id']}"

        # Check floats to 2 decimal places
        expected_mean = f"{expected['mean_temp']:.2f}"
        expected_min = f"{expected['min_temp']:.2f}"
        expected_max = f"{expected['max_temp']:.2f}"

        assert actual['mean_temp'] == expected_mean, f"mean_temp mismatch: expected {expected_mean}, got {actual['mean_temp']}"
        assert actual['min_temp'] == expected_min, f"min_temp mismatch: expected {expected_min}, got {actual['min_temp']}"
        assert actual['max_temp'] == expected_max, f"max_temp mismatch: expected {expected_max}, got {actual['max_temp']}"