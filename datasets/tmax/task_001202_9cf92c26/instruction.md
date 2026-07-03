You are an AI assistant helping a computational physics researcher build a reproducible simulation pipeline to analyze the numerical convergence of a 1D Poisson equation solver. 

The physical system is modeled by the 1D Poisson equation:
d²u/dx² = -π² * sin(π * x)  for x ∈ [0, 1]
With Dirichlet boundary conditions: u(0) = 0, u(1) = 0.
The analytical solution to this equation is exactly: u(x) = sin(π * x).

Your objective is to complete a pipeline that performs mesh refinement, solves the system using the Thomas algorithm, measures the convergence rate, and visualizes the results.

Please complete the following steps in `/home/user`:

**Phase 1: Numerical Solver in C**
Write a C program named `/home/user/poisson1d.c` that solves this boundary value problem using the finite difference method.
1. It must accept exactly one command-line argument: `N`, the number of *internal* grid points.
2. The domain [0, 1] should be divided into `N+1` equal intervals of width `h = 1.0 / (N + 1)`.
3. Discretize the equation using the standard second-order central difference scheme: (u_{i-1} - 2u_i + u_{i+1}) / h² = -π² * sin(π * x_i).
4. Solve the resulting tridiagonal linear system using the Thomas algorithm.
5. Compute the discrete L2 norm of the error against the analytical solution:
   L2_error = sqrt( h * sum_{i=1}^{N} (u_i - u_exact(x_i))^2 )
6. The program must write the spatial coordinates, numerical solutions, and exact solutions to a tab-separated text file named `/home/user/solution_<N>.dat`. The columns should be `x`, `u_num`, `u_exact`. Do not include boundary points.
7. The program must print a single line to standard output in exactly this format:
   `N=<N>, h=<h>, error=<error>`
   Print `h` and `error` as floats with exactly 6 decimal places (e.g., `%.6f`).

**Phase 2: Reproducible Pipeline**
Create a bash script named `/home/user/pipeline.sh` that automates the mesh refinement study.
1. The script must compile `poisson1d.c` into an executable named `poisson1d` using `gcc` with the `-lm` flag.
2. It must run the executable for the following values of `N`: 9, 19, 39, 79, 159.
3. It must capture the standard output of all runs and append it sequentially to `/home/user/convergence.log`.
4. Make sure the script has execution permissions. Run the script once you have created it.

**Phase 3: Visualization**
Create a Python script named `/home/user/plot.py` to visualize the experimental data. 
1. Use `matplotlib` and `numpy`.
2. The script must read `/home/user/convergence.log` and plot the `error` against `h` on a log-log scale. Save this plot to `/home/user/convergence.png`.
3. The script must read `/home/user/solution_159.dat` and plot both the numerical and exact solutions against `x`. Save this plot to `/home/user/solution.png`.
4. Execute `plot.py` so the PNG files are generated.

Ensure that by the end of your interactions, `convergence.log`, `solution.png`, and `convergence.png` exist and are strictly formatted as requested.