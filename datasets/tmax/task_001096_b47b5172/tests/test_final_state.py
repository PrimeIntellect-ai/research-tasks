# test_final_state.py
import os
import csv

def test_cleaned_data_exists():
    """Test that cleaned_data.csv was created."""
    assert os.path.exists('/home/user/cleaned_data.csv'), "cleaned_data.csv is missing"

def test_top_pairs_exists():
    """Test that top_pairs.csv was created."""
    assert os.path.exists('/home/user/top_pairs.csv'), "top_pairs.csv is missing"

def test_top_pairs_content():
    """Test the content, format, and correctness of top_pairs.csv."""
    file_path = '/home/user/top_pairs.csv'

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, "top_pairs.csv is empty"

        assert header == ['id1', 'id2', 'similarity'], f"Incorrect columns in top_pairs.csv: {header}"

        rows = list(reader)
        assert len(rows) == 3, f"Should contain exactly 3 pairs, found {len(rows)}"

        parsed_rows = []
        for row in rows:
            assert len(row) == 3, f"Row does not have exactly 3 columns: {row}"
            try:
                id1 = int(row[0])
                id2 = int(row[1])
                sim = float(row[2])
            except ValueError as e:
                assert False, f"Error parsing row values {row}: {e}"
            parsed_rows.append((id1, id2, sim))

        actual_scores = [r[2] for r in parsed_rows]
        expected_top_scores = [0.9129, 0.9129, 0.7500]

        for exp, act in zip(expected_top_scores, actual_scores):
            assert abs(exp - act) < 0.0002, f"Expected similarity close to {exp}, got {act}"

        top_pairs_set = {(r[0], r[1]) for r in parsed_rows}
        assert (4, 5) in top_pairs_set, "Pair (4, 5) is missing from the top pairs."
        assert (8, 9) in top_pairs_set, "Pair (8, 9) is missing from the top pairs."
        assert (1, 2) in top_pairs_set or (1, 10) in top_pairs_set, "A 0.7500 pair (either 1,2 or 1,10) is missing."