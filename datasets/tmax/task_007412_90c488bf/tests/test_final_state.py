# test_final_state.py
import json
import math
import os
import pytest

def test_regression_report():
    report_path = "/home/user/regression_report.json"
    assert os.path.exists(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert isinstance(data, list), "JSON root must be an array."

    seqs = [
        ("seq1", "ATGCGTAACGTACGTAGCTAGCTAGCATCGATCGATCGATCGA"),
        ("seq2", "GGGGCCCCGGGGCCCCGGGGCCCC"),
        ("seq3", "ATATATATATATATATATATATATATATATAT")
    ]

    assert len(data) == len(seqs), f"Expected {len(seqs)} records in the JSON array, found {len(data)}."

    for i, (sid, seq) in enumerate(seqs):
        record = data[i]

        expected_keys = {"seq_id", "analytical_M50", "numerical_M50", "numerical_derivative_M50", "passed_regression"}
        assert set(record.keys()) == expected_keys, f"Record {i} keys {set(record.keys())} do not match expected {expected_keys}."

        assert record["seq_id"] == sid, f"Expected seq_id '{sid}', got '{record['seq_id']}'."

        # Calculate expected values
        L = len(seq)
        gc_count = seq.count('G') + seq.count('C')
        gc_frac = gc_count / L
        alpha = 1000.0 / L
        gamma = 0.05 + 2.0 * abs(gc_frac - 0.5)

        ana_M50 = (alpha / gamma) * (1 - math.exp(-gamma * 50))

        # Euler integration
        dt = 0.1
        M = 0.0
        for _ in range(500):
            M += (alpha - gamma * M) * dt

        num_M50 = M

        # Backward difference derivative
        M_prev = 0.0
        for _ in range(499):
            M_prev += (alpha - gamma * M_prev) * dt

        num_deriv = (num_M50 - M_prev) / dt

        passed = abs(ana_M50 - num_M50) < 1.0

        # Assertions
        assert math.isclose(record["analytical_M50"], ana_M50, rel_tol=1e-3, abs_tol=1e-3), \
            f"Record '{sid}' analytical_M50 expected ~{ana_M50}, got {record['analytical_M50']}"

        assert math.isclose(record["numerical_M50"], num_M50, rel_tol=1e-3, abs_tol=1e-3), \
            f"Record '{sid}' numerical_M50 expected ~{num_M50}, got {record['numerical_M50']}"

        assert math.isclose(record["numerical_derivative_M50"], num_deriv, rel_tol=1e-3, abs_tol=1e-3), \
            f"Record '{sid}' numerical_derivative_M50 expected ~{num_deriv}, got {record['numerical_derivative_M50']}"

        assert record["passed_regression"] == passed, \
            f"Record '{sid}' passed_regression expected {passed}, got {record['passed_regression']}"