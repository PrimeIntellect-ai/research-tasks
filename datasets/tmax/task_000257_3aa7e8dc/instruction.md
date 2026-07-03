You are a data scientist tasked with fitting a sequential kinetic model to time-resolved transient absorption spectroscopy data. The chemical reaction follows a simple linear chain: 
A --(k1)--> B --(k2)--> C --(k3)--> D

You need to write a C++ program that determines the rate constants (k1, k2, k3) that best fit a given spectroscopic dataset. Since the pure spectra of the intermediate species are unknown, you must use a Variable Projection (VARPRO) approach: for a given set of rate constants (k1, k2, k3), you will solve the ODEs to find the concentration matrix `C(t)`, and then use matrix decomposition (SVD or QR) to find the conditionally optimal spectral matrix `S` that minimizes the Frobenius norm of `Data - C * S`. 

Your goal is to implement a command-line tool at `/home/user/fit_model` that takes two arguments: an input binary file path and an output binary file path.
It should find the optimal `k1, k2, k3` (minimizing the residual sum of squares) using a simple grid search or gradient descent (the exact optimization method is up to you, but it must be deterministic and converge to the global minimum within the domain `0.1 <= k <= 10.0`).

Input Binary Format (Little-Endian):
- `N` (uint32_t): Number of time points.
- `M` (uint32_t): Number of wavelengths.
- `T` (N * double): Array of time points.
- `Data` (N * M * double): The flattened 2D data matrix (row-major, N rows by M columns).

Output Binary Format (Little-Endian):
- 3 doubles representing the best-fit rate constants: `k1`, `k2`, `k3`.

To solve the ODEs, you MUST use the vendored C++ library located at `/app/fast_odesolver-1.2.0/`. However, the previous engineer left it in a broken state; it currently fails to compile due to a configuration error in its build system. You will need to diagnose and fix the perturbation in `/app/fast_odesolver-1.2.0/` before you can link it against your `fit_model` code.

Write the C++ application, fix the vendored library, and ensure your program compiles and perfectly matches the expected kinetic extraction behavior. Use standard C++17 or C++20. Eigen3 is available on the system for matrix operations (`#include <Eigen/Dense>`).