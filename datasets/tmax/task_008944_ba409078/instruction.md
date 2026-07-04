You are a data scientist validating a custom MCMC sampling algorithm against an analytical solution. 

You need to write a Python script `/home/user/validate_mcmc.py` that samples from the posterior of a Beta-Binomial model using the Metropolis-Hastings algorithm, and compares the sample statistics with the exact analytical solution.

Model Details:
- Parameter of interest: $\theta$ (probability of success), bounded in $[0, 1]$.
- Prior distribution: Beta distribution with $\alpha=2$ and $\beta=2$.
- Data (Likelihood): Binomial distribution with $n=20$ trials and $k=15$ successes.

MCMC Algorithm (Metropolis-Hastings):
- Initialize $\theta_0 = 0.5$.
- Proposal distribution: Normal distribution centered at the current $\theta$ with standard deviation $\sigma = 0.1$.
- If the proposed $\theta$ is outside $[0, 1]$, the probability of accepting it is 0.
- Otherwise, the acceptance probability is $\min(1, \frac{P(\theta_{prop} | \text{data})}{P(\theta_{curr} | \text{data})})$.
- Run the sampler for 100,000 total iterations.
- Discard the first 20,000 iterations as burn-in.

Analytical Solution:
- Calculate the exact analytical posterior mean and variance based on conjugacy.

Output Requirements:
1. Run the sampler and compute the sample mean and variance of the kept samples.
2. Save the results to `/home/user/results.json` with exactly the following keys:
   - `"analytical_mean"` (float)
   - `"analytical_var"` (float)
   - `"mcmc_mean"` (float)
   - `"mcmc_var"` (float)
3. Create a plot saved to `/home/user/posterior.png` that overlays a density histogram of your MCMC samples and the exact analytical Probability Density Function (PDF) of the posterior distribution. 

Make sure the script executes successfully and generates both the JSON and the PNG files.