# test_final_state.py

import os
import pytest
from decimal import Decimal, getcontext, ROUND_DOWN

def test_final_state_csv_exists():
    filepath = "/home/user/telemetry/final_state.csv"
    assert os.path.isfile(filepath), f"The required output file {filepath} does not exist."

def test_final_state_csv_content():
    initial_filepath = "/home/user/telemetry/initial_state.csv"
    wal_filepath = "/home/user/telemetry/sensor.wal"
    final_filepath = "/home/user/telemetry/final_state.csv"

    assert os.path.isfile(initial_filepath), "Missing initial_state.csv"
    assert os.path.isfile(wal_filepath), "Missing sensor.wal"
    assert os.path.isfile(final_filepath), "Missing final_state.csv"

    # Set up Decimal context to mimic bc scale=4
    getcontext().prec = 28

    # Parse initial state
    state = {}
    with open(initial_filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sensor, val = line.split(',')
            state[sensor] = Decimal(val).quantize(Decimal('0.0000'), rounding=ROUND_DOWN)

    # Process WAL
    with open(wal_filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 3:
                continue
            seq, sensor, val_str = parts

            # Check if val_str is a valid float
            try:
                val = Decimal(val_str)
            except Exception:
                # Skip invalid float (corrupted entry)
                continue

            if sensor in state:
                curr_val = state[sensor]
                # Formula: (curr_val * 0.9) + (val * 0.1)
                term1 = (curr_val * Decimal('0.9')).quantize(Decimal('0.0000'), rounding=ROUND_DOWN)
                term2 = (val * Decimal('0.1')).quantize(Decimal('0.0000'), rounding=ROUND_DOWN)
                new_val = (term1 + term2).quantize(Decimal('0.0000'), rounding=ROUND_DOWN)
                state[sensor] = new_val

    # Parse final state
    actual_state = {}
    with open(final_filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            assert len(parts) == 2, f"Invalid format in final_state.csv: {line}"
            sensor, val = parts
            actual_state[sensor] = val

    # Verify actual vs expected
    for sensor, expected_val in state.items():
        expected_str = f"{expected_val:.4f}"
        assert sensor in actual_state, f"Sensor {sensor} missing from final_state.csv"
        actual_val = actual_state[sensor]
        assert actual_val == expected_str, f"Sensor {sensor} has incorrect EMA. Expected {expected_str}, got {actual_val}"

    # Ensure no extra sensors
    for sensor in actual_state:
        assert sensor in state, f"Unexpected sensor {sensor} found in final_state.csv"