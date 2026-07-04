# test_final_state.py

import os
import sys
import math
import importlib.util
import pytest

def test_fix_report_contents():
    report_path = "/home/user/fix_report.txt"
    assert os.path.exists(report_path), f"Fix report not found at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in {report_path}, found {len(lines)}"

    assert lines[0] == "TXN-KLMN-9382", f"First line of fix_report.txt should be 'TXN-KLMN-9382', got '{lines[0]}'"
    assert lines[1] == "65.4330", f"Second line of fix_report.txt should be '65.4330', got '{lines[1]}'"

def test_risk_calc_fixed():
    module_path = "/home/user/app/risk_calc.py"
    assert os.path.exists(module_path), f"File not found: {module_path}"

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("risk_calc", module_path)
    risk_calc = importlib.util.module_from_spec(spec)
    sys.modules["risk_calc"] = risk_calc
    try:
        spec.loader.exec_module(risk_calc)
    except Exception as e:
        pytest.fail(f"Failed to load {module_path}: {e}")

    assert hasattr(risk_calc, "calculate_risk"), "calculate_risk function is missing in risk_calc.py"

    # Test with the crashed transaction values
    v_list = [10, 20, 30]
    w_list = [15, 25, 35]

    try:
        result = risk_calc.calculate_risk(v_list, w_list)
    except ValueError as e:
        pytest.fail(f"calculate_risk raised ValueError (likely math.sqrt of negative number): {e}")
    except Exception as e:
        pytest.fail(f"calculate_risk raised an unexpected error: {e}")

    expected_result = 1700 / math.sqrt(675)
    assert math.isclose(result, expected_result, rel_tol=1e-5), f"calculate_risk returned {result}, expected approximately {expected_result}"