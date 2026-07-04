# test_final_state.py
import os
import re
import pytest
import numpy as np
import pandas as pd

def test_fastcsv_max_columns_fixed():
    header_path = "/app/fastcsv-1.0/fastcsv.h"
    assert os.path.isfile(header_path), f"fastcsv.h not found at {header_path}"

    with open(header_path, "r") as f:
        content = f.read()

    # Find MAX_COLUMNS
    match = re.search(r"#define\s+MAX_COLUMNS\s+(\d+)", content)
    assert match is not None, "Could not find #define MAX_COLUMNS in fastcsv.h"

    max_cols = int(match.group(1))
    assert max_cols >= 5, f"MAX_COLUMNS is {max_cols}, expected at least 5 to parse the dataset"

def test_bootstrap_results():
    results_path = "/home/user/bootstrap_results.txt"
    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    with open(results_path, "r") as f:
        text = f.read()

    mean_match = re.search(r"Sample Mean:\s*([\d\.]+)", text)
    se_match = re.search(r"Standard Error:\s*([\d\.]+)", text)

    assert mean_match is not None, "Sample Mean not found in output. File content:\n" + text
    assert se_match is not None, "Standard Error not found in output. File content:\n" + text

    agent_mean = float(mean_match.group(1))
    agent_se = float(se_match.group(1))

    csv_path = "/home/user/data/sales.csv"
    assert os.path.isfile(csv_path), f"Data file missing at {csv_path}"

    df = pd.read_csv(csv_path)
    amounts = df['amount'].values
    expected_mean = np.mean(amounts)
    expected_se = np.std(amounts, ddof=1) / np.sqrt(len(amounts))

    mean_diff = abs(agent_mean - expected_mean)
    se_diff = abs(agent_se - expected_se)

    assert mean_diff <= 0.05, f"Mean difference {mean_diff} exceeds tolerance 0.05. Agent: {agent_mean}, Expected: {expected_mean}"
    assert se_diff <= 0.015, f"SE difference {se_diff} exceeds tolerance 0.015. Agent: {agent_se}, Expected: {expected_se}"