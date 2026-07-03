# test_final_state.py
import os
import json
import math

def test_script_exists():
    assert os.path.isfile('/home/user/profile_hilbert.py'), "The script /home/user/profile_hilbert.py does not exist."

def test_plot_exists():
    assert os.path.isfile('/home/user/hilbert_plot.png'), "The plot /home/user/hilbert_plot.png does not exist."

def test_json_data():
    json_path = '/home/user/hilbert_data.json'
    assert os.path.isfile(json_path), f"The data file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "The file hilbert_data.json is not valid JSON."

    expected_Ns = ["2", "4", "6", "8", "10", "12"]
    for N in expected_Ns:
        assert N in data, f"Key '{N}' is missing from the JSON data."
        assert "condition_number" in data[N], f"Key 'condition_number' is missing for N={N}."
        assert "relative_error" in data[N], f"Key 'relative_error' is missing for N={N}."

        cond = data[N]["condition_number"]
        err = data[N]["relative_error"]

        assert isinstance(cond, (int, float)), f"Condition number for N={N} must be a float."
        assert isinstance(err, (int, float)), f"Relative error for N={N} must be a float."

    # Check invariants: condition numbers and errors should be strictly increasing
    conds = [data[N]["condition_number"] for N in expected_Ns]
    errs = [data[N]["relative_error"] for N in expected_Ns]

    for i in range(1, len(expected_Ns)):
        assert conds[i] > conds[i-1], f"Condition numbers should increase with N. Failed at N={expected_Ns[i]}."
        assert errs[i] > errs[i-1] or errs[i] > 1e-10, f"Relative errors should generally increase with N. Failed at N={expected_Ns[i]}."

    # Check approximate expected magnitudes for condition numbers
    # Theoretical condition numbers for Hilbert matrices grow as O(e^{3.5 * N})
    # N=2: ~19
    # N=4: ~1.5e4
    # N=6: ~1.5e7
    # N=12: ~1.6e16
    assert 10 < conds[0] < 30, "Condition number for N=2 is incorrect."
    assert 1e4 < conds[1] < 3e4, "Condition number for N=4 is incorrect."
    assert 1e7 < conds[2] < 3e7, "Condition number for N=6 is incorrect."
    assert 1e15 < conds[5] < 1e18, "Condition number for N=12 is incorrect."

    # Check approximate expected magnitudes for relative errors
    assert errs[0] < 1e-12, "Relative error for N=2 is too high."
    assert errs[5] > 1e-4, "Relative error for N=12 is too low (should reflect ill-conditioning)."