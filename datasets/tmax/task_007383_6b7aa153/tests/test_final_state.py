# test_final_state.py
import os
import math

def compute_expected_max_temp():
    # Re-implement the correct logic using only standard library
    coords = [
        (-1.424, -2.193, 0.218),
        (0.039, -2.221, 0.245),
        (0.556, -0.814, 0.509),
        (1.455, -0.612, 1.328),
        (0.592, -3.155, 1.306),
        (-0.038, 0.147, -0.198),
        (0.360, 1.543, 0.007),
        (0.267, 2.368, -1.272),
        (-0.569, 2.115, -2.138),
        (-0.457, 2.164, 1.143),
        (0.063, 3.856, 1.503)
    ]

    N = 20
    dx = 1.0

    # Grid initialization
    T = [[[0.0 for _ in range(N)] for _ in range(N)] for _ in range(N)]

    # Map atoms to grid exactly as np.digitize(..., edges) - 1 would do
    for x, y, z in coords:
        ix = int(math.floor(x + 10.0))
        iy = int(math.floor(y + 10.0))
        iz = int(math.floor(z + 10.0))

        ix = max(0, min(N-1, ix))
        iy = max(0, min(N-1, iy))
        iz = max(0, min(N-1, iz))

        T[ix][iy][iz] = 100.0

    alpha = 0.1
    # Maximum stable dt
    dt = (dx**2) / (6.0 * alpha)
    steps = 500

    for _ in range(steps):
        T_new = [[[T[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
        for i in range(1, N-1):
            for j in range(1, N-1):
                for k in range(1, N-1):
                    laplacian = (
                        T[i+1][j][k] + T[i-1][j][k] +
                        T[i][j+1][k] + T[i][j-1][k] +
                        T[i][j][k+1] + T[i][j][k-1] -
                        6.0 * T[i][j][k]
                    ) / (dx**2)
                    T_new[i][j][k] = T[i][j][k] + alpha * dt * laplacian
        T = T_new

    max_val = 0.0
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if T[i][j][k] > max_val:
                    max_val = T[i][j][k]

    return max_val

def test_files_generated():
    assert os.path.exists("/home/user/z_profile.png"), "/home/user/z_profile.png was not generated."
    assert os.path.exists("/home/user/max_temp.txt"), "/home/user/max_temp.txt was not generated."

def test_max_temp_correct():
    txt_path = "/home/user/max_temp.txt"
    assert os.path.exists(txt_path), f"Missing file: {txt_path}"

    with open(txt_path, "r") as f:
        content = f.read().strip()

    try:
        actual_temp = float(content)
    except ValueError:
        assert False, f"Could not parse the content of {txt_path} as a float. Found: {content}"

    expected_temp = compute_expected_max_temp()

    assert not math.isnan(actual_temp), "The maximum temperature is NaN, indicating numerical instability."
    assert not math.isinf(actual_temp), "The maximum temperature is infinite, indicating numerical instability."

    # Check if the actual temperature matches the expected temperature rounded to 4 decimal places
    expected_rounded = round(expected_temp, 4)
    actual_rounded = round(actual_temp, 4)

    assert math.isclose(actual_rounded, expected_rounded, rel_tol=1e-3, abs_tol=1e-3), \
        f"Expected max temperature to be approximately {expected_rounded}, but got {actual_rounded}. Ensure dt is calculated correctly."