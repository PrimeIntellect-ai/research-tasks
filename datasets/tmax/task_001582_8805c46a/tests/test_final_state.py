# test_final_state.py

import os
import math
import re
from datetime import datetime, timezone

def test_script_exists_and_executable():
    script_path = "/home/user/clean_data.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_aligned_data_output():
    output_path = "/home/user/aligned_data.tsv"
    sensor_a_path = "/home/user/sensor_A.log"
    sensor_b_path = "/home/user/sensor_B.csv"

    assert os.path.isfile(output_path), f"Output file not found at {output_path}"
    assert os.path.isfile(sensor_a_path), f"Input file not found at {sensor_a_path}"
    assert os.path.isfile(sensor_b_path), f"Input file not found at {sensor_b_path}"

    # Parse sensor_B.csv
    sensor_b_data = []
    with open(sensor_b_path, 'r') as f:
        lines = f.read().strip().split('\n')
        for line in lines[1:]:  # Skip header
            if not line.strip():
                continue
            epoch_str, temp_str = line.split(',')
            sensor_b_data.append((int(epoch_str), temp_str.strip()))

    # Parse sensor_A.log and compute expected output
    expected_lines = []
    log_pattern = re.compile(r'\[(.*?) UTC\] POS: lat=(.*?), lon=(.*)')

    with open(sensor_a_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = log_pattern.match(line)
            assert match, f"Failed to parse sensor_A.log line: {line}"

            dt_str, lat_str, lon_str = match.groups()
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            log_epoch = int(dt.timestamp())

            lat = float(lat_str)
            lon = float(lon_str)
            distance = round(math.sqrt(lat**2 + lon**2), 2)

            # Find closest in sensor_B
            closest_b = None
            min_diff = float('inf')
            for b_epoch, b_temp in sensor_b_data:
                diff = abs(b_epoch - log_epoch)
                if diff < min_diff:
                    min_diff = diff
                    closest_b = (b_epoch, b_temp)

            expected_lines.append(f"{log_epoch}\t{closest_b[0]}\t{distance:.2f}\t{closest_b[1]}")

    expected_output = "\n".join(expected_lines)

    # Read student's output
    with open(output_path, 'r') as f:
        student_output = f.read().strip()

    assert student_output == expected_output, (
        f"Contents of {output_path} do not match expected output.\n"
        f"Expected:\n{expected_output}\n\nGot:\n{student_output}"
    )