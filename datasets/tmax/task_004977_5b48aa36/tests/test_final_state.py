# test_final_state.py

import os
import subprocess
import pytest

def test_lib_rs_bugs_fixed():
    path = "/home/user/num_calc/src/lib.rs"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "as f32" not in content, "The precision loss bug (using f32) is still present in lib.rs."
    assert "0..=steps" not in content, "The off-by-one bug (0..=steps) is still present in lib.rs."
    assert "left_riemann_sum" in content, "The left_riemann_sum function is missing in lib.rs."

def test_cargo_test_passes():
    path = "/home/user/num_calc"
    assert os.path.isdir(path), f"Directory {path} does not exist."

    result = subprocess.run(
        ["cargo", "test"],
        cwd=path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed:\n{result.stdout}\n{result.stderr}"

def test_mre_compiles_and_runs():
    mre_path = "/home/user/mre.rs"
    assert os.path.isfile(mre_path), f"File {mre_path} does not exist."

    # Compile
    compile_result = subprocess.run(
        ["rustc", mre_path],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert compile_result.returncode == 0, f"rustc failed to compile mre.rs:\n{compile_result.stderr}"

    # Run
    exe_path = "/home/user/mre"
    assert os.path.isfile(exe_path), f"Executable {exe_path} was not created."

    run_result = subprocess.run(
        [exe_path],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert run_result.returncode == 0, f"./mre failed to run:\n{run_result.stderr}"

    # Check output
    output = run_result.stdout.strip()
    assert output, "./mre did not print any output."

    # The expected value of left_riemann_sum(0.0, 100.0, 1000) for x^2
    # step = 0.1
    # sum_{i=0}^{999} (i * 0.1)^2 * 0.1
    # = 0.1^3 * sum_{i=0}^{999} i^2
    # = 0.001 * (999 * 1000 * 1999) / 6
    # = 0.001 * 333333500 / 1
    # = 332833.5

    try:
        val = float(output)
        # Check if the value is reasonably close to the expected left Riemann sum
        assert abs(val - 332833.5) < 1.0, f"Expected output close to 332833.5, but got {val}"
    except ValueError:
        pytest.fail(f"Output of ./mre could not be parsed as a float: {output}")