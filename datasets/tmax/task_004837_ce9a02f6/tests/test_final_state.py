# test_final_state.py
import os
import csv
import math
import pytest

def test_similar_customers_output():
    csv_path = '/home/user/customers.csv'
    output_path = '/home/user/similar_customers.txt'

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.exists(csv_path), f"Input file {csv_path} does not exist."

    valid_rows = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                id_val = int(row['id'])
                age_val = int(row['age'])
                income_val = float(row['income'])
                score_val = float(row['spending_score'])

                if age_val > 0 and income_val >= 0 and 0 <= score_val <= 100:
                    valid_rows.append({
                        'id': id_val,
                        'age': age_val,
                        'income': income_val,
                        'score': score_val
                    })
            except (ValueError, TypeError, KeyError):
                continue

    assert len(valid_rows) > 0, "No valid rows found in the CSV."

    min_age = min(r['age'] for r in valid_rows)
    max_age = max(r['age'] for r in valid_rows)
    min_inc = min(r['income'] for r in valid_rows)
    max_inc = max(r['income'] for r in valid_rows)
    min_score = min(r['score'] for r in valid_rows)
    max_score = max(r['score'] for r in valid_rows)

    target = {'age': 35, 'income': 75000, 'score': 50}

    def normalize(val, min_v, max_v):
        if max_v == min_v:
            return 0.0
        return (val - min_v) / (max_v - min_v)

    target_norm = (
        normalize(target['age'], min_age, max_age),
        normalize(target['income'], min_inc, max_inc),
        normalize(target['score'], min_score, max_score)
    )

    distances = []
    for r in valid_rows:
        r_norm = (
            normalize(r['age'], min_age, max_age),
            normalize(r['income'], min_inc, max_inc),
            normalize(r['score'], min_score, max_score)
        )
        dist = math.sqrt(
            (r_norm[0] - target_norm[0])**2 +
            (r_norm[1] - target_norm[1])**2 +
            (r_norm[2] - target_norm[2])**2
        )
        distances.append((dist, r['id']))

    distances.sort(key=lambda x: x[0])
    expected_ids = [str(d[1]) for d in distances[:3]]
    expected_output = ",".join(expected_ids)

    with open(output_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Output file content is incorrect.\n"
        f"Expected: {expected_output}\n"
        f"Got: {actual_output}"
    )