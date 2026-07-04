You are a machine learning engineer preparing baseline synthetic training data for a downstream Bayesian neural network. Your task is to generate samples from a known mathematical posterior to serve as a gold-standard dataset, combining MCMC sampling with analytical validation.

We are modeling the bias $p$ of a coin. The coin was flipped $N=100$ times, resulting in $k=70$ heads. 
The prior distribution for $p$ is a Beta distribution with parameters $\alpha=2$ and $\beta=2$.

Your objective is to write a Python script at `/home/user/mcmc_sampler.py` that performs the following steps:
1. Calculates the **exact analytical mean** of the posterior distribution for $p$. (You must use your domain knowledge of conjugate priors to determine the posterior parameters).
2. Implements a **Metropolis-Hastings MCMC sampler** from scratch (using only `numpy` and `scipy`) to draw samples from the unnormalized posterior.
    - Use a Gaussian proposal distribution centered at the current $p$ with standard deviation $\sigma=0.05$.
    - Handle the bounds (if a proposed $p$ is outside $(0, 1)$, reject it).
    - Run the chain for 110,000 iterations.
    - Discard the first 10,000 iterations as burn-in.
3. Computes the empirical mean of the remaining 100,000 MCMC samples.
4. Validates that the absolute difference between the MCMC mean and the analytical mean is strictly less than 0.005. If it is not, the script should raise an AssertionError.
5. Saves a summary of the validated results to `/home/user/posterior_summary.json`. The JSON file must have exactly this structure:
```json
{
  "analytical_mean": 0.0000,
  "mcmc_mean": 0.0000,
  "samples_kept": 100000
}
```

Once the script is written, execute it to ensure `/home/user/posterior_summary.json` is generated successfully.