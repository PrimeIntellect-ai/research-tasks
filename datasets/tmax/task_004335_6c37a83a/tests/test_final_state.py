# test_final_state.py
import os
import subprocess

def test_simulator_c_exists():
    assert os.path.isfile("/home/user/simulator.c"), "/home/user/simulator.c is missing."

def test_simulator_executable_exists_and_runs():
    executable = "/home/user/simulator"
    assert os.path.isfile(executable), f"{executable} is missing."
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

    # Run the simulator with a timeout to ensure the infinite loop is fixed
    try:
        result = subprocess.run([executable], capture_output=True, text=True, timeout=2.0)
        assert result.returncode == 0, f"Simulator exited with non-zero code: {result.returncode}"
        assert "Simulation complete." in result.stdout, "Simulator did not print expected output."
    except subprocess.TimeoutExpired:
        assert False, "Simulator timed out after 2 seconds. The infinite loop is likely not fixed."

def test_regression_script_exists_and_runs():
    script = "/home/user/test_regression.sh"
    assert os.path.isfile(script), f"{script} is missing."
    assert os.access(script, os.X_OK), f"{script} is not executable."

    # Run the regression script
    result = subprocess.run([script], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"test_regression.sh exited with non-zero code: {result.returncode}"
    assert "PASS" in result.stdout, "test_regression.sh did not echo 'PASS'."

def test_debug_report_contents():
    report = "/home/user/debug_report.txt"
    assert os.path.isfile(report), f"{report} is missing."

    with open(report, "r") as f:
        content = f.read().lower()

    # Check for mentions of float/precision/mantissa limitations
    precision_keywords = ["precision", "float", "mantissa", "ieee", "representable"]
    found_keyword = any(kw in content for kw in precision_keywords)
    assert found_keyword, "debug_report.txt does not seem to mention floating-point precision limitations."

    # Check for original code mention
    code_keywords = ["energy -= decay_rate", "33554432", "float energy", "while (energy > 0.0f)"]
    found_code = any(kw.lower() in content for kw in code_keywords)
    assert found_code, "debug_report.txt does not contain the original line of code causing the issue."