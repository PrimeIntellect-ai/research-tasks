# test_final_state.py
import os
import sys
import json
import pytest

def test_bug_report_exists_and_correct():
    report_path = "/home/user/bug_report.json"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "problematic_packet_index" in report_data, "Missing 'problematic_packet_index' in bug_report.json"
    assert report_data["problematic_packet_index"] == 2, f"Expected problematic_packet_index to be 2, got {report_data['problematic_packet_index']}"

    assert "problematic_payload" in report_data, "Missing 'problematic_payload' in bug_report.json"
    payload = report_data["problematic_payload"]
    assert payload.get("x") == 3.0, f"Expected problematic_payload.x to be 3.0, got {payload.get('x')}"
    assert payload.get("y") == 4.0, f"Expected problematic_payload.y to be 4.0, got {payload.get('y')}"
    assert payload.get("z") == 5.0, f"Expected problematic_payload.z to be 5.0, got {payload.get('z')}"

def test_math_engine_fixed():
    engine_dir = "/home/user/simulation_build"
    assert os.path.isdir(engine_dir), f"Directory {engine_dir} does not exist."

    sys.path.insert(0, engine_dir)
    try:
        import math_engine
    except ImportError:
        pytest.fail("Could not import math_engine from /home/user/simulation_build")

    problematic_payload = {"x": 3.0, "y": 4.0, "z": 5.0}

    try:
        result = math_engine.compute_trajectory(problematic_payload)
    except ZeroDivisionError:
        pytest.fail("math_engine.compute_trajectory still raises ZeroDivisionError for the problematic payload.")
    except Exception as e:
        pytest.fail(f"math_engine.compute_trajectory raised an unexpected exception: {e}")

    assert isinstance(result, float), f"Expected compute_trajectory to return a float, got {type(result)}"