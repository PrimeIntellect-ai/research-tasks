# test_final_state.py

import os
import csv
import math

def compute_expected():
    raw_file = '/home/user/raw_sensor.csv'
    x = 20.0
    p = 5.0
    r = 2.0
    q = 0.1

    expected_rows = []
    mse_sum = 0.0
    count = 0

    with open(raw_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            time_val = float(row['Time'])
            measurement = float(row['Measurement'])

            # Predict
            x_pred = x
            p_pred = p + q

            # Update
            k = p_pred / (p_pred + r)
            x = x_pred + k * (measurement - x_pred)
            p = (1.0 - k) * p_pred

            expected_rows.append((time_val, measurement, x))
            mse_sum += (measurement - x) ** 2
            count += 1

    mse = mse_sum / count if count > 0 else 0.0
    return expected_rows, mse

def test_filter_c_exists():
    assert os.path.exists('/home/user/filter.c'), "The file /home/user/filter.c does not exist."

def test_smoothed_sensor_csv():
    output_file = '/home/user/smoothed_sensor.csv'
    assert os.path.exists(output_file), f"The file {output_file} does not exist."

    expected_rows, _ = compute_expected()

    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['Time', 'Measurement', 'Smoothed'], f"Incorrect header in {output_file}."

        output_rows = list(reader)
        assert len(output_rows) == len(expected_rows), "Output file does not have the same number of rows as the input file."

        for i, (out_row, exp_row) in enumerate(zip(output_rows, expected_rows)):
            assert len(out_row) == 3, f"Row {i+1} does not have exactly 3 columns."

            out_time = float(out_row[0])
            out_meas = float(out_row[1])
            out_smooth = float(out_row[2])

            exp_time, exp_meas, exp_smooth = exp_row

            assert math.isclose(out_time, exp_time, rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1}: Time mismatch."
            assert math.isclose(out_meas, exp_meas, rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1}: Measurement mismatch."
            assert math.isclose(out_smooth, exp_smooth, rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1}: Smoothed value mismatch. Expected {exp_smooth:.4f}, got {out_smooth:.4f}."

def test_mse_txt():
    mse_file = '/home/user/mse.txt'
    assert os.path.exists(mse_file), f"The file {mse_file} does not exist."

    _, expected_mse = compute_expected()

    with open(mse_file, 'r') as f:
        content = f.read().strip()

    try:
        actual_mse = float(content)
    except ValueError:
        assert False, f"Content of {mse_file} is not a valid float."

    assert math.isclose(actual_mse, expected_mse, rel_tol=1e-4, abs_tol=1e-4), f"MSE value mismatch. Expected {expected_mse:.4f}, got {actual_mse:.4f}."