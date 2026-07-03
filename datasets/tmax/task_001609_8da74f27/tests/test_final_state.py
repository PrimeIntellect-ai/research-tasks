# test_final_state.py
import os
import csv
from datetime import datetime

def parse_datetime(dt_str):
    if not dt_str:
        return None
    try:
        # Handle formats like "2023-01-01 00:00:00"
        return datetime.fromisoformat(dt_str.replace(" ", "T"))
    except ValueError:
        return None

def compute_mean(values):
    if not values:
        return 0.0
    return sum(values) / len(values)

def compute_median(values):
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n % 2 == 1:
        return sorted_vals[n // 2]
    else:
        return (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2.0

def test_clean_data_exists_and_correct():
    raw_file = '/home/user/raw_sensor_data.csv'
    clean_file = '/home/user/clean_data.csv'

    assert os.path.isfile(raw_file), f"Raw data file {raw_file} is missing."
    assert os.path.isfile(clean_file), f"Clean data file {clean_file} is missing. Did you run your script?"

    # Read raw data
    raw_data = []
    with open(raw_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_data.append(row)

    # 1. Filter missing timestamp
    filtered_data = []
    for row in raw_data:
        if row['timestamp'] and row['timestamp'].strip():
            filtered_data.append(row)

    # 2. Neutralize outliers
    for row in filtered_data:
        try:
            temp = float(row['temperature_c'])
            if temp > 80.0 or temp < -30.0:
                row['temperature_c'] = ''
        except ValueError:
            row['temperature_c'] = ''

    # 3. Impute
    sensor_temps = {}
    sensor_hums = {}
    for row in filtered_data:
        sid = row['sensor_id']
        if sid not in sensor_temps:
            sensor_temps[sid] = []
            sensor_hums[sid] = []

        try:
            t = float(row['temperature_c'])
            sensor_temps[sid].append(t)
        except ValueError:
            pass

        try:
            h = float(row['humidity'])
            sensor_hums[sid].append(h)
        except ValueError:
            pass

    mean_temps = {sid: round(compute_mean(vals), 2) for sid, vals in sensor_temps.items()}
    median_hums = {sid: round(compute_median(vals), 1) for sid, vals in sensor_hums.items()}

    for row in filtered_data:
        sid = row['sensor_id']
        try:
            float(row['temperature_c'])
        except ValueError:
            row['temperature_c'] = mean_temps.get(sid, 0.0)

        try:
            float(row['humidity'])
        except ValueError:
            row['humidity'] = median_hums.get(sid, 0.0)

    # 4. Feature Engineering
    for row in filtered_data:
        temp_c = float(row['temperature_c'])
        row['temp_f'] = round(temp_c * 9/5 + 32, 2)

        dt = parse_datetime(row['timestamp'])
        row['hour_of_day'] = dt.hour if dt else 0

    # 5. Sorting
    def sort_key(row):
        dt = parse_datetime(row['timestamp'])
        return (dt, row['sensor_id'])

    filtered_data.sort(key=sort_key)

    # Format expected output
    expected_rows = []
    for row in filtered_data:
        dt = parse_datetime(row['timestamp'])
        expected_rows.append({
            'timestamp': str(dt),
            'sensor_id': row['sensor_id'],
            'temperature_c': f"{float(row['temperature_c']):.2f}".rstrip('0').rstrip('.'), # approximation of pandas output
            'humidity': f"{float(row['humidity']):.1f}".rstrip('0').rstrip('.'),
            'temp_f': f"{float(row['temp_f']):.2f}".rstrip('0').rstrip('.'),
            'hour_of_day': str(row['hour_of_day'])
        })

    # Read clean data
    clean_data = []
    with open(clean_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['timestamp', 'sensor_id', 'temperature_c', 'humidity', 'temp_f', 'hour_of_day'], "Incorrect columns in clean_data.csv"
        for row in reader:
            clean_data.append(row)

    assert len(clean_data) == len(expected_rows), f"Expected {len(expected_rows)} rows, found {len(clean_data)}"

    for i, (actual, expected) in enumerate(zip(clean_data, expected_rows)):
        # Check parsed dates to avoid strict string match issues
        actual_dt = parse_datetime(actual['timestamp'])
        expected_dt = parse_datetime(expected['timestamp'])
        assert actual_dt == expected_dt, f"Row {i+1}: Expected timestamp {expected_dt}, got {actual_dt}"

        assert actual['sensor_id'] == expected['sensor_id'], f"Row {i+1}: Expected sensor_id {expected['sensor_id']}, got {actual['sensor_id']}"

        assert abs(float(actual['temperature_c']) - float(expected['temperature_c'])) < 1e-5, f"Row {i+1}: Expected temperature_c {expected['temperature_c']}, got {actual['temperature_c']}"
        assert abs(float(actual['humidity']) - float(expected['humidity'])) < 1e-5, f"Row {i+1}: Expected humidity {expected['humidity']}, got {actual['humidity']}"
        assert abs(float(actual['temp_f']) - float(expected['temp_f'])) < 1e-5, f"Row {i+1}: Expected temp_f {expected['temp_f']}, got {actual['temp_f']}"

        assert int(actual['hour_of_day']) == int(expected['hour_of_day']), f"Row {i+1}: Expected hour_of_day {expected['hour_of_day']}, got {actual['hour_of_day']}"