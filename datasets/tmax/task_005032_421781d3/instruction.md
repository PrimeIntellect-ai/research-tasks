You are acting as a data scientist modeling the conformational dynamics of a simple peptide. We are using a 1D Langevin dynamics simulation written in Rust to generate a probability distribution of the peptide's position, and we need to fit/compare this against experimental target data.

Currently, the numerical integrator in our Rust codebase diverges because of a flawed step-size adaptation algorithm. The error shoots up, and the resulting distribution is completely wrong. 

Your task is to fix the integrator, implement a distribution distance metric, verify convergence, and visualize the results.

Here are your specific objectives:

1. **Fix the Integrator Bug**: 
   The Rust project is located at `/home/user/langevin_fit`. Look at `src/integrator.rs`. The `adaptive_step` function is supposed to adjust the time-step `dt` based on the local error `err` and a `tolerance`. 
   The standard formula for the new step size should be: `new_dt = dt * (tolerance / err).sqrt()`.
   However, the current implementation has a bug causing it to diverge when the error is large. Find and fix this bug.

2. **Extract Initial State**:
   The simulation needs an initial starting position. Modify `src/main.rs` to parse the provided PDB file at `/home/user/data/init.pdb`. Extract the `X` coordinate of the *first* atom listed in the file, and use it as the `initial_x` variable for the simulation.

3. **Implement KL Divergence**:
   In `src/main.rs`, implement the function `calculate_kl_divergence(p: &[f64], q: &[f64]) -> f64`. 
   It should calculate the Kullback-Leibler divergence: Σ p[i] * ln(p[i] / q[i]).
   *Note: To avoid log(0) or division by zero, add `1e-9` to both p[i] and q[i] before doing the division and log operations.*

4. **Output Logging**:
   When you run the fixed program (`cargo run`), it will generate a `simulated.csv` file. The program should also calculate the KL divergence between the simulated distribution and the target distribution (`/home/user/data/target.csv`).
   Write the final calculated KL divergence as a single floating-point number to `/home/user/kl_result.txt`.

5. **Regression Testing**:
   Create a regression test in `tests/integration_test.rs` that runs the simulation (you can extract the simulation logic into a reusable function or just test the math) and asserts that the KL divergence is less than `0.05`. Ensure `cargo test` passes.

6. **Visualization**:
   Write a Python script at `/home/user/plot_dist.py` that reads `simulated.csv` and `/home/user/data/target.csv`. Both CSVs contain a single column of probability values representing bins. Plot both distributions on the same line graph (Simulated vs Target) and save the figure to `/home/user/distribution.png`.

Requirements:
- Your Rust code must compile and run successfully using `cargo run`.
- Your Python script must generate `distribution.png` successfully.
- `/home/user/kl_result.txt` must contain only the KL divergence value.