# test_final_state.py

import os
import json
import csv

def compute_expected_output(csv_path):
    valid_data = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            temp = float(row['temperature'])
            hum = float(row['humidity'])
            sensor_id = row['sensor_id']
            timestamp = row['timestamp']

            if -20.0 <= temp <= 50.0 and 0.0 <= hum <= 100.0:
                if sensor_id not in valid_data:
                    valid_data[sensor_id] = []
                valid_data[sensor_id].append({'time': timestamp, 'temp': temp, 'hum': hum})

    # Ensure chronological processing
    for sensor_id in valid_data:
        valid_data[sensor_id].sort(key=lambda x: x['time'])

    rolling_temp_sma = {}
    max_humidity = {}

    for sensor_id, records in valid_data.items():
        if not records:
            continue

        # Summary Aggregation: Max Humidity
        max_humidity[sensor_id] = round(max(r['hum'] for r in records), 1)

        # Rolling Aggregation: SMA of valid temperatures
        sma = []
        temps = [r['temp'] for r in records]
        for i in range(len(temps) - 2):
            window = temps[i:i+3]
            avg = sum(window) / 3.0
            sma.append(round(avg, 1))
        rolling_temp_sma[sensor_id] = sma

    return {
        "rolling_temp_sma": rolling_temp_sma,
        "max_humidity": max_humidity
    }

def test_etl_output_exists():
    output_path = "/home/user/etl_output.json"
    assert os.path.exists(output_path), f"The expected output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a valid file."

def test_etl_output_correctness():
    csv_path = "/home/user/sensor_data.csv"
    output_path = "/home/user/etl_output.json"

    assert os.path.exists(csv_path), f"The input file {csv_path} is missing."
    assert os.path.exists(output_path), f"The output file {output_path} is missing."

    # Compute the expected result based on the task rules
    expected_result = compute_expected_output(csv_path)

    # Load the student's output
    try:
        with open(output_path, 'r') as f:
            actual_result = json.load(f)
    except json.JSONDecodeError:
        assert False, f"The file {output_path} does not contain valid JSON."

    # Check top-level keys
    assert "rolling_temp_sma" in actual_result, "Missing 'rolling_temp_sma' key in the output JSON."
    assert "max_humidity" in actual_result, "Missing 'max_humidity' key in the output JSON."

    # Compare max_humidity
    expected_max_hum = expected_result["max_humidity"]
    actual_max_hum = actual_result["max_humidity"]

    for sensor_id, expected_val in expected_max_hum.items():
        assert sensor_id in actual_max_hum, f"Missing sensor_id '{sensor_id}' in 'max_humidity'."
        assert actual_max_hum[sensor_id] == expected_val, (
            f"Incorrect max_humidity for sensor '{sensor_id}'. "
            f"Expected {expected_val}, got {actual_max_hum[sensor_id]}."
        )

    # Compare rolling_temp_sma
    expected_sma = expected_result["rolling_temp_sma"]
    actual_sma = actual_result["rolling_temp_sma"]

    for sensor_id, expected_val in expected_sma.items():
        assert sensor_id in actual_sma, f"Missing sensor_id '{sensor_id}' in 'rolling_temp_sma'."
        assert actual_sma[sensor_id] == expected_val, (
            f"Incorrect rolling_temp_sma for sensor '{sensor_id}'. "
            f"Expected {expected_val}, got {actual_sma[sensor_id]}."
        )