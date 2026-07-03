# test_final_state.py
import os

def test_decoded_accuracy():
    decoded_path = '/home/user/decoded.txt'
    truth_path = '/app/data/ground_truth.txt'

    assert os.path.isfile(decoded_path), f"Output file {decoded_path} is missing."
    assert os.path.isfile(truth_path), f"Ground truth file {truth_path} is missing."

    with open(decoded_path, 'r') as f:
        pred = [line.strip() for line in f if line.strip()]

    with open(truth_path, 'r') as f:
        truth = [line.strip() for line in f if line.strip()]

    assert len(pred) > 0, "Decoded output is empty."

    correct = sum(1 for p, t in zip(pred, truth) if p == t)
    accuracy = correct / len(truth)

    assert accuracy >= 0.95, f"Accuracy is {accuracy:.2f}, which is below the threshold of 0.95."