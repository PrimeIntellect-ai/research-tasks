# test_final_state.py

import os
import json
import csv
import math

def get_expected_values():
    csv_path = '/home/user/nanopore_signal.csv'
    if not os.path.exists(csv_path):
        return None

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        currents = [float(row['current']) for row in reader]

    if len(currents) < 10:
        return None

    # 1. Rolling mean of window 10
    smoothed = []
    # To match pandas rolling(10).mean().dropna(), the first value is at index 9
    # which is the average of indices 0 to 9.
    window_sum = sum(currents[:10])
    smoothed.append(window_sum / 10.0)

    for i in range(10, len(currents)):
        window_sum += currents[i] - currents[i-10]
        smoothed.append(window_sum / 10.0)

    # 2. Thresholding
    is_blocked = [s < 75.0 for s in smoothed]

    # 3. Dwell time extraction
    lengths = []
    current_len = 0
    for b in is_blocked:
        if b:
            current_len += 1
        else:
            if current_len > 0:
                lengths.append(current_len)
                current_len = 0
    if current_len > 0:
        lengths.append(current_len)

    dwell_times = [l * 0.1 for l in lengths]

    if not dwell_times:
        return None

    # 4. Mean and Analytical CI
    N = len(dwell_times)
    mean_dwell = sum(dwell_times) / N
    se = mean_dwell / math.sqrt(N)
    ana_lower = mean_dwell - 1.96 * se
    ana_upper = mean_dwell + 1.96 * se

    return {
        "mean_dwell_time": round(mean_dwell, 4),
        "analytical_ci_lower": round(ana_lower, 4),
        "analytical_ci_upper": round(ana_upper, 4),
        "event_count": N
    }

def test_results_json_exists_and_format():
    results_path = '/home/user/results.json'
    assert os.path.isfile(results_path), f"File not found: {results_path}"

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_path} is not a valid JSON."

    expected_keys = {
        "mean_dwell_time",
        "bootstrap_ci_lower",
        "bootstrap_ci_upper",
        "analytical_ci_lower",
        "analytical_ci_upper",
        "event_count"
    }

    assert set(data.keys()) == expected_keys, f"JSON keys do not match expected. Found: {list(data.keys())}"
    assert isinstance(data["event_count"], int), "event_count must be an integer."

    for k in expected_keys:
        if k != "event_count":
            assert isinstance(data[k], (float, int)), f"{k} must be a float."

def test_results_values_correct():
    results_path = '/home/user/results.json'
    assert os.path.isfile(results_path), f"File not found: {results_path}"

    with open(results_path, 'r') as f:
        data = json.load(f)

    expected = get_expected_values()
    assert expected is not None, "Could not compute expected values from the dataset."

    assert data["event_count"] == expected["event_count"], \
        f"Expected event_count {expected['event_count']}, got {data['event_count']}"

    assert data["mean_dwell_time"] == expected["mean_dwell_time"], \
        f"Expected mean_dwell_time {expected['mean_dwell_time']}, got {data['mean_dwell_time']}"

    assert data["analytical_ci_lower"] == expected["analytical_ci_lower"], \
        f"Expected analytical_ci_lower {expected['analytical_ci_lower']}, got {data['analytical_ci_lower']}"

    assert data["analytical_ci_upper"] == expected["analytical_ci_upper"], \
        f"Expected analytical_ci_upper {expected['analytical_ci_upper']}, got {data['analytical_ci_upper']}"

    # For bootstrap CI, since we cannot easily replicate numpy's PRNG exact sequence in stdlib,
    # we assert that the bootstrap bounds are reasonably close to the analytical bounds.
    # The prompt requires values rounded to 4 decimal places, so we check they are floats and near the analytical CI.
    assert abs(data["bootstrap_ci_lower"] - expected["analytical_ci_lower"]) < 0.5, \
        f"bootstrap_ci_lower {data['bootstrap_ci_lower']} is too far from expected analytical {expected['analytical_ci_lower']}"

    assert abs(data["bootstrap_ci_upper"] - expected["analytical_ci_upper"]) < 0.5, \
        f"bootstrap_ci_upper {data['bootstrap_ci_upper']} is too far from expected analytical {expected['analytical_ci_upper']}"