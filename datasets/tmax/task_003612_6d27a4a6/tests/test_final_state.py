# test_final_state.py

import os
import pytest

def compute_accuracy(ref, hyp):
    ref_words = ref.lower().split()
    hyp_words = hyp.lower().split()

    # Check if the exact redactions are present
    redacted_count = hyp.count("[REDACTED]")
    if redacted_count < 2:
        return 0.0 # Failed to redact properly

    # Simple overlap coefficient for text
    overlap = len(set(ref_words) & set(hyp_words))
    if len(set(ref_words)) == 0:
        return 0.0
    acc = overlap / float(len(set(ref_words)))
    return acc

def test_final_report_accuracy():
    """Test that the final report exists and meets the accuracy threshold."""
    report_path = "/home/user/final_report.txt"
    assert os.path.isfile(report_path), f"Final report is missing at {report_path}"

    with open(report_path, "r") as f:
        output = f.read()

    expected = "The backup server is at [REDACTED] and the billing account uses the card [REDACTED] for processing."

    score = compute_accuracy(expected, output)

    assert score >= 0.85, f"Accuracy score {score:.2f} is below the threshold of 0.85. Output was: {output}"