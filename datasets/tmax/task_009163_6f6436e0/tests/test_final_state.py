# test_final_state.py
import os
import re
import pytest

def get_expected_outputs():
    log_file = "/home/user/iot_sensors.log"
    valid_regex = re.compile(r'^\[(\d{4}-\d{2}-\d{2}) (\d{2}):\d{2}:\d{2}\] \[SENS-\d{4}:([A-Z]+)\] (OK|ERROR) .+$')

    error_counts = {}
    ok_samples = []
    ok_counts = {}

    with open(log_file, 'r') as f:
        for line in f:
            line_stripped = line.strip('\n')
            match = valid_regex.match(line_stripped)
            if not match:
                continue
            date, hour, sens_type, status = match.groups()

            if status == 'ERROR':
                key = (date, hour, sens_type)
                error_counts[key] = error_counts.get(key, 0) + 1
            elif status == 'OK':
                ok_counts[sens_type] = ok_counts.get(sens_type, 0) + 1
                if ok_counts[sens_type] % 10 == 1:
                    ok_samples.append(line_stripped)

    expected_error_summary = []
    for (date, hour, sens_type), count in error_counts.items():
        expected_error_summary.append(f"{date},{hour},{sens_type},{count}")
    expected_error_summary.sort()

    return expected_error_summary, ok_samples

def test_script_exists_and_executable():
    script_path = "/home/user/process_logs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_error_summary_csv():
    output_file = "/home/user/error_summary.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        actual_lines = [line.strip('\n') for line in f if line.strip('\n')]

    expected_error_summary, _ = get_expected_outputs()

    # The requirement says "sorted chronologically, then by Type", which matches a standard sort of the strings.
    # We sort the actual lines just in case, but we also assert it was already sorted.
    assert actual_lines == sorted(actual_lines), f"{output_file} is not sorted correctly."

    assert sorted(actual_lines) == expected_error_summary, f"Contents of {output_file} do not match the expected aggregated counts."

def test_sampled_ok_log():
    output_file = "/home/user/sampled_ok.log"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        actual_lines = [line.strip('\n') for line in f if line.strip('\n')]

    _, expected_ok_samples = get_expected_outputs()

    assert actual_lines == expected_ok_samples, f"Contents of {output_file} do not match the expected sampled OK logs."