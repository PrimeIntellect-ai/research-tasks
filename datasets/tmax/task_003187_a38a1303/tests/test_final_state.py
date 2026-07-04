# test_final_state.py
import csv
import math
import requests
import pytest
from collections import defaultdict

def compute_ground_truth():
    data = defaultdict(list)
    with open('/app/sensor_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensor = row['sensor_id']
            val = float(row['value'])
            data[sensor].append(val)

    stats = {}
    for sensor, values in data.items():
        n = len(values)
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / n
        stddev = math.sqrt(variance)

        anomalies = sum(1 for x in values if x > mean + 3 * stddev or x < mean - 3 * stddev)
        flagged = anomalies > 5

        stats[sensor] = {
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "mean": round(mean, 2),
            "anomalies": anomalies,
            "flagged": flagged
        }

    target_sensor = "S07"
    target_values = data[target_sensor]

    min_dist = float('inf')
    most_similar = None

    for sensor, values in data.items():
        if sensor == target_sensor:
            continue
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(target_values, values)))
        if dist < min_dist:
            min_dist = dist
            most_similar = sensor

    return stats, target_sensor, most_similar, round(min_dist, 2)

@pytest.fixture(scope="module")
def ground_truth():
    return compute_ground_truth()

def test_stats_s02(ground_truth):
    stats, _, _, _ = ground_truth
    expected = stats["S02"]

    try:
        resp = requests.get("http://127.0.0.1:9090/stats?sensor_id=S02", timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        pytest.fail(f"Failed to get stats for S02: {e}")

    assert data.get("anomalies") == expected["anomalies"], f"Expected {expected['anomalies']} anomalies for S02, got {data.get('anomalies')}"
    assert data.get("flagged") is True, f"Expected S02 to be flagged, got {data.get('flagged')}"
    assert math.isclose(data.get("mean"), expected["mean"], abs_tol=0.02), f"Expected mean {expected['mean']}, got {data.get('mean')}"

def test_stats_s01(ground_truth):
    stats, _, _, _ = ground_truth
    expected = stats["S01"]

    try:
        resp = requests.get("http://127.0.0.1:9090/stats?sensor_id=S01", timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        pytest.fail(f"Failed to get stats for S01: {e}")

    assert data.get("flagged") is False, f"Expected S01 to not be flagged, got {data.get('flagged')}"

def test_similar(ground_truth):
    _, target, most_similar, dist = ground_truth

    try:
        resp = requests.get("http://127.0.0.1:9090/similar", timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        pytest.fail(f"Failed to get similar sensor: {e}")

    assert data.get("target") == target, f"Expected target {target}, got {data.get('target')}"
    assert data.get("most_similar") == most_similar, f"Expected most_similar {most_similar}, got {data.get('most_similar')}"
    assert math.isclose(data.get("distance"), dist, abs_tol=0.02), f"Expected distance {dist}, got {data.get('distance')}"