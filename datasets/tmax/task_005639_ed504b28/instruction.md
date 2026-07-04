You are an AI assistant helping a researcher run numerical simulations and perform statistical analysis on the results.

The researcher is studying the 2D Laplace equation $\nabla^2 u = 0$ on the unit square domain $[0,1] \times [0,1]$. They have a known analytical solution: 
$u_{ana}(x,y) = \sin(\pi x) \sinh(\pi y)$

Your task is to write and execute a Python script that solves this equation numerically, performs a convergence study, and conducts a statistical hypothesis test on the errors.

Specific requirements:
1. Write a Python script `/home/user/solve.py`.
2. Use a standard 5-point finite difference stencil to approximate the Laplacian. 
3. Apply Dirichlet boundary conditions evaluated exactly from the analytical solution $u_{ana}(x,y)$.
4. Formulate the problem as a linear system $A u = b$ for the interior points and solve it directly (e.g., using `scipy.sparse.linalg.spsolve`).
5. Perform mesh refinement by solving the problem on grids with $N \times N$ cells (meaning $(N+1) \times (N+1)$ grid points), for $N \in \{10, 20, 40\}$.
6. For each $N$, calculate the exact numerical approximation $u_{num}$ at all grid points. Compute the maximum absolute error $E_N = \max |u_{num} - u_{ana}|$ over all $(N+1) \times (N+1)$ points.
7. Compute the empirical convergence orders: $p_1 = \log_2(E_{10} / E_{20})$ and $p_2 = \log_2(E_{20} / E_{40})$.
8. For the $N=40$ grid, compute the individual error at every grid point: $e_{i,j} = u_{num}(x_i, y_j) - u_{ana}(x_i, y_j)$. Flatten this into a 1D array.
9. Perform a Shapiro-Wilk test on this 1D error array (using `scipy.stats.shapiro`) to test the null hypothesis that the spatial distribution of the numerical errors follows a normal distribution.
10. Save your results to a JSON file located at `/home/user/results.json` containing exactly these keys:
    - `"E_10"`: Float, max absolute error for N=10
    - `"E_20"`: Float, max absolute error for N=20
    - `"E_40"`: Float, max absolute error for N=40
    - `"p_1"`: Float, convergence order from N=10 to 20
    - `"p_2"`: Float, convergence order from N=20 to 40
    - `"shapiro_statistic"`: Float, the test statistic from the Shapiro-Wilk test on the N=40 errors
    - `"shapiro_p_value"`: Float, the p-value from the Shapiro-Wilk test on the N=40 errors

Format requirements for `/home/user/results.json`:
- All float values must be rounded to exactly 6 decimal places.

You have full access to a terminal. You may need to install standard scientific libraries (e.g., `numpy`, `scipy`) if they are not already present.