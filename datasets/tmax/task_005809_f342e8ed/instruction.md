You are a performance engineer working on a bio-molecular simulation tool. Recently, the development team parallelized the pairwise energy calculation in `/home/user/src/energy_sim.cpp` using OpenMP. However, scientists are complaining that the simulation produces slightly different results on every run, failing their reproducibility tests.

Your investigation reveals that the non-reproducibility is due to the floating-point reduction order. The code uses an atomic add on a `float` accumulator inside a parallel loop, which means the additions happen in a non-deterministic order. Because floating-point addition is not associative, this causes run-to-run variance.

Your task has 4 phases:

1. **Fix the Reduction Bug:**
   Edit `/home/user/src/energy_sim.cpp`. Fix the `compute_total_energy` function by changing the accumulator to a `double` and using a proper OpenMP `reduction` clause instead of `#pragma omp atomic`. This guarantees deterministic, high-precision accumulation regardless of thread scheduling.

2. **Implement Curve Fitting (using Matrix Decomposition):**
   The scientists also left a placeholder function `fit_energy_curve(const std::vector<double>& x, const std::vector<double>& y)` in the same file. You must implement this function to perform a quadratic polynomial regression ($y = c_0 + c_1 x + c_2 x^2$) using matrix decomposition (e.g., solving the normal equations via Cholesky, LU, or SVD). 
   * Note: You may download and use the Eigen library (header-only) in `/home/user/eigen` and compile with `-I/home/user/eigen`. 

3. **Build and Run:**
   Compile the fixed code:
   `g++ -O3 -fopenmp -I/home/user/eigen /home/user/src/energy_sim.cpp -o /home/user/src/sim`
   Run the simulation 10 times. The simulation processes the PDB file at `/home/user/data/molecule.pdb`.

4. **Statistical Verification & Logging:**
   Write a small script or command to compute the variance of the "Total Energy" outputs across your 10 runs. 
   Create a file `/home/user/results/stat_log.txt` containing the exact line:
   `Variance: 0.0000` (since your fix should make it perfectly reproducible).
   
   The simulation also outputs the fitted coefficients for a set of energy samples. Append the output of the curve fit to `/home/user/results/fit_log.txt` in the exact format printed by the simulation:
   `Coeffs: c0, c1, c2` (formatted to 4 decimal places, e.g., `Coeffs: 1.2345, -0.1234, 0.5678`).

Ensure all files are placed in `/home/user/results/` which you must create.