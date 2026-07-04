I am a performance engineer profiling an orbital mechanics application, and I'm running into an issue where our simulations are diverging. We use a vendored version of a numerical integration library, but it seems there's a bug in its adaptive step-size logic that causes the simulations to blow up instead of refining the step size.

Your task has several parts:

1. **Fix the Vendored Package:**
   There is a vendored package located at `/app/scipack-1.0.0`. It contains a module `scipack.ode` with an adaptive Runge-Kutta integrator (`rk45_step`).
   A recent bad commit perturbed the step-size adaptation formula. You need to find the error in `/app/scipack-1.0.0/scipack/ode.py` and fix it. (Hint: look at how `dt_new` is calculated relative to the error and tolerance; the ratio might be inverted). Make sure the package is usable by your scripts (you may need to install it locally or adjust `PYTHONPATH`).

2. **Simulate and Find the Root:**
   Read the initial conditions from the HDF5 file `/home/user/initial_states.h5`. This file contains a dataset `state_0` which is a 1D array of 4 elements: `[x, y, vx, vy]`.
   The system of ODEs represents a simple non-linear oscillator:
   dx/dt = vx
   dy/dt = vy
   dvx/dt = -x - 0.5 * x**3
   dvy/dt = -y - 0.5 * y**3

   Using the fixed `scipack.ode.solve_ivp_adaptive`, simulate this system from `t=0` to `t=10`.
   We are interested in the exact time `T` when the oscillator crosses the `x`-axis from positive `y` to negative `y` (i.e., `y=0` and `vy < 0`). Use a non-linear root-finding method (like `scipy.optimize.brentq`) on an interpolation of the trajectory to find this exact crossing time `T` between `t=0` and `t=10`.

3. **Bootstrap Confidence Intervals:**
   We need to quantify the uncertainty of `T` due to measurement noise in the initial conditions.
   Create a reproducible pipeline:
   - Set the numpy random seed to `42`.
   - Generate 100 perturbed initial states by adding independent Gaussian noise with mean 0 and standard deviation 0.01 to the original `state_0`.
   - For each perturbed state, run the simulation and find the crossing time `T`.
   - Compute the 95% Bootstrap Confidence Interval (using 1000 bootstrap resamples) for the mean of the crossing time `T`. (Calculate the 2.5th and 97.5th percentiles of the bootstrap distribution of the mean). Set the random seed to `42` right before the bootstrap resampling.

4. **Serve the Results:**
   Create and run a simple HTTP server (e.g., using Flask or `http.server`) that listens on `127.0.0.1:8080`.
   It must implement a `GET /metrics` endpoint that returns a JSON response with the bootstrap CI:
   ```json
   {
     "t_crossing_mean": <float>,
     "ci_95_lower": <float>,
     "ci_95_upper": <float>
   }
   ```
   Leave this server running in the background so it can be queried. Provide an auth token in the headers for security: the server must only respond with 200 OK if the request header `X-Auth-Token` is exactly `perf-eng-secret`. Otherwise, return 401 Unauthorized.