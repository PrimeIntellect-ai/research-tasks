# test_final_state.py

import os
import csv
import pytest

def get_expected_anomalies(input_path):
    """Compute the expected anomalies based on the rules in the task."""
    anomalies = []
    sensor_counts = {}
    sensor_prev_kept = {}

    with open(input_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                val = float(row['value'])
            except ValueError:
                continue

            # Constraint-based validation
            if val < -50.0 or val > 150.0:
                continue

            sensor = row['sensor_id']
            count = sensor_counts.get(sensor, 0)
            sensor_counts[sensor] = count + 1

            # Stratified Sampling: keep every 5th valid row (0-indexed -> count % 5 == 0)
            if count % 5 == 0:
                if sensor in sensor_prev_kept:
                    prev_val = sensor_prev_kept[sensor]
                    delta = abs(val - prev_val)
                    # Anomaly Detection
                    if delta > 20.0:
                        # Format floats to 1 decimal place as required
                        anomalies.append({
                            'timestamp': row['timestamp'],
                            'sensor_id': sensor,
                            'value': str(val) if '.' in str(val) else f"{val:.1f}",
                            'delta': f"{delta:.1f}"
                        })
                sensor_prev_kept[sensor] = val

    return anomalies

def test_anomalies_file_exists():
    """Test that the output anomalies.csv file has been created."""
    output_path = "/home/user/anomalies.csv"
    assert os.path.isfile(output_path), f"The expected output file {output_path} is missing."

def test_anomalies_content():
    """Test that anomalies.csv contains the correct headers and computed anomalies."""
    input_path = "/home/user/sensor_data.csv"
    output_path = "/home/user/anomalies.csv"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    expected_anomalies = get_expected_anomalies(input_path)

    with open(output_path, 'r') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"The file {output_path} is empty.")

        expected_headers = ['timestamp', 'sensor_id', 'value', 'delta']
        assert headers == expected_headers, f"Headers in {output_path} are incorrect. Expected {expected_headers}, got {headers}."

        actual_anomalies = []
        for row in reader:
            if not row:
                continue
            assert len(row) == 4, f"Row {row} does not have exactly 4 columns."

            # Ensure value and delta are formatted to 1 decimal place where applicable
            # The test checks if the parsed values match the expected formatted strings
            # To be robust against slight formatting differences like 46.0 vs 46, we parse them as floats for comparison
            actual_anomalies.append({
                'timestamp': row[0],
                'sensor_id': row[1],
                'value': float(row[2]),
                'delta': float(row[3])
            })

    assert len(actual_anomalies) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies, but found {len(actual_anomalies)}."

    for i, (actual, expected) in enumerate(zip(actual_anomalies, expected_anomalies)):
        assert actual['timestamp'] == expected['timestamp'], f"Row {i+1}: expected timestamp {expected['timestamp']}, got {actual['timestamp']}."
        assert actual['sensor_id'] == expected['sensor_id'], f"Row {i+1}: expected sensor_id {expected['sensor_id']}, got {actual['sensor_id']}."
        assert actual['value'] == float(expected['value']), f"Row {i+1}: expected value {expected['value']}, got {actual['value']}."
        assert actual['delta'] == float(expected['delta']), f"Row {i+1}: expected delta {expected['delta']}, got {actual['delta']}."