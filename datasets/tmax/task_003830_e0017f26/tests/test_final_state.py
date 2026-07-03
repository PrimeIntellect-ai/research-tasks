# test_final_state.py
import os
import pytest

TRUE_OFFSETS = {1024, 50000, 1048576, 25000000, 49999992}

def test_backup_staging_exists():
    backup_file = '/home/user/backup_staging/file1.md'
    assert os.path.exists(backup_file), (
        f"Backup file {backup_file} does not exist. "
        "The recursive copy likely failed due to the symlink loop."
    )

def test_offsets_f1_score():
    offsets_file = '/home/user/offsets.txt'
    assert os.path.exists(offsets_file), f"Offsets file {offsets_file} does not exist."

    try:
        with open(offsets_file, 'r') as f:
            lines = f.read().strip().split()
        predicted_offsets = {int(x) for x in lines if x.strip().isdigit()}
    except Exception as e:
        pytest.fail(f"Failed to read or parse {offsets_file}: {e}")

    true_positives = len(predicted_offsets.intersection(TRUE_OFFSETS))
    false_positives = len(predicted_offsets - TRUE_OFFSETS)
    false_negatives = len(TRUE_OFFSETS - predicted_offsets)

    if (true_positives + false_positives) == 0:
        precision = 0.0
    else:
        precision = true_positives / (true_positives + false_positives)

    if (true_positives + false_negatives) == 0:
        recall = 0.0
    else:
        recall = true_positives / (true_positives + false_negatives)

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 1.0, (
        f"F1 score for found offsets is {f1:.2f}, which is below the threshold of 1.0. "
        f"Predicted: {predicted_offsets}, Expected: {TRUE_OFFSETS}"
    )