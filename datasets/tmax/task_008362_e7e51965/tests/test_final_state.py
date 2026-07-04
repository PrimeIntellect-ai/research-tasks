# test_final_state.py
import os
import math
from decimal import Decimal, ROUND_HALF_UP

def test_results_file_exists_and_correct():
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"Expected output file {results_path} does not exist."

    # Read the data to compute truth
    users_path = "/home/user/users.csv"
    impressions_path = "/home/user/impressions.csv"
    clicks_path = "/home/user/clicks.csv"

    assert os.path.isfile(users_path), f"Missing {users_path}"
    assert os.path.isfile(impressions_path), f"Missing {impressions_path}"
    assert os.path.isfile(clicks_path), f"Missing {clicks_path}"

    us_users = set()
    with open(users_path, 'r') as f:
        header = f.readline()
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2 and parts[1] == 'US':
                us_users.add(parts[0])

    impressions = {}
    with open(impressions_path, 'r') as f:
        header = f.readline()
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2 and parts[0] in us_users:
                impressions[parts[0]] = parts[1]

    clicks = set()
    with open(clicks_path, 'r') as f:
        header = f.readline()
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 1:
                clicks.add(parts[0])

    n_a = 0
    c_a = 0
    n_b = 0
    c_b = 0

    for uid, variant in impressions.items():
        if variant == 'A':
            n_a += 1
            if uid in clicks:
                c_a += 1
        elif variant == 'B':
            n_b += 1
            if uid in clicks:
                c_b += 1

    p_a = c_a / n_a if n_a > 0 else 0
    p_b = c_b / n_b if n_b > 0 else 0
    diff = p_a - p_b
    se = math.sqrt((p_a * (1 - p_a) / n_a) + (p_b * (1 - p_b) / n_b)) if n_a > 0 and n_b > 0 else 0
    ci_lower = diff - 1.96 * se
    ci_upper = diff + 1.96 * se

    def round_4(val):
        return Decimal(str(val)).quantize(Decimal('0.0000'), rounding=ROUND_HALF_UP)

    expected = {
        "N_A": str(n_a),
        "C_A": str(c_a),
        "P_A": f"{round_4(p_a):.4f}",
        "N_B": str(n_b),
        "C_B": str(c_b),
        "P_B": f"{round_4(p_b):.4f}",
        "Diff": f"{round_4(diff):.4f}",
        "SE": f"{round_4(se):.4f}",
        "CI_Lower": f"{round_4(ci_lower):.4f}",
        "CI_Upper": f"{round_4(ci_upper):.4f}",
    }

    # Read actual results
    actual = {}
    with open(results_path, 'r') as f:
        for line in f:
            if ':' in line:
                key, val = line.strip().split(':', 1)
                actual[key.strip()] = val.strip()

    for key, expected_val in expected.items():
        assert key in actual, f"Missing key '{key}' in {results_path}"
        # Allow small floating point differences due to bash 'bc' rounding vs python
        if key not in ["N_A", "C_A", "N_B", "C_B"]:
            actual_val = actual[key]
            # Try to convert both to float and check if they are very close
            try:
                actual_float = float(actual_val)
                expected_float = float(expected_val)
                assert abs(actual_float - expected_float) <= 0.0002, \
                    f"Value for {key} is {actual_val}, expected {expected_val} (allowable diff 0.0002)"
            except ValueError:
                assert actual[key] == expected_val, f"Value for {key} is '{actual[key]}', expected '{expected_val}'"
        else:
            assert actual[key] == expected_val, f"Value for {key} is '{actual[key]}', expected '{expected_val}'"