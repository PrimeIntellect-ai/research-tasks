You are a bioinformatics analyst tasked with replacing a legacy pipeline that estimates the GC content distribution of DNA sequencing reads. The old pipeline is slow, but we need to ensure our new statistical models remain backwards-compatible with its outputs.

Your objective is to set up a scientific environment, implement a new robust script for density estimation and MCMC sampling of GC content, and write a regression test suite against the legacy data.

Step 1: Environment Management
- Create a Python virtual environment at `/home/user/bio_env`.
- Install `biopython`, `numpy`, `scipy`, `emcee`, and `pytest` in this environment.

Step 2: Data Processing & Density Estimation
- Read the sequences from `/home/user/data/reads.fasta` (already present on the system).
- Calculate the GC content (percentage, 0.0 to 100.0) for each sequence. GC content is `(Count(G) + Count(C)) / Length * 100`.
- Write a Python script `/home/user/pipeline/gc_model.py` that uses `scipy.stats.gaussian_kde` (with default Scott's rule) on the sequence GC percentages. Evaluate this KDE over 1000 evenly spaced points between 0.0 and 100.0 to find the GC percentage that maximizes the density (`kde_peak`).

Step 3: MCMC Posterior Estimation
- In the same script (`gc_model.py`), use `emcee` to fit a Normal distribution to the observed GC percentages.
- Define a log-likelihood function for a Normal distribution.
- Define uniform log-priors: $\mu \in [0, 100]$ and $\sigma \in [0.1, 50]$. Return $-\infty$ outside these bounds.
- Set `np.random.seed(42)` immediately before initializing the MCMC sampler to ensure reproducibility.
- Run an `emcee.EnsembleSampler` with 10 walkers, 2 dimensions ($\mu$ and $\sigma$). Initialize the walkers with random uniform values within the prior bounds (using `np.random.uniform` with bounds [40, 60] for $\mu$ and [1, 10] for $\sigma$).
- Run the sampler for 1000 steps. Discard the first 200 steps as burn-in.
- Calculate the mean of the flattened posterior samples for $\mu$ (`mcmc_mu`) and $\sigma$ (`mcmc_sigma`).
- Save the results to `/home/user/pipeline/results.json` as a JSON object:
  ```json
  {
    "kde_peak": <float>,
    "mcmc_mu": <float>,
    "mcmc_sigma": <float>
  }
  ```

Step 4: Scientific Code Regression Testing
- There is a legacy output file at `/home/user/data/legacy_results.json`.
- Write a `pytest` test file at `/home/user/pipeline/test_regression.py`.
- The test file should read both `legacy_results.json` and your newly generated `results.json`.
- Write test functions asserting that `mcmc_mu` and `mcmc_sigma` from your new model are within an absolute tolerance of `0.5` compared to the legacy results.
- Run the test suite and ensure it passes.

Make sure to execute your script to generate `/home/user/pipeline/results.json` and ensure your regression tests pass successfully before finishing.