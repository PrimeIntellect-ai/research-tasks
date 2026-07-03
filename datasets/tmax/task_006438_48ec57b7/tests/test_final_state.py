# test_final_state.py
import os

def invert_4x4(A):
    n = 4
    inv = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    a = [row[:] for row in A]
    for i in range(n):
        pivot = a[i][i]
        for j in range(n):
            a[i][j] /= pivot
            inv[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = a[k][i]
                for j in range(n):
                    a[k][j] -= factor * a[i][j]
                    inv[k][j] -= factor * inv[i][j]
    return inv

def compute_expected_weights():
    X = [
        [1.0, 2.0, 3.0, 4.0],
        [2.0, 4.0, 6.0, 8.001],
        [1.0, 0.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 1.0]
    ]
    y = [21.0, 16.0, 61.0, 61.0]

    # Compute X^T * X
    XtX = [[sum(X[k][i] * X[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

    # Add Ridge penalty
    for i in range(4):
        XtX[i][i] += 0.1

    # Invert
    inv_XtX = invert_4x4(XtX)

    # Compute X^T * y
    XtY = [sum(X[k][i] * y[k] for k in range(4)) for i in range(4)]

    # Compute w
    w = [sum(inv_XtX[i][j] * XtY[j] for j in range(4)) for i in range(4)]

    return " ".join(f"{val:.4f}" for val in w)

def test_executable_exists():
    exe_path = "/home/user/model/fit_model"
    assert os.path.isfile(exe_path), f"The compiled executable {exe_path} is missing. Did you compile the program?"
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_weights_output_exists():
    output_path = "/home/user/weights_output.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} is missing. Did you save the output weights?"

def test_weights_output_content():
    output_path = "/home/user/weights_output.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} is missing."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_content = compute_expected_weights()

    assert content == expected_content, (
        f"The contents of {output_path} are incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Got: '{content}'\n"
        "Ensure you added the ridge penalty lambda = 0.1 to the diagonal of XtX."
    )