You are a bioinformatics analyst studying the mutation rate across different genomic windows. You have been provided with an HDF5 file at `/home/user/mutation_counts.h5` which contains a single dataset named `counts`. This dataset contains integers representing the number of mutations observed in various sequence windows.

Your task is to estimate the posterior distribution of the mutation rate ($\lambda$) using both Markov Chain Monte Carlo (MCMC) sampling and analytical validation. 

Assume the following Bayesian model:
1. **Likelihood**: The mutation counts $X_i$ follow a Poisson distribution: $X_i \sim \text{Poisson}(\lambda)$.
2. **Prior**: The mutation rate $\lambda$ follows a Gamma prior distribution: $\lambda \sim \text{Gamma}(\alpha_{prior}=2.0, \beta_{prior}=1.0)$, where $\alpha$ is the shape parameter and $\beta$ is the rate (inverse scale) parameter.

Perform the following:
1. Read the mutation counts from the HDF5 file.
2. Implement a simple MCMC sampler (e.g., Metropolis-Hastings) in Python to draw 10,000 samples from the posterior distribution of $\lambda$ (after discarding an appropriate burn-in, e.g., 1,000 samples). Calculate the mean of these MCMC posterior samples.
3. Validate your MCMC results by calculating the **exact analytical** posterior mean and variance of $\lambda$ (exploiting the Gamma-Poisson conjugacy).
4. Save your results to a JSON file at `/home/user/posterior_results.json` with the following exact keys and numeric values (floats):
   - `"analytical_mean"`: The exact analytical posterior mean of $\lambda$.
   - `"analytical_variance"`: The exact analytical posterior variance of $\lambda$.
   - `"mcmc_mean"`: The mean of your MCMC samples.

Ensure your MCMC mean is reasonably converged (it should be very close to the analytical mean).