# test_final_state.py
import os

def test_stable_result():
    result_path = "/home/user/stable_result.txt"
    reads_path = "/home/user/reads.txt"

    assert os.path.isfile(result_path), f"File {result_path} is missing. Did you redirect the output?"
    assert os.path.isfile(reads_path), f"File {reads_path} is missing."

    # Calculate expected sum in Python (float is IEEE 754 double precision, identical to Go's float64)
    expected_sum = 0.0
    with open(reads_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            val = float(line)
            expected_sum += val * 0.123456789

    expected_str = f"{expected_sum:.12f}"

    with open(result_path, "r") as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, (
        f"Numerical mismatch. Expected strictly sequential addition resulting in {expected_str}, "
        f"but got {actual_str} in {result_path}. Ensure the sum is accumulated in the exact order."
    )