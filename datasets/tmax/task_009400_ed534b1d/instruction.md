You are a bioinformatics analyst tasked with estimating the GC-content distribution parameters of a synthetic viral genome using Bayesian inference. The observed GC-content fractions across 200 genomic windows have been extracted and saved as a numpy array.

Your objective is to implement a reproducible Markov Chain Monte Carlo (MCMC) pipeline from scratch to estimate the posterior distributions of the mean ($\mu$) and standard deviation ($\sigma$) of the GC content, assuming the data follows a Normal distribution. You must also implement a regression test using `pytest` to ensure your pipeline is reproducible.

**Data:**
The data is located at `/home/user/gc_data.npy`. It is a 1D numpy array of floats between 0 and 1.

**Model & Priors:**
- Likelihood: $X \sim \mathcal{N}(\mu, \sigma^2)$
- Prior for $\mu$: $\text{Uniform}(0, 1)$
- Prior for $\sigma$: $\text{Uniform}(0.01, 0.5)$
- The log-prior should be 0 if parameters are within bounds, and $-\infty$ otherwise.

**Task Requirements:**
1. **Implementation (`/home/user/mcmc_gc.py`):**
   Write a Python script containing a function `run_mcmc(data_path, iterations=10000, seed=42)`.
   - Implement the Metropolis-Hastings algorithm.
   - Start at $\mu_{0} = 0.5$, $\sigma_{0} = 0.1$.
   - Proposal distribution: At each step, draw proposals independently: $\mu_{prop} \sim \mathcal{N}(\mu_{curr}, 0.05^2)$ and $\sigma_{prop} \sim \mathcal{N}(\sigma_{curr}, 0.05^2)$.
   - Use `numpy.random` with the provided `seed` at the very beginning of the function for reproducibility.
   - Run for `iterations` steps. Discard the first 50% of the steps as burn-in.
   - Return the posterior samples of $\mu$ and $\sigma$ (arrays of length `iterations / 2`).

2. **Distance Metric Calculation:**
   In the same script, create a function `evaluate_posterior(mu_samples)` that calculates the 1st Wasserstein distance between the posterior samples of $\mu$ and a reference uniform distribution $U(0.4, 0.5)$.
   - Generate the reference uniform samples using `np.random.uniform(0.4, 0.5, size=len(mu_samples))` (set a fixed seed of 99 before this draw).
   - Use `scipy.stats.wasserstein_distance`.

3. **Execution & Logging:**
   Write a script `/home/user/run_pipeline.sh` that installs any necessary packages (`numpy`, `scipy`, `pytest`), runs your MCMC code on `/home/user/gc_data.npy` (with 10,000 iterations and seed 42), and saves the calculated Wasserstein distance to `/home/user/results.txt`. The text file should contain only the float value rounded to 4 decimal places.

4. **Regression Test (`/home/user/test_mcmc.py`):**
   Write a `pytest` test script that imports your functions, runs the MCMC for 2000 iterations (seed 42), and asserts that the Wasserstein distance is strictly less than 0.20.

All code must be written in Python. You are free to run the shell script and tests to verify your implementation before concluding.