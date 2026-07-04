You are acting as a computational statistics assistant for a researcher analyzing physics simulation results. 

The researcher has a Rust project located at `/home/user/sim_analysis` that reads simulation data from an HDF5 file (`/home/user/data/simulation.h5`) and performs a multiple linear regression to find the coefficients. 

Currently, the Rust program uses the naive Normal Equations approach ($\beta = (X^T X)^{-1} X^T y$) using standard matrix inversion. Unfortunately, the feature matrix $X$ is near-singular (it contains highly correlated features/multicollinearity due to the nature of the simulation). Because of this numerical instability, the standard matrix inversion either fails completely or produces wildly inaccurate, exploding coefficients, causing our regression test suite to fail.

Your task is to fix the Rust program to be numerically stable. 
Specifically, you must:
1. Modify `/home/user/sim_analysis/src/main.rs` to implement Ridge Regression (Tikhonov regularization) instead of standard OLS.
2. Use a regularization parameter (lambda/alpha) of exactly `0.1`. The Ridge formula is $\beta = (X^T X + \lambda I)^{-1} X^T y$, where $I$ is the identity matrix of appropriate dimensions.
3. The program must read the `X` (2D array, shape N x M) and `y` (1D array, shape N) datasets from the root group of the HDF5 file. 
4. Calculate the Ridge regression coefficients.
5. Save the resulting coefficient vector to `/home/user/solution.txt`, with exactly one coefficient per line, formatted to exactly 6 decimal places (e.g., `1.234567`).

Constraints & Environment:
* The Rust project is already initialized with `ndarray`, `ndarray-linalg`, and `hdf5` crates in its `Cargo.toml`. You may use `ndarray_linalg::Solve` or `ndarray_linalg::Inverse` as needed.
* You do not need to install system dependencies; assume `libopenblas-dev` and `libhdf5-dev` are already installed.
* Make sure your code compiles with `cargo build --release` and runs without panicking.
* Do not modify the HDF5 file.