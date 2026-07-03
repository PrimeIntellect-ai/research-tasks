# test_final_state.py
import csv
import os

def test_clean_output_mse():
    output_path = '/app/clean_output.csv'
    assert os.path.isfile(output_path), f"Expected output file {output_path} is missing."

    expected = {
        "2023-10-01T12:00:00Z": 12.5000,
        "2023-10-01T12:01:00Z": 13.0000,
        "2023-10-01T12:02:00Z": 13.5000,
        "2023-10-01T12:03:00Z": 15.1667,
        "2023-10-01T12:04:00Z": 16.1667,
    }

    sq_errors = []
    count = 0

    with open(output_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames is not None, "CSV header is missing."
        assert 'time' in reader.fieldnames, "Column 'time' is missing in the output CSV."
        assert 'smoothed_value' in reader.fieldnames, "Column 'smoothed_value' is missing in the output CSV."

        for row in reader:
            t = row['time']
            if t in expected:
                try:
                    v = float(row['smoothed_value'])
                except ValueError:
                    assert False, f"Could not parse smoothed_value '{row['smoothed_value']}' as float for time {t}."

                sq_errors.append((v - expected[t])**2)
                count += 1

    assert count == len(expected), f"Expected {len(expected)} matching rows, but found {count}."

    mse = sum(sq_errors) / count
    threshold = 0.001

    assert mse < threshold, f"MSE {mse:.6f} is not strictly less than the threshold {threshold}."