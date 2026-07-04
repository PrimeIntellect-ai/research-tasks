# test_final_state.py
import os
import sys
import pytest

def test_simulate_py_fixed():
    path = '/home/user/simulate.py'
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        content = f.read()

    assert 'def run_simulation' in content, "simulate.py is missing 'run_simulation' function"

    # Check for stiff solver
    has_bdf = 'BDF' in content
    has_radau = 'Radau' in content
    has_lsoda = 'LSODA' in content
    assert has_bdf or has_radau or has_lsoda, "simulate.py must use a stiff solver like 'BDF' or 'Radau'"

    # Check for tolerances
    assert '1e-6' in content or '10**-6' in content, "simulate.py is missing rtol=1e-6"
    assert '1e-9' in content or '10**-9' in content, "simulate.py is missing atol=1e-9"

def test_analysis_results_file_exists():
    path = '/home/user/analysis_results.h5'
    assert os.path.isfile(path), f"Missing file: {path}"

def test_analysis_results_contents():
    path = '/home/user/analysis_results.h5'
    assert os.path.isfile(path), f"Missing file: {path}"

    try:
        import h5py
        import numpy as np
    except ImportError:
        pytest.fail("h5py or numpy is not installed, cannot verify HDF5 contents.")

    with h5py.File(path, 'r') as f:
        # Check mu_tested
        assert 'mu_tested' in f, "Missing dataset 'mu_tested' in analysis_results.h5"
        mu_tested = np.array(f['mu_tested'])
        expected_mu = np.array([950, 990, 1000, 1010, 1050])
        np.testing.assert_array_equal(mu_tested, expected_mu, err_msg="mu_tested dataset does not match expected values")

        # Check chi_squared
        assert 'chi_squared' in f, "Missing dataset 'chi_squared' in analysis_results.h5"
        chi_squared = np.array(f['chi_squared'])
        assert len(chi_squared) == 5, f"Expected 5 elements in chi_squared, got {len(chi_squared)}"

        # Check best_mu attribute
        assert 'best_mu' in f.attrs, "Missing attribute 'best_mu' on the root group"
        best_mu = f.attrs['best_mu']
        assert best_mu == 1000, f"Expected best_mu to be 1000, got {best_mu}"

        # Check chi_squared value for mu=1000
        idx_1000 = np.where(mu_tested == 1000)[0][0]
        chi2_1000 = chi_squared[idx_1000]
        assert chi2_1000 < 1e-4, f"Expected chi_squared for mu=1000 to be very small, got {chi2_1000}"