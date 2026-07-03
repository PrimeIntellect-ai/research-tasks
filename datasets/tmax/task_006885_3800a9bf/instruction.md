You are a data scientist working on fitting a model that involves the 1D Bratu equation, a classic non-linear ODE. Before fitting parameters, you need a robust, self-written forward solver that implements manual mesh refinement and convergence testing.

Your task is to write a Python script at `/home/user/solve_bratu.py` that solves the Bratu boundary value problem using the finite difference method and `scipy.optimize.root`.

The boundary value problem is:
d²u/dx² + exp(u) = 0  for x in (0, 1)
u(0) = 0, u(1) = 0

You must implement the following specific algorithm:
1. Discretize the domain (0, 1) using `N` equally spaced **interior** points. The step size is `h = 1 / (N + 1)`.
2. Use the standard second-order central finite difference approximation for the second derivative: 
   u''(x_i) ≈ (u_{i-1} - 2u_i + u_{i+1}) / h²
3. Start with an initial mesh of `N = 3` interior points.
4. Use `scipy.optimize.root` (with its default solver) to solve the resulting system of `N` non-linear equations. Always use an array of zeros of length `N` as your initial guess for the root finder.
5. Extract the value of the solution at the exact midpoint of the domain, x = 0.5. Since `N` will always be odd in this procedure, this corresponds to the interior point at integer index `N // 2` (zero-indexed).
6. Compare the midpoint value of the current mesh (`u_mid_current`) with the midpoint value from the previous mesh (`u_mid_prev`). 
7. If the absolute difference `|u_mid_current - u_mid_prev|` is less than or equal to `1e-5`, the grid has converged. Stop the loop.
8. If it has not converged (or if it is the very first step `N=3`), refine the mesh by setting `N_new = 2 * N + 1` and repeat the process.
9. Once converged, write the final `N` and the final midpoint value (rounded to exactly 6 decimal places) to a log file at `/home/user/bratu_convergence.log`.

The format of `/home/user/bratu_convergence.log` must be exactly:
`N=<final_N>, u_mid=<final_u_mid_rounded>`
(e.g., `N=15, u_mid=0.123456`)

Ensure your script is fully self-contained and runs without errors. You may install `numpy` and `scipy` using `pip` if they are not already installed.