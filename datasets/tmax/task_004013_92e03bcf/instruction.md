I am a researcher studying the numerical stability of finite difference methods for 1D heat conduction, and I need you to write a Python script to automate my simulation workflow. 

Please create a self-contained Python script at `/home/user/run_sim.py` that performs a mesh refinement and numerical stability study on the 1D Poisson equation: 
-d²u/dx² = sin(πx)  for x in (0, 1)
with Dirichlet boundary conditions u(0) = u(1) = 0.

The exact analytical solution is u_exact(x) = (1/π²) * sin(πx).

Your script should do the following:
1. Iterate over the following internal grid sizes (N): 10, 50, 100, 200.
2. For each N, construct the standard 1D finite difference matrix `A` (size N x N) for the negative Laplacian (-d²u/dx²) using a uniform grid with spacing h = 1/(N+1). The grid points are x_i = i * h for i=1 to N.
3. Calculate the condition number of `A` using Singular Value Decomposition (SVD). The condition number is the ratio of the maximum singular value to the minimum singular value.
4. Construct the right-hand side vector `b` where b_i = sin(π * x_i).
5. Solve the system A * u = b using a **Cholesky decomposition** (since A is symmetric positive-definite).
6. Calculate the "clean_error", which is the maximum absolute difference (L-infinity norm) between your numerical solution `u` and the exact solution `u_exact` evaluated at the grid points.
7. To test numerical stability, create a deterministic perturbation vector `p` where p_i = 1e-6 * (-1)^i. Add this to `b` to get `b_pert`.
8. Solve the perturbed system A * u_pert = b_pert using the *same* Cholesky factors computed in step 5.
9. Calculate the "perturbed_diff", which is the maximum absolute difference between `u_pert` and `u`.

The script must save the results to a JSON file at `/home/user/sim_results.json`. The JSON file should have the N values as string keys ("10", "50", "100", "200"). Each key should map to an object containing:
- `"condition_number"`: (float)
- `"clean_error"`: (float)
- `"perturbed_diff"`: (float)

Run the script so the JSON file is generated. Ensure that standard libraries like `numpy` and `scipy` are used (you can install them if necessary).