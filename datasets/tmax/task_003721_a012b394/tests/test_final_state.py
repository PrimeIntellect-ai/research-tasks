# test_final_state.py
import os
import math

def compute_expected_log(input_file):
    expected_lines = []
    with open(input_file, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            vals = list(map(float, line.split()))
            if len(vals) != 9:
                continue
            A = [vals[0:3], vals[3:6], vals[6:9]]
            L = [[0.0]*3 for _ in range(3)]
            stable = True
            for i in range(3):
                for j in range(i + 1):
                    s = A[i][j]
                    for k in range(j):
                        s -= L[i][k] * L[j][k]
                    if i == j:
                        if s <= 1e-6:
                            stable = False
                            break
                        L[i][j] = math.sqrt(s)
                    else:
                        L[i][j] = s / L[j][j]
                if not stable:
                    break

            if stable:
                l_sum = sum(sum(row) for row in L)
                expected_lines.append(f"Stable: {l_sum:.2f}")
            else:
                expected_lines.append("Unstable")
    return expected_lines

def test_stable_log_exists():
    assert os.path.exists("/home/user/stable_log.txt"), "/home/user/stable_log.txt does not exist."

def test_stable_log_contents():
    input_file = "/home/user/matrices.txt"
    assert os.path.exists(input_file), f"{input_file} is missing, cannot verify."

    expected_lines = compute_expected_log(input_file)

    with open("/home/user/stable_log.txt", "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in stable_log.txt, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."