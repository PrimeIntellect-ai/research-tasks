I am developing a finite difference solver in Rust for a steady-state diffusion PDE with Neumann boundary conditions. The discretization results in a linear system of the form $Ax = b$. 

Because of the boundary conditions, the system is purely conservative, meaning the coefficient matrix $A$ is singular (it has a rank deficiency and a null space). The current code in `/home/user/stiff_ode` attempts to solve this using a standard LU decomposition-based linear solver (`A.solve(&b)`), which panics or produces extreme floating-point garbage due to the near-singular condition.

Your task is to fix the numerical solver by modifying the Rust project:
1. Navigate to `/home/user/stiff_ode`.
2. Modify `src/main.rs` to replace the LU-based `.solve()` method with a Truncated Singular Value Decomposition (SVD) pseudo-inverse solver.
3. Compute the SVD of $A = U \Sigma V^T$. 
4. Calculate the pseudo-inverse by inverting the singular values in $\Sigma$. To ensure stability, truncate the SVD by discarding (setting to zero) any singular values smaller than the threshold $\epsilon = 10^{-5}$.
5. Reconstruct the solution $x = V \Sigma^{+} U^T b$.
6. Format the resulting 1D solution array as a single-line comma-separated string, with each value formatted to exactly 4 decimal places (e.g., `1.2345,0.0000,-1.2345`).
7. Save this exact string into `/home/user/stiff_ode/solution.txt`.

The matrices $A$ and $b$ are already parsed from `matrix_A.txt` and `vector_b.txt` in the provided `src/main.rs`. Do not alter the input files or the file-reading logic. Ensure your modified code compiles and runs successfully using `cargo run`.