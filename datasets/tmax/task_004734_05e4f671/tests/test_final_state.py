# test_final_state.py
import os
import json
import stat

def test_simulator_executable_exists():
    """Verify that the simulator was compiled and is executable."""
    exe_path = '/home/user/simulator'
    assert os.path.isfile(exe_path), f"{exe_path} does not exist. Did you compile the simulator?"
    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{exe_path} is not executable."

def test_report_json_exists_and_valid():
    """Verify that report.json exists and contains the correct keys and values."""
    report_path = '/home/user/report.json'
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not a valid JSON file."

    expected_keys = {"optimal_x", "optimal_y", "p_value", "t_statistic"}
    assert set(report.keys()) == expected_keys, f"report.json must contain exactly the keys: {expected_keys}"

    assert isinstance(report["optimal_x"], (int, float)), "optimal_x must be a number"
    assert isinstance(report["optimal_y"], (int, float)), "optimal_y must be a number"
    assert isinstance(report["p_value"], (int, float)), "p_value must be a number"
    assert isinstance(report["t_statistic"], (int, float)), "t_statistic must be a number"

    # Check optimal values
    assert abs(report["optimal_x"] - 7.5) < 1e-5, f"Expected optimal_x to be 7.5, got {report['optimal_x']}"
    assert abs(report["optimal_y"] - 3.2) < 1e-5, f"Expected optimal_y to be 3.2, got {report['optimal_y']}"

    # Check statistical values
    assert report["t_statistic"] > 10.0, f"Expected a large positive t_statistic (> 10), got {report['t_statistic']}"
    assert report["p_value"] < 0.01, f"Expected a very small p_value (< 0.01), got {report['p_value']}"