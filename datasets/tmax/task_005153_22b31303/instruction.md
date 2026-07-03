You are a data scientist tasked with running a Monte Carlo simulation of a dynamic system. 

You are modeling a system described by the following Ordinary Differential Equation (ODE):
`dy/dt = -θ_0 * y + θ_1 * sin(θ_2 * t)`
with the initial condition `y(0) = 5.0`.

The parameters `θ = [θ_0, θ_1, θ_2]^T` are drawn from a multivariate normal distribution with mean `μ = [0.5, 1.0, 2.0]^T` and a covariance matrix `Σ`.

However, the provided covariance matrix `Σ` is near-singular (perfectly collinear), which will cause standard matrix factorization (like Cholesky decomposition) to fail. 

Your tasks:
1. Read the 3x3 covariance matrix from `/home/user/workspace/cov_matrix.txt`.
2. Regularize the covariance matrix by adding a small "jitter" or ridge of `1e-5` (0.00001) to each of the diagonal elements to make it positive definite. Let this be `Σ_reg`.
3. Compute the Cholesky decomposition `L` of `Σ_reg` (such that `L * L^T = Σ_reg`, where `L` is lower triangular).
4. Read 1000 standard normal samples `Z` from `/home/user/workspace/z_samples.txt`. Each row contains three standard normal values `[z_0, z_1, z_2]^T`.
5. For each of the 1000 samples, transform the standard normal vector `Z` into the parameter space using `θ = μ + L * Z`.
6. For each resulting parameter vector `θ`, solve the ODE from `t = 0.0` to `t = 2.0` using the forward Euler method with a time step of `dt = 0.01` (200 steps).
7. Calculate the average of the final state `y(2.0)` across all 1000 Monte Carlo simulations.
8. Write this single average value to `/home/user/workspace/result.txt`, formatted to exactly 4 decimal places (e.g., `3.1415`).

You must implement the logic in C++ (save it as `/home/user/workspace/mc_ode.cpp` and compile it). You may use standard C++ libraries, or install and use the Eigen3 library for matrix operations if you prefer.