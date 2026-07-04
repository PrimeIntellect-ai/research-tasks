# test_final_state.py
import os
import pytest

def test_output_file_exists():
    """Check if the output NetCDF file was created."""
    assert os.path.isfile('/home/user/results/output.nc'), "/home/user/results/output.nc is missing. Did the script run successfully?"

def test_output_file_contents_and_accuracy():
    """Verify the NetCDF file contents and the accuracy of the computed roots."""
    try:
        import h5py
        import netCDF4 as nc
        import numpy as np
        from scipy.integrate import solve_ivp
        from scipy.optimize import root_scalar
    except ImportError as e:
        pytest.fail(f"Required library missing: {e}")

    # Read initial conditions
    try:
        with h5py.File('/home/user/data/initial_conditions.h5', 'r') as f:
            x0_arr = f['x0'][:]
            y0_arr = f['y0'][:]
            alpha_arr = f['alpha'][:]
    except Exception as e:
        pytest.fail(f"Failed to read input HDF5 file: {e}")

    # Compute expected roots
    expected_t_root = []
    for x0, y0, alpha in zip(x0_arr, y0_arr, alpha_arr):
        def ode(t, z):
            x, y = z
            return [-alpha * x + y**2, -x - alpha * y]

        sol = solve_ivp(ode, [0, 10], [x0, y0], dense_output=True)

        def objective(t):
            z = sol.sol(t)
            return z[0] - z[1]

        res = root_scalar(objective, bracket=[0.1, 10.0], method='brentq')
        expected_t_root.append(res.root)

    expected_t_root = np.array(expected_t_root)

    # Read agent's output
    try:
        ds = nc.Dataset('/home/user/results/output.nc', 'r')
    except Exception as e:
        pytest.fail(f"Failed to read output NetCDF file: {e}")

    # Check dimensions and variables
    assert 'index' in ds.dimensions, "Dimension 'index' is missing in the output NetCDF file."
    assert len(ds.dimensions['index']) == len(x0_arr), "Dimension 'index' has incorrect length."

    for var in ['x0', 'y0', 'alpha', 't_root']:
        assert var in ds.variables, f"Variable '{var}' is missing in the output NetCDF file."
        assert ds.variables[var].dtype in [np.float64, float], f"Variable '{var}' should be float64."

    agent_x0 = ds.variables['x0'][:]
    agent_y0 = ds.variables['y0'][:]
    agent_alpha = ds.variables['alpha'][:]
    agent_t_root = ds.variables['t_root'][:]

    # Check that inputs were copied correctly
    assert np.allclose(agent_x0, x0_arr), "Variable 'x0' does not match the input data."
    assert np.allclose(agent_y0, y0_arr), "Variable 'y0' does not match the input data."
    assert np.allclose(agent_alpha, alpha_arr), "Variable 'alpha' does not match the input data."

    # Check the computed roots
    assert np.allclose(agent_t_root, expected_t_root, rtol=1e-3, atol=1e-3), "Computed 't_root' values do not match expected results within tolerance."

    ds.close()