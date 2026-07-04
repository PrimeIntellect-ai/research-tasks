# test_final_state.py

import os
import csv
from collections import defaultdict

def test_script_exists_and_executable():
    """Test that the ETL script exists and is executable."""
    script_path = "/home/user/process_etl.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_output_file_exists():
    """Test that the daily_summary.csv file exists."""
    output_path = "/home/user/data/daily_summary.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_etl_output_correctness():
    """Test that the output data matches the expected ETL logic applied to the raw data."""
    input_path = "/home/user/data/raw_sensor.csv"
    output_path = "/home/user/data/daily_summary.csv"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    # 1. Read and deduplicate (keep first occurrence)
    seen = set()
    records = []
    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 4:
                continue
            ts, sensor, temp, hum = row[0], row[1], row[2], row[3]
            key = (ts, sensor)
            if key not in seen:
                seen.add(key)
                records.append({
                    'ts': ts,
                    'sensor': sensor,
                    'temp': float(temp) if temp.strip() else None,
                    'hum': float(hum) if hum.strip() else None
                })

    # Sort chronologically by timestamp
    records.sort(key=lambda x: x['ts'])

    # 2. Imputation (Forward Fill per sensor)
    last_vals = {}
    for r in records:
        sensor = r['sensor']
        if sensor not in last_vals:
            last_vals[sensor] = {'temp': None, 'hum': None}

        if r['temp'] is not None:
            last_vals[sensor]['temp'] = r['temp']
        else:
            r['temp'] = last_vals[sensor]['temp']

        if r['hum'] is not None:
            last_vals[sensor]['hum'] = r['hum']
        else:
            r['hum'] = last_vals[sensor]['hum']

    # 3. Metric Calculation
    for r in records:
        r['metric'] = r['temp'] + (r['hum'] * 0.1)

    # 4. Rolling Average (window=3)
    sensor_metrics = defaultdict(list)
    for r in records:
        sensor = r['sensor']
        sensor_metrics[sensor].append(r['metric'])
        window = sensor_metrics[sensor][-3:]
        r['rolling_avg'] = sum(window) / len(window)

    # 5. Summary Aggregation
    daily_sensor_avgs = defaultdict(list)
    for r in records:
        date = r['ts'][:10]  # Extract YYYY-MM-DD
        key = (date, r['sensor'])
        daily_sensor_avgs[key].append(r['rolling_avg'])

    expected_output = []
    # Sort by Date ascending, then Sensor ID ascending
    for (date, sensor) in sorted(daily_sensor_avgs.keys()):
        avgs = daily_sensor_avgs[(date, sensor)]
        daily_mean = sum(avgs) / len(avgs)
        # Round to exactly 2 decimal places
        expected_output.append(f"{date},{sensor},{daily_mean:.2f}")

    with open(output_path, 'r') as f:
        actual_output = [line.strip() for line in f if line.strip()]

    assert actual_output == expected_output, (
        f"Output file contents do not match expected.\n"
        f"Expected:\n{chr(10).join(expected_output)}\n\n"
        f"Actual:\n{chr(10).join(actual_output)}"
    )