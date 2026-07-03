You are helping a computational chemistry researcher debug and run a numerical simulation of the Robertson chemical kinetics problem. This is a classic stiff system of ordinary differential equations (ODEs).

The ODE system is defined as follows:
dy1/dt = -0.04 * y1 + 10^4 * y2 * y3
dy2/dt = 0.04 * y1 - 10^4 * y2 * y3 - 3 * 10^7 * y2^2
dy3/dt = 3 * 10^7 * y2^2

Initial conditions at t = 0:
y1(0) = 1.0
y2(0) = 0.0
y3(0) = 0.0

The researcher has written the right-hand side (RHS) of this ODE in a C file located at `/home/user/sim_project/rhs_calc.c` to speed up evaluations. However, they need you to finish the pipeline:

1. **Compile the C code**: Compile `/home/user/sim_project/rhs_calc.c` into a shared library named `/home/user/sim_project/librhs.so` (ensure it is compiled with position-independent code).
2. **Write the Simulation & Convergence Test Script**: Create a Python script at `/home/user/sim_project/run_sim.py` that:
   - Uses `ctypes` to load the compiled `librhs.so` and wraps the C function so it can be passed to `scipy.integrate.solve_ivp`.
   - Solves the ODE system from t = 0 to t = 1000 using the `Radau` method.
   - Performs a convergence test by running the simulation over a sequence of relative tolerances (`rtol`): `[1e-2, 1e-3, 1e-4, 1e-5, 1e-6]`. For each run, set the absolute tolerance (`atol`) to be `1e-3 * rtol`.
   - Calculates the absolute difference in the final value of `y1(1000)` between each tolerance level and the tightest tolerance level (`rtol = 1e-6`).
   - Identifies the *largest* `rtol` from the list (excluding 1e-6) where the absolute difference in `y1(1000)` compared to the `1e-6` baseline is strictly less than `1e-5`.
3. **Save Results**: Your Python script must output a JSON file at `/home/user/sim_project/convergence_result.json` containing:
   - `"baseline_y1"`: The final value of y1(1000) at rtol = 1e-6.
   - `"threshold_rtol"`: The largest rtol that satisfies the error condition described above (if none satisfy it, set it to `1e-6`).

Please complete this pipeline so the researcher can verify the solver's convergence.