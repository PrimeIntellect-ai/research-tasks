You are acting as a bioinformatics analyst. We are upgrading our sequence mutation analysis pipeline and need to perform a regression test on a newly implemented Markov Chain Monte Carlo (MCMC) module. 

We have a reference dataset of Single Nucleotide Polymorphism (SNP) counts observed over different exposure times. 
Your task is to write a script (in any language you choose, e.g., Python) that implements a Metropolis-Hastings MCMC sampler to estimate the posterior mean of the mutation rate ($\lambda$), and then compare your result against a verified reference value to ensure the new sampler works correctly.

**Model Specification:**
*   **Likelihood:** The number of SNPs ($y_i$) follows a Poisson distribution: $y_i \sim \text{Poisson}(\lambda \times t_i)$, where $t_i$ is the exposure time and $\lambda$ is the universal mutation rate.
*   **Prior:** $\lambda$ has a Uniform prior distribution between 0 and 10 (inclusive). $\lambda \sim \text{Uniform}(0, 10)$.

**MCMC Sampler Requirements:**
*   Algorithm: Standard Metropolis-Hastings.
*   Initial state: $\lambda_0 = 1.0$.
*   Proposal distribution: Normal distribution centered at the current $\lambda$ with standard deviation $\sigma = 0.5$.
*   Boundary conditions: If a proposed $\lambda$ falls outside the prior bounds [0, 10], the proposal must be rejected (prior probability is 0).
*   Total iterations: 50,000.
*   Burn-in: Discard the first 10,000 iterations. The posterior mean should be calculated from the remaining 40,000 samples.
*   Random Seed: Set your random number generator seed to `42` before starting the sampling loop.

**Input Files:**
1.  `/home/user/snp_counts.csv`: A CSV file containing the dataset. It has a header and two columns: `exposure_time` ($t_i$) and `snp_count` ($y_i$).
2.  `/home/user/reference.txt`: A text file containing the ground-truth posterior mean of $\lambda$ (a float) computed by our legacy, validated system.

**Output Requirements:**
You must perform the sampling, calculate the posterior mean of $\lambda$ from your post-burn-in samples, and compare it to the reference value. 

Create a regression test report at `/home/user/regression_report.json` with the following strict JSON format:
```json
{
  "computed_mean": 2.55, 
  "reference_mean": 2.62,
  "status": "PASS"
}
```
*   `computed_mean`: Your calculated posterior mean, rounded to exactly 2 decimal places.
*   `reference_mean`: The exact float value read from `/home/user/reference.txt`.
*   `status`: String `"PASS"` if the absolute difference between `computed_mean` and `reference_mean` is less than or equal to `0.05`. Otherwise, `"FAIL"`.

Do not use external MCMC libraries like PyMC or Stan; implement the Metropolis-Hastings algorithm directly. Standard math/statistics libraries (like `numpy`, `scipy.stats`, or `math`) are perfectly fine.