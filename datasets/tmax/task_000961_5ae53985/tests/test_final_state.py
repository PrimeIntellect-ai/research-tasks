# test_final_state.py

import os
import pytest

def test_anomalies_csv():
    cpu_file = "/home/user/cpu.csv"
    mem_file = "/home/user/mem.csv"
    anomalies_file = "/home/user/anomalies.csv"

    assert os.path.isfile(anomalies_file), f"Output file {anomalies_file} is missing."

    # Parse CPU data
    cpu_data = {}
    if os.path.exists(cpu_file):
        with open(cpu_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    ts, cpu = line.split(',')
                    cpu_data[int(ts)] = int(cpu)

    # Parse Memory data
    mem_data = {}
    if os.path.exists(mem_file):
        with open(mem_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    ts, mem = line.split(',')
                    mem_data[int(ts)] = int(mem)

    # Join on timestamp and sort chronologically
    common_ts = sorted(list(set(cpu_data.keys()).intersection(set(mem_data.keys()))))

    # Compute expected anomalies
    expected_anomalies = []
    prev_cpu = None
    for ts in common_ts:
        curr_cpu = cpu_data[ts]
        curr_mem = mem_data[ts]

        if prev_cpu is not None:
            cpu_diff = curr_cpu - prev_cpu
            if cpu_diff >= 50 and curr_mem >= 90:
                expected_anomalies.append(f"{ts},{curr_cpu},{curr_mem},{cpu_diff}")

        prev_cpu = curr_cpu

    # Read actual anomalies
    with open(anomalies_file, 'r') as f:
        actual_anomalies = [line.strip() for line in f if line.strip()]

    assert actual_anomalies == expected_anomalies, (
        f"Contents of {anomalies_file} do not match the expected anomalies.\n"
        f"Expected: {expected_anomalies}\n"
        f"Actual: {actual_anomalies}"
    )