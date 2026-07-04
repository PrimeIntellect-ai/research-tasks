# test_final_state.py
import os
import sys

def test_final_result_correct():
    data_path = '/home/user/simulator/data.txt'
    result_path = '/home/user/simulator/final_result.txt'

    assert os.path.isfile(data_path), f"{data_path} is missing"
    assert os.path.isfile(result_path), f"{result_path} is missing. Did the pipeline complete successfully?"

    total = 0.0
    with open(data_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            x_str, y_str, z_str = line.strip().split(',')
            x, y, z = float(x_str), float(y_str), float(z_str)
            total += (x ** 2 + y) / z

    expected_result = f"{total:.2f}"

    with open(result_path, 'r') as f:
        actual_result = f.read().strip()

    assert actual_result == expected_result, (
        f"Incorrect final result in {result_path}. "
        f"Expected {expected_result}, but got {actual_result}. "
        "Check both the math formula and the concurrency logic in simulator.py."
    )

def test_parser_cycle_detection():
    # Dynamically import the student's parser.py
    sys.path.insert(0, '/home/user/simulator')
    try:
        import parser
    except ImportError:
        assert False, "Could not import parser.py from /home/user/simulator"

    assert hasattr(parser, 'resolve_alias'), "resolve_alias function missing in parser.py"

    # Test 1: Cycle detection
    test_config_cycle = {"node_A": "node_B", "node_B": "node_C", "node_C": "node_A"}
    try:
        res_cycle = parser.resolve_alias("node_A", test_config_cycle)
    except RecursionError:
        assert False, "resolve_alias raised a RecursionError. Cycle detection is not fixed."

    assert res_cycle == 'CYCLE_DETECTED', (
        f"resolve_alias did not return 'CYCLE_DETECTED' for a cycle. "
        f"Got: {res_cycle}"
    )

    # Test 2: Normal resolution
    test_config_normal = {"node_X": "node_Y", "node_Y": "node_Z"}
    res_normal = parser.resolve_alias("node_X", test_config_normal)
    assert res_normal == 'node_Z', (
        f"resolve_alias failed to resolve a normal alias chain. "
        f"Expected 'node_Z', got: {res_normal}"
    )