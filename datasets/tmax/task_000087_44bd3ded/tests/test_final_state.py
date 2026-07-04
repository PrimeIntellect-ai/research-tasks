# test_final_state.py

import os
import json
import pytest

def test_curated_metadata_f1_score():
    """
    Test that the curated_metadata.json file exists, contains the correct format,
    and the F1 score of the extracted valid metadata is >= 0.95 compared to the golden set.
    """
    output_file = '/home/user/curated_metadata.json'

    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"Path {output_file} is not a file."

    try:
        with open(output_file, 'r') as f:
            predicted = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to load JSON from {output_file}: {e}")

    assert isinstance(predicted, list), f"Expected a JSON array, got {type(predicted).__name__}"

    # Ground truth data
    golden = [
        {"Artifact-ID": "bin-001", "Checksum": "1111", "Status": "VALID"},
        {"Artifact-ID": "bin-003", "Checksum": "3333", "Status": "VALID"}
    ]

    pred_set = set(f"{d.get('Artifact-ID')}_{d.get('Checksum')}" for d in predicted if d.get('Status') == 'VALID')
    gold_set = set(f"{d['Artifact-ID']}_{d['Checksum']}" for d in golden)

    if not pred_set and not gold_set:
        f1 = 1.0
    elif not pred_set or not gold_set:
        f1 = 0.0
    else:
        tp = len(pred_set & gold_set)
        fp = len(pred_set - gold_set)
        fn = len(gold_set - pred_set)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0

        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 score {f1:.4f} is below the threshold of 0.95. Precision: {precision:.4f}, Recall: {recall:.4f}"