# test_final_state.py

import os
import csv
import pytest
from datetime import datetime, timedelta

def parse_time(t_str):
    # Parse RFC3339 e.g. 2023-10-01T10:00:15Z
    return datetime.strptime(t_str, "%Y-%m-%dT%H:%M:%SZ")

def truncate_to_minute(dt):
    return dt.replace(second=0, microsecond=0)

def test_output_csv_exists():
    assert os.path.isfile('/home/user/output.csv'), "/home/user/output.csv is missing"

def test_output_csv_content():
    # Read input files
    temp_file = '/home/user/data/temperature.csv'
    pres_file = '/home/user/data/pressure.csv'

    assert os.path.isfile(temp_file), f"{temp_file} is missing"
    assert os.path.isfile(pres_file), f"{pres_file} is missing"

    temps = []
    with open(temp_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            temps.append((parse_time(row['timestamp']), float(row['temperature'])))

    pressures = []
    with open(pres_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pressures.append((parse_time(row['timestamp']), float(row['pressure'])))

    # Determine min and max minutes
    all_times = [t for t, _ in temps] + [t for t, _ in pressures]
    min_time = truncate_to_minute(min(all_times))
    max_time = truncate_to_minute(max(all_times))

    # Aggregate by minute
    minutes = []
    current = min_time
    while current <= max_time:
        minutes.append(current)
        current += timedelta(minutes=1)

    agg_temps = {m: [] for m in minutes}
    for t, val in temps:
        agg_temps[truncate_to_minute(t)].append(val)

    agg_pressures = {m: [] for m in minutes}
    for t, val in pressures:
        agg_pressures[truncate_to_minute(t)].append(val)

    raw_temps = [sum(agg_temps[m])/len(agg_temps[m]) if agg_temps[m] else None for m in minutes]
    raw_pressures = [sum(agg_pressures[m])/len(agg_pressures[m]) if agg_pressures[m] else None for m in minutes]

    # Impute temperature (forward fill)
    filled_temps = []
    last_temp = None
    for val in raw_temps:
        if val is not None:
            last_temp = val
        filled_temps.append(last_temp)

    # Impute pressure (linear interpolation)
    interp_pressures = list(raw_pressures)
    for i in range(len(interp_pressures)):
        if interp_pressures[i] is None:
            # find prior
            prior_idx = i - 1
            while prior_idx >= 0 and interp_pressures[prior_idx] is None:
                prior_idx -= 1
            # find next
            next_idx = i + 1
            while next_idx < len(interp_pressures) and raw_pressures[next_idx] is None:
                next_idx += 1

            if prior_idx >= 0 and next_idx < len(interp_pressures):
                prior_val = interp_pressures[prior_idx]
                next_val = raw_pressures[next_idx]
                steps = next_idx - prior_idx
                interp_pressures[i] = prior_val + (next_val - prior_val) * (i - prior_idx) / steps

    # Rolling average temperature
    rolling_temps = []
    for i in range(len(filled_temps)):
        start_idx = max(0, i - 4)
        window = filled_temps[start_idx:i+1]
        rolling_temps.append(sum(window)/len(window))

    # Build expected rows
    expected_rows = []
    for i, m in enumerate(minutes):
        expected_rows.append({
            'timestamp': m.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'temp_filled': f"{filled_temps[i]:.2f}",
            'pressure_interpolated': f"{interp_pressures[i]:.2f}",
            'temp_rolling_avg': f"{rolling_temps[i]:.2f}"
        })

    # Read actual output
    actual_rows = []
    with open('/home/user/output.csv', 'r') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['timestamp', 'temp_filled', 'pressure_interpolated', 'temp_rolling_avg'], "CSV headers do not match expected exactly."
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}"

    for i in range(len(expected_rows)):
        assert actual_rows[i]['timestamp'] == expected_rows[i]['timestamp'], f"Row {i} timestamp mismatch: expected {expected_rows[i]['timestamp']}, got {actual_rows[i]['timestamp']}"
        assert actual_rows[i]['temp_filled'] == expected_rows[i]['temp_filled'], f"Row {i} temp_filled mismatch: expected {expected_rows[i]['temp_filled']}, got {actual_rows[i]['temp_filled']}"
        assert actual_rows[i]['pressure_interpolated'] == expected_rows[i]['pressure_interpolated'], f"Row {i} pressure_interpolated mismatch: expected {expected_rows[i]['pressure_interpolated']}, got {actual_rows[i]['pressure_interpolated']}"
        assert actual_rows[i]['temp_rolling_avg'] == expected_rows[i]['temp_rolling_avg'], f"Row {i} temp_rolling_avg mismatch: expected {expected_rows[i]['temp_rolling_avg']}, got {actual_rows[i]['temp_rolling_avg']}"