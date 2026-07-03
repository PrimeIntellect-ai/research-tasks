# test_final_state.py

import os
import subprocess
import pandas as pd
import numpy as np
import pytest

def test_datamash_perturbation_fixed():
    """Ensure the deliberate perturbation in datamash.c has been removed."""
    c_file = "/app/datamash-1.20/src/datamash.c"
    if os.path.exists(c_file):
        with open(c_file, "r") as f:
            content = f.read()
        assert '#error "Deliberate perturbation: remove this line"' not in content, \
            f"The deliberate perturbation is still present in {c_file}."

def test_detect_anomalies_f1_score(tmp_path):
    """Test the anomaly detection script against a generated dataset and evaluate F1 score."""
    script_path = "/home/user/detect_anomalies.sh"
    assert os.path.exists(script_path), f"Script not found at {script_path}"

    csv_path = tmp_path / "hidden_test_logs.csv"

    # Generate hidden test data
    np.random.seed(42)
    start_time = 1680307200
    locales = ['es-ES', 'fr-FR', 'de-DE', 'en-US']
    string_ids = ['ui_button_login', 'ui_label_welcome', 'ui_menu_settings']

    records = []

    for h in range(50):
        for loc in locales:
            base_count = np.random.randint(10, 50)
            # Introduce anomalies
            if h >= 3 and np.random.rand() < 0.1:
                base_count = base_count * 3 + 20

            for _ in range(base_count):
                ts = start_time + h * 3600 + np.random.randint(0, 3600)
                sid = np.random.choice(string_ids)
                records.append({
                    'timestamp': ts,
                    'locale': loc,
                    'string_id': sid,
                    'access_count': np.random.randint(1, 5)
                })

    df = pd.DataFrame(records)
    # Shuffle to ensure the script doesn't rely on pre-sorted data
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv(csv_path, index=False)

    # Compute true anomalies based on the defined rules
    df['hour'] = np.floor(df['timestamp'] / 3600).astype(int)
    hourly = df.groupby(['hour', 'locale'])['access_count'].sum().reset_index()

    true_anomalies = set()
    for loc in locales:
        loc_data = hourly[hourly['locale'] == loc].sort_values('hour')
        for i in range(len(loc_data)):
            prev = loc_data['access_count'].iloc[max(0, i-3):i]
            r_avg = prev.mean() if len(prev) > 0 else 0.0
            row = loc_data.iloc[i]
            if row['access_count'] > 2.0 * r_avg + 10:
                true_anomalies.add((int(row['hour']), loc))

    # Run the student's script
    result = subprocess.run(
        ["bash", script_path, str(csv_path)],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    # Parse predicted anomalies
    predicted_anomalies = set()
    for line in result.stdout.strip().split('\n'):
        if not line: continue
        parts = line.split(',')
        if len(parts) >= 2:
            try:
                hour = int(parts[0])
                locale = parts[1]
                predicted_anomalies.add((hour, locale))
            except ValueError:
                pass

    # Calculate F1 Score
    tp = len(predicted_anomalies & true_anomalies)
    fp = len(predicted_anomalies - true_anomalies)
    fn = len(true_anomalies - predicted_anomalies)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.90, (
        f"F1 Score {f1:.4f} is less than the required threshold of 0.90. "
        f"True anomalies: {len(true_anomalies)}, Predicted: {len(predicted_anomalies)}, "
        f"TP: {tp}, FP: {fp}, FN: {fn}"
    )