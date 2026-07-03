# test_final_state.py
import os
import pytest
from collections import defaultdict

def test_f1_score_and_extraction():
    expected_safe_files = {
        "log1.txt": "data1",
        "config/settings.ini": "data2",
        "users.db": "data3"
    }

    extracted_dir = "/home/user/recovered_files"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist. The archive was not extracted to the correct location."

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for root, _, files in os.walk(extracted_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), extracted_dir)
            if rel_path in expected_safe_files:
                try:
                    with open(os.path.join(root, file), "r") as f:
                        if f.read() == expected_safe_files[rel_path]:
                            true_positives += 1
                        else:
                            false_positives += 1
                except Exception:
                    false_positives += 1
            else:
                false_positives += 1

    false_negatives = len(expected_safe_files) - true_positives

    if (true_positives + false_positives) == 0:
        precision = 0.0
    else:
        precision = true_positives / (true_positives + false_positives)

    if (true_positives + false_negatives) == 0:
        recall = 0.0
    else:
        recall = true_positives / (true_positives + false_negatives)

    if (precision + recall) == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.99, f"F1 Score: {f1:.4f} is below the threshold of 0.99 (TP: {true_positives}, FP: {false_positives}, FN: {false_negatives}). Zip-slip mitigation or extraction failed."

def test_hard_links_for_duplicates():
    extracted_dir = "/home/user/recovered_files"
    if not os.path.isdir(extracted_dir):
        pytest.fail(f"Directory {extracted_dir} does not exist.")

    content_to_inodes = defaultdict(set)

    for root, _, files in os.walk(extracted_dir):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath) and not os.path.islink(filepath):
                try:
                    with open(filepath, "rb") as f:
                        content = f.read()
                    stat = os.stat(filepath)
                    content_to_inodes[content].add(stat.st_ino)
                except Exception:
                    pass

    for content, inodes in content_to_inodes.items():
        assert len(inodes) == 1, f"Found multiple inodes {inodes} for identical file content. Duplicates were not properly replaced with hard links."