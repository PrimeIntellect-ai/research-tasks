# test_final_state.py
import os
import csv
import re

def test_sensor_readings_copied():
    path = "/home/user/workspace/sensor_readings.csv"
    assert os.path.isfile(path), f"File {path} does not exist. Did you copy it from /tmp/remote_data/?"

def test_c_program_exists_and_parallel():
    path = "/home/user/workspace/process.c"
    assert os.path.isfile(path), f"C program source {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    # Check for OpenMP or pthreads usage
    has_omp = "omp.h" in content or "#pragma omp" in content
    has_pthread = "pthread.h" in content or "pthread_create" in content

    assert has_omp or has_pthread, "The C program does not appear to use OpenMP or pthreads for parallelization."

def test_metrics_output_correctness():
    path = "/home/user/workspace/metrics.csv"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    # Calculate expected values
    expected = {}
    for t in range(10):
        total = 0.0
        for i in range(1, 10001):
            val = (i % 100) + t * 2.5
            total += val * val
        expected[f"T{t}"] = f"{total:.2f}"

    with open(path, 'r', newline='') as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, f"File {path} is empty."

    header = reader[0]
    assert header == ['TimeStep', 'SumOfSquares'], f"Header is incorrect. Expected ['TimeStep', 'SumOfSquares'], got {header}"

    data_rows = reader[1:]
    assert len(data_rows) == 10, f"Expected 10 data rows, got {len(data_rows)}"

    # Check sorting and values
    for t in range(10):
        ts = f"T{t}"
        row = data_rows[t]
        assert len(row) == 2, f"Row {t+1} does not have exactly 2 columns: {row}"
        assert row[0] == ts, f"Expected TimeStep {ts} at row {t+1}, got {row[0]}. Ensure the output is sorted."
        assert row[1] == expected[ts], f"Incorrect SumOfSquares for {ts}. Expected {expected[ts]}, got {row[1]}."