# test_final_state.py

import os
import csv
import random
from datetime import datetime, timedelta
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for older python versions if needed
    import pytz

def test_alerts_f1_score():
    """
    Computes the F1 score of the generated alerts.csv against the expected ground truth.
    Threshold: F1 >= 0.95
    """
    random.seed(42)
    start_time = datetime(2023, 10, 1, 0, 0, 0)
    processes = ['worker_daemon', 'web_server', 'db_writer']
    expected_alerts = set()

    try:
        tz = ZoneInfo('Asia/Tokyo')
        utc_tz = ZoneInfo('UTC')
    except NameError:
        tz = pytz.timezone('Asia/Tokyo')
        utc_tz = pytz.utc

    # Reconstruct ground truth
    for i in range(5000):
        current_time = start_time + timedelta(minutes=i)
        proc = random.choice(processes)
        load = round(random.uniform(10.0, 99.9), 1)

        if proc == 'worker_daemon' and load > 82.5:
            # Convert UTC to Asia/Tokyo
            utc_dt = current_time.replace(tzinfo=utc_tz)
            tokyo_dt = utc_dt.astimezone(tz)
            expected_alerts.add(f"{tokyo_dt.strftime('%Y-%m-%d %H:%M:%S')},{proc},{load}")

    agent_alerts = set()
    alerts_path = '/home/user/alerts.csv'

    assert os.path.exists(alerts_path), f"Output file {alerts_path} does not exist. The supervisor failed to produce the alerts file."

    # Read agent alerts
    with open(alerts_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and len(row) >= 3:
                # Format exactly as expected to match sets
                agent_alerts.add(f"{row[0].strip()},{row[1].strip()},{row[2].strip()}")

    # Calculate F1
    true_positives = len(expected_alerts.intersection(agent_alerts))
    false_positives = len(agent_alerts - expected_alerts)
    false_negatives = len(expected_alerts - agent_alerts)

    if true_positives == 0:
        f1 = 0.0
    else:
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, (
        f"F1 Score {f1:.4f} is below threshold 0.95. "
        f"True Positives: {true_positives}, False Positives: {false_positives}, False Negatives: {false_negatives}."
    )