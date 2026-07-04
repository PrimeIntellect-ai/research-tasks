# test_final_state.py

import os
import sys
import importlib.util

def test_makefile_fixed():
    makefile_path = "/home/user/workspace/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "METRICS_DIR=/home/user/workspace/data" in content, "Makefile does not contain the correct METRICS_DIR path."

def test_compute_stats_fixed():
    compute_stats_path = "/home/user/workspace/src/compute_stats.py"
    assert os.path.isfile(compute_stats_path), f"compute_stats.py is missing at {compute_stats_path}"

    # Dynamically import compute_stats.py
    spec = importlib.util.spec_from_file_location("compute_stats", compute_stats_path)
    compute_stats = importlib.util.module_from_spec(spec)
    sys.modules["compute_stats"] = compute_stats
    spec.loader.exec_module(compute_stats)

    assert hasattr(compute_stats, "calculate_variance"), "calculate_variance function is missing."

    # Test the fix
    try:
        result = compute_stats.calculate_variance([42.0])
        assert result == 0.0, f"Expected calculate_variance([42.0]) to return 0.0, got {result}"
    except ZeroDivisionError:
        pytest.fail("calculate_variance([42.0]) raised ZeroDivisionError. The bug is not fixed.")

def test_regression_script_exists():
    regression_test_path = "/home/user/workspace/test_regression.py"
    assert os.path.isfile(regression_test_path), f"Regression test script missing at {regression_test_path}"

def test_logs_exist_and_correct():
    test_output_path = "/home/user/workspace/test_output.log"
    build_success_path = "/home/user/workspace/build_success.log"

    assert os.path.isfile(test_output_path), f"Test output log missing at {test_output_path}"
    assert os.path.isfile(build_success_path), f"Build success log missing at {build_success_path}"

    with open(build_success_path, "r") as f:
        build_content = f.read()

    assert "Variance: 0.0000" in build_content, "build_success.log does not contain 'Variance: 0.0000'. The build process might not have run successfully or the bug wasn't fixed."