You are acting as a performance engineer working on a scientific application. 
We have a custom ODE solver in `/home/user/integrator.py` that implements an adaptive Runge-Kutta method. Currently, the solver is failing on the Van der Pol oscillator problem due to a bug in the step-size adaptation logic, which causes it to diverge or take too many steps (raising a `RuntimeError`).

Your tasks are:

1. **Fix the Integrator**: 
   Inspect `/home/user/integrator.py`. The `adaptive_integrate` function has a bug in how `h_new` is computed. The correct formula for the new step size should be: 
   `h_new = h * (tol / error)**0.2 * 0.9`
   Fix this logic so the integration completes successfully without taking too many steps. Also ensure that step sizes are bounded between `1e-5` and `1.0`.

2. **Reshape and Compare Observational Data**:
   We have ground truth observational data in `/home/user/obs_data.csv` (columns: `t`, `y0`, `y1`).
   Write a script `/home/user/compare.py` that:
   - Imports and runs `adaptive_integrate` from `integrator.py` for the Van der Pol oscillator (`vdp_deriv`) from $t=0$ to $t=20$ with initial conditions $y_0 = [2.0, 0.0]$ and $tol=1e-5$.
   - Uses `scipy.interpolate.interp1d` (cubic interpolation) on the solver's output to estimate the state values at the exact time points specified in `obs_data.csv`.
   - Calculates the Mean Absolute Error (MAE) between the interpolated solver outputs and the observational `y0` and `y1` values combined (average over all time points and both dimensions).
   - Writes the single MAE float value to a file `/home/user/mae.log`.

3. **Experimental Data Visualization**:
   In the same `/home/user/compare.py` script, generate a plot saving to `/home/user/plot.png` that plots the solver's $y_0$ over time as a line, and the observational $y_0$ as scatter points.

4. **Performance Profiling**:
   Write a script `/home/user/profile_run.py` that runs the fixed `adaptive_integrate` function (same parameters as above) using Python's built-in `cProfile` module. Save the binary profile output to `/home/user/profile.prof`.

5. **Regression Testing**:
   Write a test script `/home/user/test_integrator.py` using the `unittest` framework. It must test `adaptive_integrate` on the `vdp_deriv` (t=0 to 20, y0=[2.0, 0.0], tol=1e-5) and assert that the number of returned time steps is less than 1000, ensuring the step size bug is fixed.

Please complete all these steps. Do not modify the initial conditions or the ODE derivative function.