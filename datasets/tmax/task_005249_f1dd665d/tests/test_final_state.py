# test_final_state.py
import os
import json
import csv

def compute_expected_results(dataset_path):
    rows = []
    f1_sum = 0.0
    f1_count = 0
    with open(dataset_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            f1_str = row['f1'].strip()
            if f1_str != "NA":
                f1_val = float(f1_str)
                f1_sum += f1_val
                f1_count += 1
            rows.append(row)

    f1_mean = f1_sum / f1_count if f1_count > 0 else 0.0

    cleaned_rows = []
    for row in rows:
        f1_str = row['f1'].strip()
        f1_val = float(f1_str) if f1_str != "NA" else f1_mean

        text = row['text'].strip()
        # count space-separated words
        f2_val = len([w for w in text.split(' ') if w]) if text else 0

        if f2_val > 20:
            continue

        label = int(row['label'])
        cleaned_rows.append((f1_val, f2_val, label))

    fold_A = [cleaned_rows[i] for i in range(len(cleaned_rows)) if i % 2 == 0]
    fold_B = [cleaned_rows[i] for i in range(len(cleaned_rows)) if i % 2 != 0]

    best_w1 = -999
    best_w2 = -999
    best_cv = -1.0

    for w1 in range(-10, 11):
        for w2 in range(-10, 11):
            accA = 0
            for f1, f2, label in fold_A:
                pred = 1 if (w1 * f1 + w2 * f2 > 0) else 0
                if pred == label:
                    accA += 1
            accA = accA / len(fold_A) if fold_A else 0.0

            accB = 0
            for f1, f2, label in fold_B:
                pred = 1 if (w1 * f1 + w2 * f2 > 0) else 0
                if pred == label:
                    accB += 1
            accB = accB / len(fold_B) if fold_B else 0.0

            cv_score = (accA + accB) / 2.0

            if cv_score > best_cv:
                best_cv = cv_score
                best_w1 = w1
                best_w2 = w2
            elif abs(cv_score - best_cv) < 1e-9:
                if w1 > best_w1:
                    best_w1 = w1
                    best_w2 = w2
                elif w1 == best_w1:
                    if w2 > best_w2:
                        best_w2 = w2

    return best_w1, best_w2, best_cv

def test_artifact_exists_and_valid():
    artifact_path = '/home/user/artifact.json'
    assert os.path.exists(artifact_path), f"The artifact file {artifact_path} is missing."
    assert os.path.isfile(artifact_path), f"{artifact_path} is not a file."

    with open(artifact_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{artifact_path} is not a valid JSON file."

    assert 'best_w1' in data, "Missing 'best_w1' in artifact.json"
    assert 'best_w2' in data, "Missing 'best_w2' in artifact.json"
    assert 'cv_score' in data, "Missing 'cv_score' in artifact.json"

    # Check format of cv_score (must be formatted to exactly 4 decimal places in JSON string or as a float)
    # The spec says "Format SCORE to exactly 4 decimal places."
    # If it's a string, we check the length after the decimal point. If it's a float, we just check the value.
    if isinstance(data['cv_score'], str):
        parts = data['cv_score'].split('.')
        assert len(parts) == 2 and len(parts[1]) == 4, "SCORE is not formatted to exactly 4 decimal places."

def test_experiment_results():
    dataset_path = '/home/user/dataset.csv'
    artifact_path = '/home/user/artifact.json'

    expected_w1, expected_w2, expected_cv = compute_expected_results(dataset_path)

    with open(artifact_path, 'r') as f:
        data = json.load(f)

    actual_w1 = int(data['best_w1'])
    actual_w2 = int(data['best_w2'])
    actual_cv = float(data['cv_score'])

    assert actual_w1 == expected_w1, f"Expected best_w1 to be {expected_w1}, but got {actual_w1}."
    assert actual_w2 == expected_w2, f"Expected best_w2 to be {expected_w2}, but got {actual_w2}."
    assert abs(actual_cv - expected_cv) < 1e-4, f"Expected cv_score to be {expected_cv:.4f}, but got {actual_cv:.4f}."