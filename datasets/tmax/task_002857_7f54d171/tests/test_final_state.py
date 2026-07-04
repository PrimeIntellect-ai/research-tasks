# test_final_state.py

import os
import pytest
from collections import defaultdict

def test_cleaner_c_exists():
    assert os.path.isfile("/home/user/cleaner.c"), "The source file /home/user/cleaner.c does not exist."

def test_cleaner_executable_exists():
    assert os.path.isfile("/home/user/cleaner"), "The compiled executable /home/user/cleaner does not exist."
    assert os.access("/home/user/cleaner", os.X_OK), "The file /home/user/cleaner is not executable."

def test_cleaned_sensor_data_content():
    input_file = "/home/user/raw_sensor_data.csv"
    output_file = "/home/user/cleaned_sensor_data.csv"

    assert os.path.isfile(output_file), f"The output file {output_file} does not exist."

    with open(input_file, "rb") as f:
        raw_lines = f.read().splitlines()

    if not raw_lines:
        pytest.fail("Input file is empty.")

    header = raw_lines[0].decode('ascii')

    seen_keys = set()
    sensor_history = defaultdict(list)

    expected_output_lines = []
    expected_output_lines.append("timestamp_ms,sensor_id,temperature,humidity,rolling_avg_temp,status_message")

    for line in raw_lines[1:]:
        if not line.strip():
            continue

        parts = line.split(b',')
        if len(parts) < 5:
            continue

        timestamp_ms = int(parts[0])
        sensor_id = parts[1].decode('ascii')
        temperature = float(parts[2])
        humidity = float(parts[3])
        status_message_bytes = b','.join(parts[4:])

        # 1. Character Encoding Sanitization
        sanitized_status_chars = []
        for b in status_message_bytes:
            if b > 127:
                sanitized_status_chars.append('?')
            else:
                sanitized_status_chars.append(chr(b))
        status_message = "".join(sanitized_status_chars)

        # 2. Constraint Validation
        if not (-50.0 <= temperature <= 150.0):
            continue
        if not (0.0 <= humidity <= 100.0):
            continue

        # 3. Deduplication
        key = (timestamp_ms, sensor_id)
        if key in seen_keys:
            continue
        seen_keys.add(key)

        # 4. Windowed Aggregation
        sensor_history[sensor_id].append(temperature)
        recent_temps = sensor_history[sensor_id][-3:]
        rolling_avg = sum(recent_temps) / len(recent_temps)

        # 5. Output Format
        formatted_line = f"{timestamp_ms},{sensor_id},{temperature:.1f},{humidity:.1f},{rolling_avg:.2f},{status_message}"
        expected_output_lines.append(formatted_line)

    expected_output = "\n".join(expected_output_lines) + "\n"

    with open(output_file, "r", encoding="utf-8") as f:
        actual_output = f.read()

    # Standardize line endings for comparison
    expected_output = expected_output.replace("\r\n", "\n")
    actual_output = actual_output.replace("\r\n", "\n")

    assert actual_output == expected_output, "The content of cleaned_sensor_data.csv does not match the expected processed data."