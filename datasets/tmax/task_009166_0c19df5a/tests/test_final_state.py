# test_final_state.py
import os
import csv
import json
import math
from datetime import datetime, timedelta
import pytest

def parse_timestamp(ts_str):
    if not ts_str:
        return None
    return datetime.fromisoformat(ts_str.replace('Z', '+00:00').split('+')[0])

def interpolate_series(data_list):
    # data_list is a list of (timestamp, value)
    # value can be None
    n = len(data_list)
    result = []

    for i in range(n):
        ts, val = data_list[i]
        if val is not None:
            result.append((ts, val))
            continue

        # Find previous valid
        prev_val = None
        prev_ts = None
        for j in range(i - 1, -1, -1):
            if data_list[j][1] is not None:
                prev_ts, prev_val = data_list[j]
                break

        # Find next valid
        next_val = None
        next_ts = None
        for j in range(i + 1, n):
            if data_list[j][1] is not None:
                next_ts, next_val = data_list[j]
                break

        if prev_val is not None and next_val is not None:
            # Time-based linear interpolation
            total_seconds = (next_ts - prev_ts).total_seconds()
            if total_seconds == 0:
                interp_val = prev_val
            else:
                ratio = (ts - prev_ts).total_seconds() / total_seconds
                interp_val = prev_val + (next_val - prev_val) * ratio
        elif prev_val is not None:
            interp_val = prev_val  # ffill
        elif next_val is not None:
            interp_val = next_val  # bfill
        else:
            interp_val = None

        result.append((ts, interp_val))

    return result

def get_bucket_start(ts):
    minute = (ts.minute // 15) * 15
    return ts.replace(minute=minute, second=0, microsecond=0)

def compute_expected_data():
    raw_file = '/home/user/raw_sensor_data.csv'
    if not os.path.exists(raw_file):
        return None, None

    sensors_data = {}
    with open(raw_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = parse_timestamp(row['timestamp'])
            sensor = row['sensor_id']
            temp = float(row['temperature']) if row['temperature'] not in ('', 'NaN', 'nan') else None
            hum = float(row['humidity']) if row['humidity'] not in ('', 'NaN', 'nan') else None

            if sensor not in sensors_data:
                sensors_data[sensor] = {'ts': [], 'temp': [], 'hum': []}

            sensors_data[sensor]['ts'].append(ts)
            sensors_data[sensor]['temp'].append(temp)
            sensors_data[sensor]['hum'].append(hum)

    resampled_data = {}

    for sensor, data in sensors_data.items():
        # Sort by timestamp
        sorted_indices = sorted(range(len(data['ts'])), key=lambda i: data['ts'][i])
        ts_sorted = [data['ts'][i] for i in sorted_indices]
        temp_sorted = [data['temp'][i] for i in sorted_indices]
        hum_sorted = [data['hum'][i] for i in sorted_indices]

        temp_interp = interpolate_series(list(zip(ts_sorted, temp_sorted)))
        hum_interp = interpolate_series(list(zip(ts_sorted, hum_sorted)))

        # Group by 15-min buckets
        buckets = {}
        for i in range(len(ts_sorted)):
            b_start = get_bucket_start(ts_sorted[i])
            if b_start not in buckets:
                buckets[b_start] = {'temp': [], 'hum': []}
            buckets[b_start]['temp'].append(temp_interp[i][1])
            buckets[b_start]['hum'].append(hum_interp[i][1])

        if not buckets:
            continue

        min_ts = min(buckets.keys())
        max_ts = max(buckets.keys())

        # Create continuous 15-min intervals
        curr_ts = min_ts
        bucket_sequence = []
        while curr_ts <= max_ts:
            bucket_sequence.append(curr_ts)
            curr_ts += timedelta(minutes=15)

        # Compute means and ffill
        resampled = []
        last_temp = None
        last_hum = None

        for b_ts in bucket_sequence:
            if b_ts in buckets:
                t_mean = sum(buckets[b_ts]['temp']) / len(buckets[b_ts]['temp'])
                h_mean = sum(buckets[b_ts]['hum']) / len(buckets[b_ts]['hum'])
                last_temp = t_mean
                last_hum = h_mean
            else:
                t_mean = last_temp
                h_mean = last_hum

            resampled.append({
                'timestamp': b_ts,
                'temp': t_mean,
                'hum': h_mean
            })

        # Compute 1h rolling average (4 periods)
        for i in range(len(resampled)):
            start_idx = max(0, i - 3)
            window = resampled[start_idx:i+1]
            t_roll = sum(w['temp'] for w in window) / len(window)
            h_roll = sum(w['hum'] for w in window) / len(window)
            resampled[i]['temp_roll'] = t_roll
            resampled[i]['hum_roll'] = h_roll

        resampled_data[sensor] = resampled

    # Compute daily summary
    daily_summary = {}
    for sensor, resampled in resampled_data.items():
        for row in resampled:
            date_str = row['timestamp'].strftime('%Y-%m-%d')
            if date_str not in daily_summary:
                daily_summary[date_str] = {}
            if sensor not in daily_summary[date_str]:
                daily_summary[date_str][sensor] = {'temp': [], 'hum': []}

            daily_summary[date_str][sensor]['temp'].append(row['temp_roll'])
            daily_summary[date_str][sensor]['hum'].append(row['hum_roll'])

    summary_result = {}
    for date_str, sensors in daily_summary.items():
        summary_result[date_str] = {}
        for sensor, vals in sensors.items():
            summary_result[date_str][sensor] = {
                "temp_rolling_min": round(min(vals['temp']), 2),
                "temp_rolling_max": round(max(vals['temp']), 2),
                "temp_rolling_mean": round(sum(vals['temp']) / len(vals['temp']), 2),
                "hum_rolling_min": round(min(vals['hum']), 2),
                "hum_rolling_max": round(max(vals['hum']), 2),
                "hum_rolling_mean": round(sum(vals['hum']) / len(vals['hum']), 2)
            }

    return resampled_data, summary_result

def test_processed_rolling_csv():
    csv_path = '/home/user/processed_rolling.csv'
    assert os.path.exists(csv_path), f"Missing required file: {csv_path}"

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['timestamp', 'sensor_id', 'temperature_bucketed', 'humidity_bucketed', 'temp_rolling_1h', 'hum_rolling_1h'], \
            f"Incorrect columns in {csv_path}"

        rows = list(reader)
        assert len(rows) > 0, f"File {csv_path} is empty (excluding header)."

def test_daily_summary_json():
    json_path = '/home/user/daily_summary.json'
    assert os.path.exists(json_path), f"Missing required file: {json_path}"

    _, expected_summary = compute_expected_data()
    if expected_summary is None:
        pytest.skip("Raw data file not found, cannot compute expected output.")

    with open(json_path, 'r') as f:
        try:
            actual_summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    # Verify structure and values
    for date_str, sensors in expected_summary.items():
        assert date_str in actual_summary, f"Missing date {date_str} in daily_summary.json"
        for sensor, expected_metrics in sensors.items():
            assert sensor in actual_summary[date_str], f"Missing sensor {sensor} on {date_str} in daily_summary.json"
            actual_metrics = actual_summary[date_str][sensor]

            for metric, expected_val in expected_metrics.items():
                assert metric in actual_metrics, f"Missing metric {metric} for {sensor} on {date_str}"
                actual_val = actual_metrics[metric]
                assert math.isclose(actual_val, expected_val, abs_tol=0.02), \
                    f"Value mismatch for {date_str} {sensor} {metric}. Expected {expected_val}, got {actual_val}"