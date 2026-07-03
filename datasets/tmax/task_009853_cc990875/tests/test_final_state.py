# test_final_state.py

import os
import csv
import pytest

def test_source_and_executable_exist():
    """Ensure the C++ source file and the compiled executable exist."""
    source_path = "/home/user/etl_validator.cpp"
    exec_path = "/home/user/etl_validator"

    assert os.path.isfile(source_path), f"C++ source file missing: {source_path}"
    assert os.path.isfile(exec_path), f"Compiled executable missing: {exec_path}"
    assert os.access(exec_path, os.X_OK), f"File is not executable: {exec_path}"

def test_etl_log_contents():
    """Validate the contents of etl_log.txt by recomputing the expected output from input_data.csv."""
    input_path = "/home/user/input_data.csv"
    log_path = "/home/user/etl_log.txt"

    assert os.path.isfile(input_path), f"Input data file missing: {input_path}"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    expected_logs = []
    valid_rows_count = 0

    with open(input_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["id", "prior_prob", "likelihood", "evidence", "expected_posterior"], "Input CSV header is incorrect."

        for row in reader:
            if not row:
                continue

            row_id = int(row[0])
            prior_prob = float(row[1])
            likelihood = float(row[2])
            evidence = float(row[3])
            expected_posterior = float(row[4])

            # Schema validation
            if prior_prob < 0.0 or prior_prob > 1.0 or evidence == 0.0:
                expected_logs.append(f"SCHEMA_ERROR: id {row_id}")
                continue

            # Bayesian Inference & Numerical Accuracy
            posterior = (likelihood * prior_prob) / evidence
            if abs(posterior - expected_posterior) > 0.0001:
                expected_logs.append(f"ACCURACY_ERROR: id {row_id}")

            valid_rows_count += 1

    expected_logs.append(f"BENCHMARK_PROCESSED: {valid_rows_count} valid rows")

    with open(log_path, "r") as f:
        actual_logs = [line.strip() for line in f if line.strip()]

    assert actual_logs == expected_logs, (
        f"Log contents do not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_logs)}\n\n"
        f"Actual:\n{chr(10).join(actual_logs)}"
    )