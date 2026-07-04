I need you to help me build an MCMC sampling web service in Rust to estimate the posterior distribution of a parameter `mu` for my simulation data. 

There is a compiled binary located at `/app/score_oracle`. I lost the source code, but it computes the log-likelihood of my observational data given a mutation rate `mu`. 
If you run `/app/score_oracle <mu>` (where `<mu>` is a floating-point number), it prints the log-likelihood to stdout.

Your task is to write a Rust HTTP server that exposes an MCMC sampler to estimate the posterior mean of `mu`.

Here are the requirements:
1. **Server Setup**: Create a Rust project and start an HTTP server listening exactly on `127.0.0.1:9090`.
2. **Endpoint**: Provide a `POST /run_mcmc` endpoint. It should accept a JSON payload like:
   `{"iterations": 10000, "init_mu": 0.5}`
3. **MCMC Algorithm**: 
   - Implement the Metropolis-Hastings algorithm.
   - **Prior**: `mu` has a Uniform(0.0, 10.0) prior. (Log-prior is 0 if within bounds, else -infinity).
   - **Proposal**: Draw a candidate `mu_new` from a Normal distribution centered at the current `mu` with a standard deviation of `0.1`.
   - **Likelihood**: Call the `/app/score_oracle` binary to get the log-likelihood for a given `mu`. To ensure numerical stability, perform all acceptance ratio calculations in log-space.
   - **Burn-in**: Discard the first 20% of the `iterations` before calculating the posterior mean.
4. **Response**: The endpoint should return a JSON response with the posterior mean of `mu` calculated from the retained samples:
   `{"mean": 1.234}` (replace 1.234 with the actual calculated mean).

You can use any Rust framework (e.g., `axum`, `hyper`, `actix-web`, `warp`) and crates (e.g., `rand`, `reqwest`, `serde`). Just ensure the server stays running and listening on `127.0.0.1:9090` so that I can send HTTP requests to it. You should start the server in the background (or foreground if you detach) so that the verifier can test it.

Please write the code, compile it, and run the server.