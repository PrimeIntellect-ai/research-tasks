You are assisting a computational physics researcher analyzing statistical error propagation in a 1D steady-state thermal model. 

The heat equation in 1D at steady state is modeled by the Poisson equation:
$$-\frac{d^2 u}{dx^2} = S(x)$$
defined on the domain $x \in (0, 1)$ with Dirichlet boundary conditions $u(0) = 0$ and $u(1) = 0$.

We discretize this domain using standard second-order central finite differences on a uniform grid with $N$ internal nodes. The grid spacing is $h = 1/(N+1)$. This forms a linear system $A u = S_{discrete}$.

The source term $S(x)$ contains independent statistical noise at each discrete internal node. Specifically, the discretized source vector $S$ has a covariance matrix $\Sigma_S = \sigma^2 I$, where $\sigma = 0.1$ and $I$ is the $N \times N$ identity matrix.

Due to linear error propagation, the covariance matrix of the temperature profile $u$ is given by:
$$\Sigma_u = A^{-1} \Sigma_S A^{-T}$$

Your task is to calculate the statistical variance of the temperature exactly at the midpoint of the domain ($x=0.5$). 

Please perform the following steps:
1. Initialize a Go module named `thermal` in `/home/user/thermal`.
2. Write a Go program `/home/user/thermal/variance_solver.go` that takes a single integer argument `N` (the number of internal nodes, guaranteed to be an odd number so $x=0.5$ is always exactly on a node).
3. The program must construct the discretized finite difference matrix $A$, perform the necessary linear algebra to compute the exact variance of $u$ at the midpoint node, and print ONLY the computed variance to standard output in scientific e-notation with exactly 6 decimal places (e.g., `1.234567e-05`). You may use external Go libraries (like gonum) if you initialize and fetch them properly.
4. To perform a mesh refinement study, write a bash script `/home/user/run_meshes.sh` that builds the Go program and runs it for $N = 3, 9, 19, 49$, and $99$.
5. The bash script must append the results to `/home/user/results.log` in the exact format: `N=<N>, Var=<Variance>`.

Ensure your bash script is executable and run it to produce the final `results.log` file.