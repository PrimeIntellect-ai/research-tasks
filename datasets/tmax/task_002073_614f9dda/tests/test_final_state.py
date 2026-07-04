# test_final_state.py

import os
import ctypes
import re

def test_libmetrics_built_and_linked():
    """Verify that libmetrics.so is built and properly linked with the math library."""
    so_path = "/home/user/uptime_monitor/libmetrics.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built."

    try:
        lib = ctypes.CDLL(so_path)
        lib.compute_penalty.restype = ctypes.c_double
        lib.compute_penalty.argtypes = [ctypes.c_double]

        # Test the function to ensure it doesn't fail due to missing 'sqrt' symbol
        result = lib.compute_penalty(100.0)
        assert isinstance(result, float), "compute_penalty did not return a float."
    except OSError as e:
        assert False, f"Failed to load {so_path}. It might not be linked correctly (e.g., missing -lm). Error: {e}"

def test_sla_report_generated():
    """Verify that sla_report.txt was successfully generated and contains expected output."""
    report_path = "/home/user/uptime_monitor/sla_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} was not generated."

    with open(report_path, "r") as f:
        content = f.read()

    assert "Converged in" in content, "Report file does not contain iteration count."
    assert "Final downtime:" in content, "Report file does not contain final downtime."

def test_calculate_sla_script_fixed():
    """Verify that the calculate_sla.py script uses a tolerance check instead of exact equality."""
    script_path = "/home/user/uptime_monitor/calculate_sla.py"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # Check that the exact equality check has been removed
    assert "current_sla != target_sla" not in content, "The exact equality check 'current_sla != target_sla' is still in the script."

    # Check that a tolerance check is implemented (e.g., using abs)
    assert re.search(r"abs\s*\(\s*current_sla\s*-\s*target_sla\s*\)", content) is not None, "The script does not appear to use a proper absolute difference tolerance check."