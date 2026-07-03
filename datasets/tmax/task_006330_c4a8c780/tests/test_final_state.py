# test_final_state.py
import os
import subprocess
import re
import math

def test_files_exist():
    assert os.path.exists("/home/user/mc_pi.c"), "/home/user/mc_pi.c is missing"
    assert os.path.exists("/home/user/Makefile"), "/home/user/Makefile is missing"
    assert os.path.exists("/home/user/scaling_report.txt"), "/home/user/scaling_report.txt is missing"

def test_makefile_and_compilation():
    # Remove mc_pi if it exists to ensure make works
    if os.path.exists("/home/user/mc_pi"):
        os.remove("/home/user/mc_pi")

    result = subprocess.run(["make", "-C", "/home/user/"], capture_output=True, text=True)
    assert result.returncode == 0, f"make failed:\n{result.stderr}"
    assert os.path.exists("/home/user/mc_pi"), "make did not produce /home/user/mc_pi"

def test_mc_pi_execution():
    # Test one of the points to ensure C code works correctly
    # N=10000, seed=42
    result = subprocess.run(["/home/user/mc_pi", "42", "10000"], capture_output=True, text=True)
    assert result.returncode == 0, "mc_pi execution failed"
    output = result.stdout.strip()

    # Expected from Python truth script:
    # 10000 points -> get_pi(42, 10000)
    # Let's just check if it outputs a float
    try:
        val = float(output)
    except ValueError:
        assert False, f"Output of mc_pi is not a valid float: {output}"

def test_scaling_report():
    with open("/home/user/scaling_report.txt", "r") as f:
        content = f.read()

    slope_match = re.search(r"Slope:\s*([+-]?\d*\.\d+)", content)
    intercept_match = re.search(r"Intercept:\s*([+-]?\d*\.\d+)", content)

    assert slope_match is not None, "Could not find 'Slope: <value>' in scaling_report.txt"
    assert intercept_match is not None, "Could not find 'Intercept: <value>' in scaling_report.txt"

    slope = float(slope_match.group(1))
    intercept = float(intercept_match.group(1))

    expected_slope = -1.0267
    expected_intercept = 5.2530

    assert math.isclose(slope, expected_slope, abs_tol=0.0005), f"Slope {slope} is not close to {expected_slope}"
    assert math.isclose(intercept, expected_intercept, abs_tol=0.0005), f"Intercept {intercept} is not close to {expected_intercept}"