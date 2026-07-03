# test_final_state.py

import os
import csv
import math
import pytest

def read_csv(path):
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_predictions_csv_exists():
    path = "/home/user/predictions.csv"
    assert os.path.isfile(path), f"Expected output file {path} is missing."

def test_predictions_logic_and_output():
    # Read input files
    features_path = "/home/user/features.csv"
    labels_path = "/home/user/labels.csv"
    test_ids_path = "/home/user/test_ids.txt"

    assert os.path.isfile(features_path), f"Missing {features_path}"
    assert os.path.isfile(labels_path), f"Missing {labels_path}"
    assert os.path.isfile(test_ids_path), f"Missing {test_ids_path}"

    features = read_csv(features_path)
    labels = read_csv(labels_path)
    with open(test_ids_path, 'r') as f:
        test_ids = {int(line.strip()) for line in f if line.strip()}

    labels_dict = {int(row['user_id']): int(row['label']) for row in labels}

    # 1. Multi-source joining
    data = []
    for row in features:
        uid = int(row['user_id'])
        if uid in labels_dict:
            data.append({
                'user_id': uid,
                'f1': float(row['f1']),
                'f2': float(row['f2']),
                'f3': float(row['f3']),
                'label': labels_dict[uid]
            })

    # 2. Train/Test Split
    train_data = [d for d in data if d['user_id'] not in test_ids]
    test_data = [d for d in data if d['user_id'] in test_ids]

    # 3. Data Normalization (strictly using training set, sample std)
    stats = {}
    n = len(train_data)
    assert n > 1, "Not enough training data to compute sample standard deviation."

    for f in ['f1', 'f2', 'f3']:
        mean = sum(d[f] for d in train_data) / n
        variance = sum((d[f] - mean) ** 2 for d in train_data) / (n - 1)
        std = math.sqrt(variance)
        stats[f] = {'mean': mean, 'std': std}

    for d in train_data + test_data:
        for f in ['f1', 'f2', 'f3']:
            d[f'{f}_norm'] = (d[f] - stats[f]['mean']) / stats[f]['std']

    # 4 & 5. Similarity Search and Prediction
    predictions = []
    for test_u in test_data:
        best_dist = float('inf')
        best_train_uid = float('inf')
        best_label = None
        for train_u in train_data:
            dist = math.sqrt(
                (test_u['f1_norm'] - train_u['f1_norm']) ** 2 +
                (test_u['f2_norm'] - train_u['f2_norm']) ** 2 +
                (test_u['f3_norm'] - train_u['f3_norm']) ** 2
            )
            # Tie breaking by lowest user_id
            if dist < best_dist or (dist == best_dist and train_u['user_id'] < best_train_uid):
                best_dist = dist
                best_train_uid = train_u['user_id']
                best_label = train_u['label']
        predictions.append((test_u['user_id'], best_label))

    # 6. Output sorted by user_id
    predictions.sort(key=lambda x: x[0])
    expected_csv = "user_id,predicted_label\n" + "\n".join(f"{u},{l}" for u, l in predictions) + "\n"

    # Verify agent's work
    predictions_path = "/home/user/predictions.csv"
    with open(predictions_path, 'r') as f:
        actual_csv = f.read().strip() + "\n"

    actual_csv = actual_csv.replace('\r\n', '\n')

    assert actual_csv == expected_csv, (
        f"Predictions in {predictions_path} do not match the expected output.\n"
        f"Expected:\n{expected_csv}\nGot:\n{actual_csv}"
    )