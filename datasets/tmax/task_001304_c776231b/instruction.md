You are a performance engineer analyzing latency profiles for a distributed microservice. The application logs latencies, but the data is noisy and mixed with different request types. Your task is to extract the relevant data, fit a custom probabilistic model to the latency distribution using MCMC, and evaluate the fit.

Phase 1: Observational Data Reshaping
You have been provided with a raw log file at `/home/user/raw_latency.log`.
1. Use shell commands (e.g., `grep`, `awk`, `sed`) to extract latency values for successful requests.
2. Filter criteria: `Status: 200` AND `Endpoint: /api/v1/data`.
3. Extract only the numerical value of the latency (e.g., from `Latency: 45.2ms` extract `45.2`).
4. Save these filtered numerical values to `/home/user/clean_latency.csv`, with one value per line.

Phase 2: MCMC Sampling and Posterior Estimation
The latency data comes from two distinct underlying operations (e.g., cache hits and cache misses), meaning it follows a 2-component Gaussian Mixture Model (GMM). 
Assume the following is known:
- Component 1 (Cache hit): Weight $w_1 = 0.7$, Standard Deviation $\sigma_1 = 5.0$
- Component 2 (Cache miss): Weight $w_2 = 0.3$, Standard Deviation $\sigma_2 = 10.0$

Write a Python script `/home/user/fit_mcmc.py` that implements a Metropolis-Hastings MCMC algorithm from scratch to estimate the posterior means $\mu_1$ and $\mu_2$ based on your cleaned data.
- **Priors**: $\mu_1 \sim \text{Uniform}(0, 50)$ and $\mu_2 \sim \text{Uniform}(50, 150)$.
- **Likelihood**: $\prod_{i} [0.7 \cdot \mathcal{N}(x_i | \mu_1, 5^2) + 0.3 \cdot \mathcal{N}(x_i | \mu_2, 10^2)]$
- **Proposal Distribution**: Gaussian centered at the current state with standard deviation $2.0$ for both parameters. Sample new proposals independently: $\mu_1' \sim \mathcal{N}(\mu_1, 2.0^2)$ and $\mu_2' \sim \mathcal{N}(\mu_2, 2.0^2)$.
- **Initialization**: Start the chain at $\mu_1 = 25.0, \mu_2 = 100.0$.
- **Convergence/Burn-in**: Run the chain for 5,000 total iterations. Discard the first 1,000 iterations as burn-in.
- **Estimate**: Calculate the expected value (mean) of the remaining 4,000 samples for both $\mu_1$ and $\mu_2$.

Phase 3: Density Estimation and Distribution Distance
In the same Python script, generate a large theoretical sample to compare with your empirical data:
1. Generate 10,000 synthetic latency values from the GMM using your estimated posterior means ($\mu_1$ and $\mu_2$) and the known weights and standard deviations.
2. Calculate the 1D Wasserstein distance between the empirical cleaned data (`clean_latency.csv`) and your 10,000 synthetic samples. You may use `scipy.stats.wasserstein_distance`.

Phase 4: Output
Save your final results to a JSON file at `/home/user/profiling_results.json` with the following exact keys:
- `"mu1"`: (float) Estimated posterior mean for component 1.
- `"mu2"`: (float) Estimated posterior mean for component 2.
- `"wasserstein_distance"`: (float) The calculated distance metric.
- `"n_samples"`: (int) The number of data points extracted into `clean_latency.csv`.

Run your script to produce the output file.