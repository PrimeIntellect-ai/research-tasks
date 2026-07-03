You are acting as a performance engineer who needs to profile and analyze application latency data from two different system configurations. 

I have two datasets of response times (in milliseconds) collected from our load tests:
- `/home/user/latency_a.txt` (Configuration A)
- `/home/user/latency_b.txt` (Configuration B)

I need you to create a Jupyter Notebook at `/home/user/profile_analysis.ipynb` that performs a statistical analysis of this data, and then execute it so the outputs are generated.

Your notebook must perform the following tasks and output a file named `/home/user/results.json`:

1. **Bootstrap Confidence Intervals:**
   Calculate the 95% Bootstrap confidence interval for the difference in the *medians* (Median of B minus Median of A). 
   - Use exactly 10,000 bootstrap resamples.
   - Use `numpy.random.seed(42)` immediately before running your bootstrap loop/function to ensure reproducibility.
   - Store the lower and upper bounds of the 95% CI (using the 2.5th and 97.5th percentiles) in `results.json` under the keys `bootstrap_ci_lower` and `bootstrap_ci_upper`.

2. **MCMC Posterior Estimation:**
   Assume the latency data for each configuration follows an Exponential distribution, where the probability density is $f(x|\mu) = \frac{1}{\mu} e^{-x/\mu}$ and $\mu$ is the mean latency.
   We want to estimate the posterior distribution of $\mu_A$ and $\mu_B$.
   - Prior: Assume a uniform prior for $\mu$ between 0 and 200.
   - Implement a simple Metropolis-Hastings MCMC sampler from scratch in numpy.
   - Proposal distribution: Normal distribution centered on the current $\mu$ with standard deviation $\sigma = 2.0$.
   - Starting value: $\mu_{init} = 50.0$.
   - Iterations: 10,000 total steps. Discard the first 2,000 steps as burn-in.
   - Use `numpy.random.seed(100)` immediately before running the MCMC sampler for Config A, and `numpy.random.seed(200)` before running the MCMC sampler for Config B.
   - Calculate the mean of the posterior samples (after burn-in) for $\mu_A$ and $\mu_B$.
   - Store these values in `results.json` under the keys `mcmc_mu_a` and `mcmc_mu_b`.

3. **Experimental Data Visualization:**
   Create a single matplotlib figure with two subplots (1 row, 2 columns).
   - Left subplot: A histogram of the bootstrap distribution of the median differences.
   - Right subplot: Overlaid density plots (or histograms) of the accepted MCMC posterior samples for $\mu_A$ and $\mu_B$.
   - Save the plot to `/home/user/posterior_plot.png`.

4. **Notebook Orchestration:**
   Write the code into `/home/user/profile_analysis.ipynb`. You must then execute the notebook in the terminal (e.g., using `jupyter nbconvert --execute --inplace /home/user/profile_analysis.ipynb` or `papermill`) so that the outputs (`results.json` and `posterior_plot.png`) are written to disk.

Ensure your `results.json` looks exactly like this:
```json
{
  "bootstrap_ci_lower": -5.123,
  "bootstrap_ci_upper": 2.456,
  "mcmc_mu_a": 45.123,
  "mcmc_mu_b": 42.456
}
```
(Note: the values above are examples, you must compute the real ones).