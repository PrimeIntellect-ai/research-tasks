# test_final_state.py
import os
import subprocess
import tempfile
import pytest

def test_sim_bin_compiled():
    bin_path = "/home/user/sim_bin"
    assert os.path.isfile(bin_path), f"Executable not found at {bin_path}"
    assert os.access(bin_path, os.X_OK), f"File at {bin_path} is not executable"

def test_best_beta_content():
    txt_path = "/home/user/best_beta.txt"
    assert os.path.isfile(txt_path), f"Result file not found at {txt_path}"

    with open(txt_path, "r") as f:
        content = f.read().strip()

    assert content != "", "best_beta.txt is empty"

    # Verify the contents by recomputing the expected value to be robust to exact simulation details
    src_path = "/home/user/sim_src/sim.cpp"
    assert os.path.isfile(src_path), f"Source file missing at {src_path}"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_bin = os.path.join(tmpdir, "sim")
        comp = subprocess.run(
            ["g++", "-O3", "-std=c++11", src_path, "-o", tmp_bin],
            capture_output=True, text=True
        )
        assert comp.returncode == 0, f"Test suite failed to compile sim.cpp: {comp.stderr}"

        def evaluate_beta(beta):
            total_infections = 0
            for seed in range(1, 101):
                res = subprocess.run(
                    [tmp_bin, str(beta), "1000", str(seed)],
                    capture_output=True, text=True
                )
                total_infections += int(res.stdout.strip())
            mean_infections = total_infections / 100.0
            return mean_infections - 634.0

        # Bisection method to find the root
        a, b = 0.1, 0.5
        fa = evaluate_beta(a)
        fb = evaluate_beta(b)

        assert fa * fb < 0, "Root is not bracketed in [0.1, 0.5]"

        tol = 1e-6
        while (b - a) / 2.0 > tol:
            mid = (a + b) / 2.0
            fmid = evaluate_beta(mid)
            if fmid == 0:
                a = b = mid
                break
            elif fa * fmid < 0:
                b = mid
                fb = fmid
            else:
                a = mid
                fa = fmid

        expected_beta = (a + b) / 2.0
        expected_str = f"{expected_beta:.4f}"

    assert content == expected_str, f"Expected beta to be {expected_str}, but got {content} in best_beta.txt"