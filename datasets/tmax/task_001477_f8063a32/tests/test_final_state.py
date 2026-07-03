# test_final_state.py
import os

def test_2hop_results_iou():
    """Test that the 2-hop results match the ground truth with IoU >= 0.85."""
    results_path = "/home/user/2hop_results.txt"
    assert os.path.exists(results_path), f"Output file {results_path} does not exist."

    truth = {"billing_info", "preferences", "telemetry"}

    with open(results_path, "r") as f:
        predictions = {line.strip().lower() for line in f if line.strip()}

    intersection = truth.intersection(predictions)
    union = truth.union(predictions)
    iou = len(intersection) / len(union) if union else 0.0

    assert iou >= 0.85, f"IoU {iou:.2f} is below threshold 0.85. Expected {truth}, got {predictions}"

def test_intermediate_files_exist():
    """Test that the intermediate files from the task steps exist."""
    assert os.path.exists("/home/user/parser.c"), "C parser source file /home/user/parser.c is missing."
    assert os.path.exists("/home/user/edges.csv"), "CSV edges file /home/user/edges.csv is missing."
    assert os.path.exists("/home/user/schema.db"), "SQLite database /home/user/schema.db is missing."