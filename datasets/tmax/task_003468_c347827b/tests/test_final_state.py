# test_final_state.py

import os
import csv
import math
import subprocess
import tempfile
import pytest

BINARY_PATH = "/home/user/pipeline_manager/target/release/pipeline_manager"
PROJECT_DIR = "/home/user/pipeline_manager"

def run_validate(file_path):
    if os.path.isfile(BINARY_PATH):
        cmd = [BINARY_PATH, "validate", file_path]
        cwd = PROJECT_DIR
    else:
        cmd = ["cargo", "run", "--release", "--", "validate", file_path]
        cwd = PROJECT_DIR

    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode

def run_engineer(input_path, output_path):
    if os.path.isfile(BINARY_PATH):
        cmd = [BINARY_PATH, "engineer", input_path, output_path]
        cwd = PROJECT_DIR
    else:
        cmd = ["cargo", "run", "--release", "--", "engineer", input_path, output_path]
        cwd = PROJECT_DIR

    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode

def test_validate_adversarial_corpus():
    evil_dir = "/app/evil_corpus"
    clean_dir = "/app/clean_corpus"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        if run_validate(f) != 1:
            evil_bypassed.append(os.path.basename(f))

    for f in clean_files:
        if run_validate(f) != 0:
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, "Adversarial corpus validation failed: " + "; ".join(errors)

def test_engineer_data_leakage():
    input_path = "/app/leak_test_input.csv"
    assert os.path.isfile(input_path), f"Missing input file: {input_path}"

    # Compute expected stats
    train_amounts = []
    train_ages = []
    with open(input_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['split_type'] == 'train':
                train_amounts.append(float(row['amount']))
                train_ages.append(float(row['account_age']))

    def mean_std(values):
        n = len(values)
        if n < 2:
            return sum(values)/n, 0.0
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        return mean, math.sqrt(variance)

    mean_amt, std_amt = mean_std(train_amounts)
    mean_age, std_age = mean_std(train_ages)

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        output_path = tmp.name

    try:
        ret = run_engineer(input_path, output_path)
        assert ret == 0, f"Engineer command failed with exit code {ret}"

        with open(input_path, 'r') as f_in, open(output_path, 'r') as f_out:
            reader_in = list(csv.DictReader(f_in))
            reader_out = list(csv.DictReader(f_out))

            assert len(reader_in) == len(reader_out), "Output CSV row count mismatch"

            for row_in, row_out in zip(reader_in, reader_out):
                orig_amt = float(row_in['amount'])
                orig_age = float(row_in['account_age'])

                exp_amt = (orig_amt - mean_amt) / std_amt
                exp_age = (orig_age - mean_age) / std_age

                out_amt = float(row_out['amount'])
                out_age = float(row_out['account_age'])

                assert math.isclose(out_amt, exp_amt, rel_tol=1e-3, abs_tol=1e-3), \
                    f"Amount mismatch for row {row_in['transaction_id']}: expected {exp_amt:.4f}, got {out_amt}"
                assert math.isclose(out_age, exp_age, rel_tol=1e-3, abs_tol=1e-3), \
                    f"Age mismatch for row {row_in['transaction_id']}: expected {exp_age:.4f}, got {out_age}"
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)