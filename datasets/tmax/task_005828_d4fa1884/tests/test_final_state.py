# test_final_state.py

import os
import csv
import pytest

def test_matched_items_exists():
    path = "/home/user/matched_items.csv"
    assert os.path.exists(path), f"Output file {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_matched_items_contents():
    path = "/home/user/matched_items.csv"
    assert os.path.exists(path), f"Output file {path} does not exist."

    expected = {
        "A01": ("B05", "1.0000"),
        "A02": ("B02", "0.9939"),
        "A03": ("B01", "0.9822"),
        "A04": ("B04", "0.9902"),
        "A05": ("B03", "0.9939"),
    }

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"File {path} is empty.")

        assert header == ["item_id_alpha", "item_id_beta", "similarity"], \
            f"Incorrect headers in {path}: expected ['item_id_alpha', 'item_id_beta', 'similarity'], got {header}"

        rows = list(reader)
        assert len(rows) == 5, f"Incorrect number of rows: expected 5, got {len(rows)}"

        seen_alphas = set()
        for row in rows:
            assert len(row) == 3, f"Row does not have 3 columns: {row}"
            alpha, beta, sim = row

            assert alpha in expected, f"Unexpected item_id_alpha: {alpha}"
            seen_alphas.add(alpha)

            expected_beta, expected_sim = expected[alpha]
            assert beta == expected_beta, f"Mismatch for {alpha}: expected {expected_beta}, got {beta}"

            # Allow for potential formatting differences like 1.0 vs 1.0000 by parsing as float then formatting
            try:
                sim_float = float(sim)
            except ValueError:
                pytest.fail(f"Similarity value for {alpha} is not a valid float: '{sim}'")

            formatted_sim = f"{sim_float:.4f}"
            assert formatted_sim == expected_sim, f"Similarity mismatch for {alpha}: expected {expected_sim}, got {formatted_sim}"

        assert seen_alphas == set(expected.keys()), f"Missing item_id_alpha rows: {set(expected.keys()) - seen_alphas}"