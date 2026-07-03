You are a performance engineer tasked with profiling a recently deployed microservice. You have collected raw response times, but you suspect the latency distribution is actually a mixture of two distinct behaviors: normal fast responses, and a long tail of slow responses due to intermittent cache misses. 

Your objective is to fit a two-component Gaussian Mixture Model (GMM) to this latency data using custom optimization, and then quantify how well this model fits the empirical data using a distribution distance metric.

**Task Requirements:**

1. **Input Data**: The raw latency data is located at `/home/user/latencies.csv`. It has a single column named `latency_ms`.

2. **Analysis Script**: Create a Python script at `/home/user/profile_latencies.py` that performs the following steps:
   * **Custom Fitting via Optimization**: Define the probability density function (PDF) of a 2-component Gaussian mixture: 
     $P(x) = w \cdot N(x | \mu_1, \sigma_1) + (1-w) \cdot N(x | \mu_2, \sigma_2)$
     Use `scipy.optimize.minimize` with the **Nelder-Mead** algorithm to find the parameters $(w, \mu_1, \sigma_1, \mu_2, \sigma_2)$ that minimize the negative log-likelihood of the observed latencies. 
     Enforce sensible bounds or transformations to ensure $0.01 \le w \le 0.99$ and $\sigma_1, \sigma_2 \ge 0.1$.
   * **Distance Metric**: Generate 100,000 synthetic samples from your optimized 2-component GMM. Calculate the 1st Wasserstein distance between the empirical latency data and your synthetic samples using `scipy.stats.wasserstein_distance`.
   * **Formatting**: Ensure that component 1 represents the "fast" responses (lower mean) and component 2 represents the "slow" responses (higher mean). If your optimizer finds them swapped, reassign them so $\mu_1 < \mu_2$, and adjust $w$ accordingly (where $w$ is the weight of the $\mu_1$ component).

3. **Output**: Your script must execute successfully and output a JSON file to `/home/user/profiling_results.json` with the exact following keys and float values:
   * `"mu1"`: Mean of the fast component
   * `"sigma1"`: Standard deviation of the fast component
   * `"mu2"`: Mean of the slow component
   * `"sigma2"`: Standard deviation of the slow component
   * `"w1"`: Weight of the fast component
   * `"wasserstein_distance"`: The calculated distance metric

**Constraints**:
* Do NOT use `sklearn.mixture.GaussianMixture` or similar off-the-shelf GMM fitters. You must implement the negative log-likelihood function and optimize it directly.
* You may need to install necessary Python packages (e.g., `numpy`, `scipy`, `pandas`) using pip.
* Choose a reasonable initial guess for your optimization based on the data.