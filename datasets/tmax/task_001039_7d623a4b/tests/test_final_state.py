# test_final_state.py

import os
import csv

def test_predictions_file_exists():
    path = '/home/user/predictions.csv'
    assert os.path.exists(path), f"File {path} does not exist. The task requires creating this file."

def test_predictions_format_and_matches():
    path = '/home/user/predictions.csv'
    if not os.path.exists(path):
        return # Handled by previous test

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, f"File {path} is empty."

        expected_header = ['id_A', 'matched_id_B', 'similarity_score', 'predicted_rating_A']
        assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

        rows = list(reader)
        assert len(rows) == 5, f"Expected exactly 5 rows of predictions, got {len(rows)}."

        # Check sorting by id_A
        ids = [row[0] for row in rows]
        assert ids == sorted(ids), "The output rows are not sorted alphabetically by id_A."

        # Expected matches based on the data descriptions
        expected_matches = {
            'A1': 'B1',
            'A2': 'B3',
            'A3': 'B2',
            'A4': 'B6',
            'A5': 'B5'
        }

        for row in rows:
            id_a, id_b, sim_score, pred_rating = row

            assert id_a in expected_matches, f"Unexpected id_A: {id_a}"
            assert id_b == expected_matches[id_a], f"For {id_a}, expected match {expected_matches[id_a]}, but got {id_b}."

            try:
                sim = float(sim_score)
                pred = float(pred_rating)
            except ValueError:
                assert False, f"similarity_score and predicted_rating_A must be numbers. Got {sim_score} and {pred_rating}."

            # Check 4 decimal places format
            assert len(sim_score.split('.')[-1]) <= 4, f"similarity_score {sim_score} is not rounded to 4 decimal places."
            assert len(pred_rating.split('.')[-1]) <= 4, f"predicted_rating_A {pred_rating} is not rounded to 4 decimal places."