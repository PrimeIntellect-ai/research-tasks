# test_final_state.py
import os
import json

def test_duplicates_json_exists_and_correct():
    out_path = "/home/user/duplicates.json"
    assert os.path.exists(out_path), f"Output file missing at {out_path}"

    with open(out_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {out_path} is not valid JSON"

    assert isinstance(results, list), f"Expected a JSON array, got {type(results)}"

    # The expected probability for S >= 0.7
    expected_prob = round((0.85 * 0.05) / (0.85 * 0.05 + 0.02 * 0.95), 4)

    # Based on the dataset texts, the duplicate pairs with S >= 0.7 are:
    # Test 5 -> Train 1 (exact match)
    # Test 6 -> Train 2 (highly similar)
    # Test 9 -> Train 4 (exact match)
    expected_pairs = [(5, 1), (6, 2), (9, 4)]

    assert len(results) == len(expected_pairs), f"Expected {len(expected_pairs)} duplicate pairs, got {len(results)}"

    for i, res in enumerate(results):
        assert "test_id" in res, f"Missing 'test_id' in result {i}"
        assert "train_id" in res, f"Missing 'train_id' in result {i}"
        assert "prob" in res, f"Missing 'prob' in result {i}"

        assert res["prob"] == expected_prob, f"Expected prob {expected_prob} for pair, got {res['prob']}"

    actual_pairs = [(res["test_id"], res["train_id"]) for res in results]

    # Check sorting: descending by prob, then test_id asc, then train_id asc
    # Since prob is identical for all kept pairs, it should be sorted by test_id asc, train_id asc
    expected_sorted_pairs = sorted(expected_pairs)
    assert actual_pairs == expected_sorted_pairs, f"Expected pairs {expected_sorted_pairs} (properly sorted), got {actual_pairs}"