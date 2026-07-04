You are a data scientist working on fitting a physical model to experimental data of a damped harmonic oscillator. 

We have a Rust project located at `/home/user/oscillator_fit` that performs Metropolis-Hastings MCMC sampling to find the posterior distribution of the damping coefficient (`c`) and spring constant (`k`). The model relies on an adaptive step-size ODE integrator.

Currently, the pipeline is failing for two reasons:
1. **Diverging Integrator:** The numerical integrator in `src/integrator.rs` is diverging and failing its regression tests (`cargo test`). The step-size adaptation logic is completely backwards—it increases the step size when the error is too high, causing explosive divergence. You need to fix the logic so the step size halves when the error exceeds the tolerance, and doubles when it is well within the tolerance.
2. **Incomplete MCMC:** The Metropolis-Hastings acceptance logic in `src/mcmc.rs` is missing. You need to implement the standard acceptance criterion for log-likelihoods.

Your tasks:
1. Fix the bug in `/home/user/oscillator_fit/src/integrator.rs` so that `cargo test` passes.
2. Complete the MCMC step function in `/home/user/oscillator_fit/src/mcmc.rs`.
3. Run the project (`cargo run --release`). It is configured to read `data.csv`, run 5000 MCMC iterations, and write the posterior means to standard output, while also generating a plot.
4. Save the final posterior mean output to `/home/user/results.txt` exactly in the format: `c: <value>, k: <value>`.
5. Ensure the visualization script successfully writes the plot to `/home/user/fit.png`.

Do not modify the `main.rs` or `data.csv` files. Rely on `cargo test` to verify your integrator fix before running the full sampler.