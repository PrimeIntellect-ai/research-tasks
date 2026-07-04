# test_final_state.py
import os
import json

def test_heatmap_exists():
    """Test that the heatmap.png was successfully generated and is a valid PNG."""
    path = "/home/user/heatmap.png"
    assert os.path.isfile(path), f"File {path} is missing. The script failed to generate the heatmap."

    with open(path, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", f"File {path} is not a valid PNG image."

def test_top_pairs_json_structure_and_content():
    """Test that top_pairs.json is correctly formatted, has no duplicates/self-similarity, and contains the expected pairs."""
    path = "/home/user/top_pairs.json"
    assert os.path.isfile(path), f"File {path} is missing. The script failed to save the JSON output."

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"File {path} does not contain valid JSON."

    assert isinstance(data, list), "The JSON root should be a list."
    assert len(data) == 3, f"Expected exactly 3 pairs in the JSON, but found {len(data)}."

    seen_pairs = set()
    for idx, item in enumerate(data):
        assert isinstance(item, list) and len(item) == 3, f"Item at index {idx} is not in the format [Movie 1, Movie 2, Similarity]."
        m1, m2, sim = item

        assert isinstance(m1, str), f"Movie 1 at index {idx} should be a string."
        assert isinstance(m2, str), f"Movie 2 at index {idx} should be a string."
        assert isinstance(sim, (int, float)), f"Similarity score at index {idx} should be a number."

        assert m1 != m2, f"Self-similarity detected: '{m1}' is paired with itself. The script should exclude self-similarity."

        # Normalize pair to check for duplicates like [A, B] and [B, A]
        pair_tuple = tuple(sorted([m1, m2]))
        assert pair_tuple not in seen_pairs, f"Duplicate pair detected: {m1} and {m2} were already included."
        seen_pairs.add(pair_tuple)

    # Check the actual top pairs based on expected TF-IDF cosine similarities
    # Inception and Dreamscape should be the most similar
    pair1 = tuple(sorted([data[0][0], data[0][1]]))
    expected_pair1 = tuple(sorted(["Inception", "Dreamscape"]))
    assert pair1 == expected_pair1, f"Expected the most similar pair to be {expected_pair1}, but got {pair1}."

    # The Matrix and The Net should be the second most similar
    pair2 = tuple(sorted([data[1][0], data[1][1]]))
    expected_pair2 = tuple(sorted(["The Matrix", "The Net"]))
    assert pair2 == expected_pair2, f"Expected the second most similar pair to be {expected_pair2}, but got {pair2}."

    # The third pair should have a similarity of 0.0
    sim3 = data[2][2]
    assert abs(sim3) < 0.01, f"Expected the third pair to have a similarity of ~0.0, but got {sim3}."