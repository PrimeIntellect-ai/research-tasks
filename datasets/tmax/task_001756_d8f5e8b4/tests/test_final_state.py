# test_final_state.py

import json
import os
import sys
import pytest

def test_benchmark_results():
    benchmark_file = '/home/user/benchmark_results.json'
    assert os.path.exists(benchmark_file), f"Benchmark results file not found at {benchmark_file}"

    with open(benchmark_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Benchmark results file is not valid JSON")

    assert 'value_25' in data, "JSON missing 'value_25' key"
    assert data['value_25'] == 1389537, f"Expected value_25 to be 1389537, got {data['value_25']}"

    assert 'c_faster_than_py' in data, "JSON missing 'c_faster_than_py' key"
    assert data['c_faster_than_py'] is True, "Expected c_faster_than_py to be True"

def test_c_extension_built_and_correct():
    project_dir = '/home/user/math_accelerator'
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)

    try:
        import math_accelerator.trib_c as tc
    except ImportError as e:
        pytest.fail(f"Failed to import math_accelerator.trib_c. Extension was not built properly. Error: {e}")

    assert tc.tribonacci(0) == 0, "C extension tribonacci(0) failed"
    assert tc.tribonacci(1) == 1, "C extension tribonacci(1) failed"
    assert tc.tribonacci(2) == 1, "C extension tribonacci(2) failed"
    assert tc.tribonacci(10) == 81, "C extension tribonacci(10) failed"
    assert tc.tribonacci(25) == 1389537, "C extension tribonacci(25) failed"

def test_python_fallback_correct():
    project_dir = '/home/user/math_accelerator'
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)

    try:
        import math_accelerator.trib_py as tp
    except ImportError as e:
        pytest.fail(f"Failed to import math_accelerator.trib_py. Error: {e}")

    assert hasattr(tp, 'tribonacci'), "trib_py.py is missing tribonacci function"

    # Test base cases and general cases
    assert tp.tribonacci(0) == 0, "Python fallback tribonacci(0) should be 0"
    assert tp.tribonacci(1) == 1, "Python fallback tribonacci(1) should be 1"
    assert tp.tribonacci(2) == 1, "Python fallback tribonacci(2) should be 1"
    assert tp.tribonacci(10) == 81, "Python fallback tribonacci(10) should be 81"
    assert tp.tribonacci(25) == 1389537, "Python fallback tribonacci(25) should be 1389537"