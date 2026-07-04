# test_final_state.py

import os
import statistics

def test_recovered_data():
    """Verify that the deleted file was correctly recovered."""
    path = "/home/user/recovered_data.csv"
    assert os.path.isfile(path), f"The file {path} does not exist. Did you recover it?"

    with open(path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 200, f"Expected 200 lines in {path}, got {len(lines)}."
    assert lines[100] == "CORRUPTED_DATA_ENTRY_MISSING_SENSOR", "The corrupted line is missing or at the wrong index."
    assert lines[0] == "1000000000.000", f"First line is incorrect, got {lines[0]}."
    assert lines[-1] == "1000000000.199", f"Last line is incorrect, got {lines[-1]}."

def test_result_txt():
    """Verify that the result file contains the correct population standard deviation."""
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"The file {path} does not exist. Did you run the fixed script?"

    with open(path, "r") as f:
        content = f.read().strip()

    # Recompute the expected population standard deviation
    data = []
    for i in range(200):
        if i != 100:
            data.append(1000000000.0 + i * 0.001)

    expected_pstdev = statistics.pstdev(data)
    expected_str = f"{expected_pstdev:.4f}"

    assert content == expected_str, f"Expected {path} to contain '{expected_str}', but got '{content}'."