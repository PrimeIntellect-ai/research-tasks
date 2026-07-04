You are an expert scientific computing assistant. I am researching localized heat generation and need to solve a 1D steady-state heat equation (a Poisson equation) of the form:

$u''(x) = f(x)$

on the domain $x \in [0, 1]$ with Dirichlet boundary conditions $u(0) = 0$ and $u(1) = 0$.

However, the source term $f(x)$ is heavily localized and provided to us only as a compiled, black-box Linux binary located at `/app/eval_source`. The binary is stripped.
Usage: `/app/eval_source <x1> <x2> ...` 
It will print the corresponding $f(x_i)$ values separated by spaces. The binary handles up to 1000 points per call.

Because $f(x)$ contains extremely sharp, highly localized features, a uniform grid requires thousands of points to capture the spike without numerical instability or smearing. 

Your task is to write a Go program `/home/user/solver.go` that uses **adaptive mesh refinement (AMR)** to solve the boundary value problem using a non-uniform finite difference method.

Your Go program must:
1. Start with a coarse grid (e.g., 5-10 points).
2. Iteratively solve the tridiagonal system for the non-uniform mesh.
3. Evaluate an error indicator (e.g., curvature, gradient, or Richardson extrapolation differences) to identify elements that need refinement.
4. Add new grid points only in the problematic regions and repeat until the solution converges.
5. Save the final mesh and solution to `/home/user/solution.txt` where each line is formatted exactly as `<x_i> <u_i>`, space-separated, and sorted in ascending order of $x$. Include the boundary points.

Constraints & Evaluation:
- We will evaluate the maximum absolute error of your solution (using linear interpolation between your grid points) against a high-fidelity ground truth.
- The maximum absolute error must be strictly **less than 0.005**.
- To test your mesh refinement logic, the automated verifier will count the number of grid points in `/home/user/solution.txt`. You must achieve the required accuracy using **fewer than 150 grid points**.
- You may only use standard Go libraries. 

Please perform any terminal interactions necessary to explore the binary, write your Go code, run the solver, and produce the optimal `/home/user/solution.txt`.