# test_final_state.py

import os
import json
import math
import sys
import pytest

def test_result_json():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"File {result_path} does not exist."

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON.")

    assert "sequence" in data, "'sequence' key missing in result.json"
    assert "optimal_weights" in data, "'optimal_weights' key missing in result.json"
    assert "min_energy" in data, "'min_energy' key missing in result.json"

    # 1. Check assembled sequence
    assert data["sequence"] == "ACCAAAT", f"Expected sequence 'ACCAAAT', got '{data['sequence']}'"

    # 2. Check optimal weights
    weights = data["optimal_weights"]
    assert isinstance(weights, list) and len(weights) == 3, "optimal_weights must be a list of 3 floats"

    expected_weights = [-37.78188583, -16.89094285, -1.0]
    for w, ew in zip(weights, expected_weights):
        assert isinstance(w, (int, float)), "Weights must be numeric"
        assert math.isclose(w, ew, rel_tol=1e-2, abs_tol=1e-2), f"Weight {w} is not close to expected {ew}"

    # 3. Check min energy
    energy = data["min_energy"]
    assert isinstance(energy, (int, float)), "min_energy must be numeric"
    expected_energy = 2362.46467
    assert math.isclose(energy, expected_energy, rel_tol=1e-2, abs_tol=1e-2), f"min_energy {energy} is not close to expected {expected_energy}"


def test_energy_function_stability():
    energy_path = "/home/user/energy.py"
    assert os.path.isfile(energy_path), f"File {energy_path} does not exist."

    sys.path.insert(0, "/home/user")
    try:
        from energy import compute_energy
    except ImportError:
        pytest.fail("Could not import compute_energy from /home/user/energy.py")
    finally:
        sys.path.pop(0)

    # Test with large weights that would cause OverflowError or inf in the naive implementation
    try:
        # A sequence with A, C, G to trigger all terms
        val = compute_energy([1000.0, 1000.0, 1000.0], "ACG")
    except OverflowError:
        pytest.fail("compute_energy raised OverflowError, indicating it is still numerically unstable.")
    except Exception as e:
        pytest.fail(f"compute_energy raised an unexpected error: {e}")

    assert not math.isinf(val), "compute_energy returned inf, indicating it is still numerically unstable."
    assert not math.isnan(val), "compute_energy returned NaN, indicating it is still numerically unstable."