# test_final_state.py
import os
import math

def test_final_threshold_file():
    path = "/home/user/final_threshold.txt"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"Content of {path} is not a valid float: '{content}'"

    expected = 0.001707825127659933
    assert math.isclose(val, expected, abs_tol=1e-5), f"Calculated threshold {val} is not within acceptable tolerance of {expected}."

def test_anomaly_detector_fixes():
    script_path = "/home/user/anomaly_detector.py"
    assert os.path.isfile(script_path), f"Expected script file {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    content_lower = content.lower()
    content_no_spaces = content.replace(" ", "")

    # 1. Check SQL query debugging
    assert "'ok'" in content_lower or '"ok"' in content_lower, "The script must filter for status 'OK'."
    assert ">0" in content_no_spaces, "The script must filter for positive latency (> 0)."

    # 2. Check Floating-point precision repair
    naive_formula = "(sum_x2-(sum_x**2)/n)/n"
    assert naive_formula not in content_no_spaces, "The naive variance formula must be removed to fix catastrophic cancellation."

    has_statistics = "statistics" in content
    has_welford = "mean" in content_lower and "m2" in content_lower # basic heuristic for Welford's
    assert has_statistics or has_welford or "variance" in content_lower, "The script should use a stable variance calculation method."

    # 3. Check Convergence failure repair
    assert "1e-7" in content_lower or "0.0000001" in content_lower, "The script must break the convergence loop when the delta is smaller than 1e-7."