# test_final_state.py
import os

def test_results_file_exists_and_correct():
    results_path = "/home/user/results.txt"
    assert os.path.exists(results_path), "results.txt does not exist. Did you run pipeline.sh?"

    with open(results_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"results.txt should contain exactly 2 lines, but found {len(lines)}."

    expected = {
        "/home/user/data/dataset 1.csv: 0.0100",
        "/home/user/data/dataset 2.csv: 1.1875"
    }

    actual = set(lines)
    assert actual == expected, f"Output mismatch in results.txt. Expected {expected}, got {actual}"