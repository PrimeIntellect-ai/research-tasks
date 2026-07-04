# test_final_state.py

import os
import csv
import pytest

def get_events_data():
    events = []
    with open('/home/user/events.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append({
                'id': int(row['id']),
                'category': row['category'],
                'value': int(row['value']),
                'label': int(row['label'])
            })
    return events

def get_bootstrap_indices():
    indices_list = []
    with open('/home/user/bootstrap_indices.txt', 'r') as f:
        for line in f:
            indices = [int(x) for x in line.strip().split(',')]
            indices_list.append(indices)
    return indices_list

def compute_phase1_truth(events):
    sums = {}
    counts = {}
    for ev in events:
        c = ev['category']
        sums[c] = sums.get(c, 0) + ev['value']
        counts[c] = counts.get(c, 0) + 1

    results = []
    for c in sorted(sums.keys()):
        avg = sums[c] / counts[c]
        results.append(f"{c},{avg:.2f}")

    return "category,average_value\n" + "\n".join(results) + "\n"

def compute_phase2_truth(events, indices_list):
    # events is 1-indexed, so events[idx-1] gets the right row
    means = []
    for indices in indices_list:
        total = sum(events[idx - 1]['value'] for idx in indices)
        mean_val = total / len(indices)
        means.append(round(mean_val, 2))

    means.sort()
    p5 = means[4]
    p95 = means[94]
    return f"{p5:.2f},{p95:.2f}"

def compute_phase3_truth(events):
    folds = {i: [] for i in range(5)}
    for i, ev in enumerate(events):
        fold_idx = i % 5
        folds[fold_idx].append(ev)

    correct = 0
    total = len(events)

    for val_fold_idx in range(5):
        train_data = []
        val_data = folds[val_fold_idx]
        for i in range(5):
            if i != val_fold_idx:
                train_data.extend(folds[i])

        # Compute priors
        count_0 = sum(1 for ev in train_data if ev['label'] == 0)
        count_1 = sum(1 for ev in train_data if ev['label'] == 1)
        total_train = len(train_data)

        p_label_0 = count_0 / total_train if total_train > 0 else 0
        p_label_1 = count_1 / total_train if total_train > 0 else 0

        # Compute likelihoods
        cat_counts_0 = {}
        cat_counts_1 = {}
        for ev in train_data:
            c = ev['category']
            if ev['label'] == 0:
                cat_counts_0[c] = cat_counts_0.get(c, 0) + 1
            else:
                cat_counts_1[c] = cat_counts_1.get(c, 0) + 1

        for ev in val_data:
            c = ev['category']
            p_cat_given_0 = (cat_counts_0.get(c, 0) / count_0) if count_0 > 0 else 0
            p_cat_given_1 = (cat_counts_1.get(c, 0) / count_1) if count_1 > 0 else 0

            score_0 = p_label_0 * p_cat_given_0
            score_1 = p_label_1 * p_cat_given_1

            if score_1 >= score_0:
                pred = 1
            else:
                pred = 0

            if pred == ev['label']:
                correct += 1

    accuracy = correct / total
    return f"{accuracy:.4f}"

def test_phase1_aggregates():
    file_path = '/home/user/phase1_aggregates.csv'
    assert os.path.exists(file_path), f"File {file_path} is missing."

    events = get_events_data()
    expected_content = compute_phase1_truth(events)

    with open(file_path, 'r') as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), \
        f"Contents of {file_path} do not match expected.\nExpected:\n{expected_content.strip()}\nActual:\n{actual_content.strip()}"

def test_phase2_ci():
    file_path = '/home/user/phase2_ci.txt'
    assert os.path.exists(file_path), f"File {file_path} is missing."

    events = get_events_data()
    indices_list = get_bootstrap_indices()
    expected_content = compute_phase2_truth(events, indices_list)

    with open(file_path, 'r') as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), \
        f"Contents of {file_path} do not match expected.\nExpected: {expected_content.strip()}\nActual: {actual_content.strip()}"

def test_phase3_accuracy():
    file_path = '/home/user/phase3_accuracy.txt'
    assert os.path.exists(file_path), f"File {file_path} is missing."

    events = get_events_data()
    expected_content = compute_phase3_truth(events)

    with open(file_path, 'r') as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), \
        f"Contents of {file_path} do not match expected.\nExpected: {expected_content.strip()}\nActual: {actual_content.strip()}"