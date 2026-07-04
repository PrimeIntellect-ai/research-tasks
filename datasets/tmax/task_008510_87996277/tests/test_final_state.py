# test_final_state.py
import os
import math
import subprocess

def f(x):
    return (x**3) * (math.cos(x/2)**2)

def get_expected_values():
    # 1. Normalization Constant (Z)
    N = 1000
    a, b = 0.0, 2.0
    dx = (b - a) / N

    Z = 0.0
    for i in range(N):
        x_i = a + i * dx
        x_next = a + (i + 1) * dx
        Z += (f(x_i) + f(x_next)) / 2.0 * dx

    expected_Z_str = f"{Z:.4f}"

    # 2 & 3. Bin probabilities and TVD
    num_bins = 10
    bin_width = (b - a) / num_bins
    steps_per_bin = 100
    dx_bin = bin_width / steps_per_bin

    tvd = 0.0
    for j in range(num_bins):
        bin_a = a + j * bin_width

        # Integrate over the bin
        P_A_unnorm = 0.0
        for k in range(steps_per_bin):
            x_k = bin_a + k * dx_bin
            x_next = bin_a + (k + 1) * dx_bin
            P_A_unnorm += (f(x_k) + f(x_next)) / 2.0 * dx_bin

        P_A = P_A_unnorm / Z
        P_B = 1.0 / num_bins # Uniform distribution over 10 bins is 0.1 per bin

        tvd += abs(P_A - P_B)

    tvd = tvd / 2.0
    expected_tvd_str = f"{tvd:.4f}"

    return expected_Z_str, expected_tvd_str

def test_script_exists_and_runs():
    script_path = "/home/user/prepare_data.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    # Run the script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

def test_norm_constant_output():
    expected_z, _ = get_expected_values()
    output_file = "/home/user/norm_constant.txt"

    assert os.path.isfile(output_file), f"Output file {output_file} not found."

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == expected_z, f"Expected normalization constant {expected_z}, but got {content}"

def test_tvd_output():
    _, expected_tvd = get_expected_values()
    output_file = "/home/user/tvd.txt"

    assert os.path.isfile(output_file), f"Output file {output_file} not found."

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == expected_tvd, f"Expected TVD {expected_tvd}, but got {content}"