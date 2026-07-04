# test_final_state.py

import os
import math
import re
import pytest

RAW_DATA_PATH = "/home/user/data/telemetry.csv"
OUTPUT_DIR = "/home/user/output"
CLEANED_CSV_PATH = os.path.join(OUTPUT_DIR, "cleaned.csv")
CORRELATION_PATH = os.path.join(OUTPUT_DIR, "correlation.txt")
BAYES_PATH = os.path.join(OUTPUT_DIR, "bayes.txt")
RETRIEVAL_PATH = os.path.join(OUTPUT_DIR, "retrieval.txt")

def get_cleaned_data():
    if not os.path.exists(RAW_DATA_PATH):
        pytest.fail(f"Raw data file missing: {RAW_DATA_PATH}")

    with open(RAW_DATA_PATH, "r") as f:
        lines = f.read().strip().splitlines()

    if not lines:
        return []

    header = lines[0]
    raw_rows = lines[1:]

    cleaned = []
    for row in raw_rows:
        cols = row.split(",")
        if len(cols) < 6:
            continue
        cpu_str = cols[2].strip()
        ram_str = cols[3].strip()

        if not cpu_str or not ram_str:
            continue

        try:
            cpu = float(cpu_str)
            ram = float(ram_str)
        except ValueError:
            continue

        if cpu < 0 or cpu > 100:
            continue

        cleaned.append(row)
    return cleaned

def test_cleaned_csv():
    assert os.path.exists(CLEANED_CSV_PATH), f"Missing file: {CLEANED_CSV_PATH}"

    expected_cleaned = get_cleaned_data()

    with open(CLEANED_CSV_PATH, "r") as f:
        actual_cleaned = f.read().strip().splitlines()

    assert actual_cleaned == expected_cleaned, "Cleaned CSV content does not match expected output."

def test_correlation():
    assert os.path.exists(CORRELATION_PATH), f"Missing file: {CORRELATION_PATH}"

    cleaned = get_cleaned_data()
    x = []
    y = []
    for row in cleaned:
        cols = row.split(",")
        x.append(float(cols[2]))
        y.append(float(cols[3]))

    n = len(x)
    if n == 0:
        expected_corr = 0.0
    else:
        sum_x = sum(x)
        sum_y = sum(y)
        sum_x_sq = sum(xi*xi for xi in x)
        sum_y_sq = sum(yi*yi for yi in y)
        sum_xy = sum(xi*yi for xi, yi in zip(x, y))

        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2))

        expected_corr = numerator / denominator if denominator != 0 else 0.0

    expected_str = f"{expected_corr:.3f}"

    with open(CORRELATION_PATH, "r") as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Correlation coefficient mismatch. Expected {expected_str}, got {actual_str}"

def test_bayes():
    assert os.path.exists(BAYES_PATH), f"Missing file: {BAYES_PATH}"

    cleaned = get_cleaned_data()
    count_cpu_gt_85 = 0
    count_crash_and_cpu_gt_85 = 0

    for row in cleaned:
        cols = row.split(",")
        cpu = float(cols[2])
        status = cols[4].strip()

        if cpu > 85.0:
            count_cpu_gt_85 += 1
            if status == "CRASH":
                count_crash_and_cpu_gt_85 += 1

    if count_cpu_gt_85 == 0:
        expected_prob = 0.0
    else:
        expected_prob = count_crash_and_cpu_gt_85 / count_cpu_gt_85

    expected_str = f"{expected_prob:.3f}"

    with open(BAYES_PATH, "r") as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Bayesian probability mismatch. Expected {expected_str}, got {actual_str}"

def test_retrieval():
    assert os.path.exists(RETRIEVAL_PATH), f"Missing file: {RETRIEVAL_PATH}"

    cleaned = get_cleaned_data()
    target_query = "database connection timeout"

    def tokenize(text):
        return set(re.findall(r'[a-z]+', text.lower()))

    target_set = tokenize(target_query)

    best_jaccard = -1.0
    best_msg = ""
    best_timestamp = float('inf')

    for row in cleaned:
        cols = row.split(",")
        timestamp = float(cols[0])
        status = cols[4].strip()
        log_message = ",".join(cols[5:]).strip()

        if status == "CRASH":
            msg_set = tokenize(log_message)
            intersection = len(target_set.intersection(msg_set))
            union = len(target_set.union(msg_set))
            jaccard = intersection / union if union > 0 else 0.0

            if jaccard > best_jaccard:
                best_jaccard = jaccard
                best_msg = log_message
                best_timestamp = timestamp
            elif jaccard == best_jaccard and timestamp < best_timestamp:
                best_msg = log_message
                best_timestamp = timestamp

    with open(RETRIEVAL_PATH, "r") as f:
        actual_msg = f.read().strip()

    assert actual_msg == best_msg, f"Retrieval mismatch. Expected '{best_msg}', got '{actual_msg}'"