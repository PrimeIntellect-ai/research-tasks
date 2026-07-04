# test_final_state.py
import os

def test_jaccard_similarity_active_config():
    csv_path = "/home/user/active_config.csv"
    assert os.path.exists(csv_path), f"Output file not found: {csv_path}"

    expected = {"10.5.5.1,22", "10.5.5.1,8080", "192.168.1.200,3306"}

    actual = set()
    with open(csv_path, 'r') as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                actual.add(stripped)

    assert len(actual) > 0, "The output file is empty."

    intersection = len(expected.intersection(actual))
    union = len(expected.union(actual))
    jaccard = intersection / union if union > 0 else 0.0

    assert jaccard >= 0.90, f"Jaccard similarity is {jaccard:.4f}, but expected >= 0.90. Expected rules: {expected}, Actual rules: {actual}"