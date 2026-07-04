# test_final_state.py

import os
import json
import math

def test_profiling_report_exists_and_valid():
    report_path = "/home/user/profiling_report.json"
    assert os.path.exists(report_path), f"Report file {report_path} was not created."

    with open(report_path, "r") as f:
        try:
            ans = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {report_path} does not contain valid JSON."

    expected_keys = {
        "num_ca_atoms",
        "min_eigenvalue_unreg",
        "condition_number_unreg",
        "trace_reg",
        "top_3_eigenvalues_reg",
        "ks_statistic"
    }

    missing_keys = expected_keys - set(ans.keys())
    assert not missing_keys, f"Missing keys in JSON report: {missing_keys}"

def test_profiling_report_values():
    report_path = "/home/user/profiling_report.json"
    with open(report_path, "r") as f:
        ans = json.load(f)

    # 1. Number of CA atoms
    assert ans["num_ca_atoms"] == 7, f"Expected 7 CA atoms, got {ans['num_ca_atoms']}"

    # 2. Trace of regularized matrix
    # The unregularized matrix has 1s on the diagonal (exp(0) = 1).
    # N = 7, so trace of M is 7. Regularization adds lambda=1e-5 to each diagonal element.
    # Expected trace = 7 * (1 + 1e-5) = 7.00007
    expected_trace = 7.00007
    assert math.isclose(ans["trace_reg"], expected_trace, rel_tol=1e-4), \
        f"Expected trace_reg ~ {expected_trace}, got {ans['trace_reg']}"

    # 3. Minimum eigenvalue of unregularized matrix
    # Since residues 3/4 and 6/7 are identical, the matrix is rank deficient.
    # The minimum eigenvalue should be effectively zero (or slightly negative due to floating point).
    min_eval = ans["min_eigenvalue_unreg"]
    assert isinstance(min_eval, (int, float)), "min_eigenvalue_unreg must be a number"
    assert min_eval < 1e-5, f"Expected min_eigenvalue_unreg to be near 0, got {min_eval}"

    # 4. Condition number of unregularized matrix
    # A near-singular matrix will have a very large condition number.
    cond_unreg = ans["condition_number_unreg"]
    assert isinstance(cond_unreg, (int, float)), "condition_number_unreg must be a number"
    assert cond_unreg > 1e14, f"Expected condition_number_unreg to be very large (>1e14), got {cond_unreg}"

    # 5. Top 3 eigenvalues of regularized matrix
    top_3 = ans["top_3_eigenvalues_reg"]
    assert isinstance(top_3, list) and len(top_3) == 3, "top_3_eigenvalues_reg must be a list of 3 floats"
    assert all(isinstance(x, (int, float)) for x in top_3), "top_3_eigenvalues_reg elements must be numbers"
    # Check descending order
    assert top_3[0] >= top_3[1] >= top_3[2], "top_3_eigenvalues_reg must be sorted in descending order"
    # Eigenvalues should be positive
    assert top_3[2] > 0, "Top eigenvalues should be positive"

    # 6. KS Statistic
    ks_stat = ans["ks_statistic"]
    assert isinstance(ks_stat, (int, float)), "ks_statistic must be a number"
    assert 0.0 <= ks_stat <= 1.0, f"KS statistic must be between 0 and 1, got {ks_stat}"