# test_final_state.py

import os
import csv
import math
import pytest

def compute_expected_stats(log_path):
    stats = {}
    if not os.path.exists(log_path):
        return stats

    with open(log_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 2:
                continue

            qid = parts[0]
            val_str = parts[1]

            # Replicate the float parsing behavior:
            # Rust's f64::from_str handles standard floats. The task says to ignore malformed ones.
            try:
                # In Python, float() handles 'e' correctly, but if it's '90.5e' it raises ValueError.
                val = float(val_str)
            except ValueError:
                continue

            if qid not in stats:
                stats[qid] = {"count": 0.0, "mean": 0.0, "m2": 0.0}

            s = stats[qid]
            s["count"] += 1.0
            delta = val - s["mean"]
            s["mean"] += delta / s["count"]
            delta2 = val - s["mean"]
            s["m2"] += delta * delta2

    return stats

def test_corrected_queries_csv_exists():
    csv_path = "/home/user/corrected_queries.csv"
    assert os.path.isfile(csv_path), f"Expected output file not found at {csv_path}. Did the service run successfully?"

def test_corrected_queries_csv_content():
    csv_path = "/home/user/corrected_queries.csv"
    log_path = "/home/user/data/metrics.log"

    assert os.path.isfile(csv_path), "CSV file is missing."
    assert os.path.isfile(log_path), "Metrics log file is missing."

    expected_stats = compute_expected_stats(log_path)

    actual_stats = {}
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["query_id", "count", "mean", "variance"], \
            f"CSV header is incorrect. Expected ['query_id', 'count', 'mean', 'variance'], got {header}"

        for row in reader:
            if not row:
                continue
            assert len(row) == 4, f"Invalid CSV row length: {row}"
            qid, count_str, mean_str, var_str = row
            actual_stats[qid] = {
                "count": float(count_str),
                "mean": float(mean_str),
                "variance": float(var_str)
            }

    # Verify that all expected queries are present and no extra queries are in the output
    expected_qids = set(expected_stats.keys())
    actual_qids = set(actual_stats.keys())

    assert expected_qids == actual_qids, \
        f"Mismatch in query IDs in CSV. Expected {expected_qids}, but got {actual_qids}. " \
        "Ensure malformed rows are skipped and valid rows are processed."

    for qid in expected_qids:
        e_stat = expected_stats[qid]
        a_stat = actual_stats[qid]

        e_count = e_stat["count"]
        e_mean = e_stat["mean"]

        if e_count <= 1.0:
            e_var = 0.0
        else:
            e_var = e_stat["m2"] / (e_count - 1.0)

        # The Rust code outputs mean and variance with {:.2}
        expected_mean_rounded = round(e_mean, 2)
        expected_var_rounded = round(e_var, 2)

        assert math.isclose(a_stat["count"], e_count, rel_tol=1e-5), \
            f"Count mismatch for {qid}. Expected {e_count}, got {a_stat['count']}"

        assert math.isclose(a_stat["mean"], expected_mean_rounded, rel_tol=1e-2), \
            f"Mean mismatch for {qid}. Expected ~{expected_mean_rounded}, got {a_stat['mean']}"

        assert not math.isnan(a_stat["variance"]), \
            f"Variance for {qid} is NaN. Ensure division by zero is prevented."

        assert math.isclose(a_stat["variance"], expected_var_rounded, rel_tol=1e-2), \
            f"Variance mismatch for {qid}. Expected ~{expected_var_rounded}, got {a_stat['variance']}"