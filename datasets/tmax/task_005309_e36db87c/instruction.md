I am a researcher running statistical simulations, and I need to build a simple Metropolis-Hastings MCMC sampler in Rust to estimate the mean of a normal distribution. I also need to ensure the sampler is robust by writing a regression test that validates its output against the analytical posterior mean.

Please complete the following steps:

1. Create a new Rust library project at `/home/user/mcmc_stat`.
2. Add the `rand` and `rand_distr` crates to your `Cargo.toml`.
3. In `src/lib.rs`, implement the following function:
   `pub fn metropolis_hastings(data: &[f64], iterations: usize, seed: u64) -> f64`
   
   **MCMC Specifications:**
   * **Likelihood:** The data is assumed to be drawn from a Normal distribution with an unknown mean ($\mu$) and a known standard deviation ($\sigma = 1.0$).
   * **Prior:** Assume a uniform (flat) prior for $\mu$. 
   * **Proposal Distribution:** Normal distribution centered at the current $\mu$ with a standard deviation of `0.5`.
   * **Initialization:** Start the chain at $\mu_0 = 0.0$.
   * **Burn-in:** Discard the first 10% of the specified `iterations`.
   * **Return Value:** The average of the $\mu$ samples *after* the burn-in period.
   * **Randomness:** Use the `StdRng::seed_from_u64(seed)` from the `rand` crate to ensure reproducibility.

4. **Analytical Solution Validation & Regression Testing:**
   In the same `src/lib.rs` file, write a test module containing a test named `test_mcmc_analytical_validation`.
   * **Test Data:** `[1.2, 2.5, 3.1, 4.0, 2.8]`
   * **Test Parameters:** 50,000 iterations, seed = `42`.
   * **Validation:** For a flat prior and known $\sigma$, the analytical posterior mean of $\mu$ is exactly equal to the sample mean of the data. Calculate this sample mean analytically in the test. Assert that the absolute difference between your MCMC estimation and the analytical sample mean is less than `0.1`.

5. Run the test and save the output. Create a bash script at `/home/user/run_test.sh` that changes into the `/home/user/mcmc_stat` directory and runs `cargo test`, redirecting both stdout and stderr to `/home/user/test_results.txt`. Make the script executable and run it so the log file is generated.