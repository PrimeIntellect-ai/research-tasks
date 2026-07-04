You are an AI assistant helping a computational physicist analyze noisy spectroscopy data. 

I have a dataset of a spectral line located at `/home/user/spectrum.csv` with two columns: `wavelength` and `intensity`. 
The signal is known to follow a Gaussian profile with a fixed standard deviation $\sigma = 1.0$:
$$ I(x) = A \cdot \exp\left(-\frac{(x - \mu)^2}{2}\right) $$
where $x$ is the wavelength, $A$ is the peak amplitude, and $\mu$ is the center wavelength. 
The observed intensity includes additive zero-mean Gaussian noise with a standard deviation of $\sigma_{noise} = 0.5$.

Your task is to:
1. Initialize a new Rust project named `spectral_mcmc` in `/home/user/`.
2. Write a Rust program that reads `/home/user/spectrum.csv` and implements a Metropolis-Hastings Markov Chain Monte Carlo (MCMC) sampler from scratch to estimate the posterior distributions of $A$ and $\mu$.
3. Use the following MCMC parameters:
    - Number of iterations: 50,000
    - Burn-in (iterations to discard): 10,000
    - Prior for $A$: Uniform over $[0.0, 10.0]$
    - Prior for $\mu$: Uniform over $[-5.0, 5.0]$
    - Proposal distributions: Normal distribution centered on the current value with standard deviation $0.1$ for both parameters.
    - Initial state: $A = 1.0$, $\mu = 0.0$
4. Calculate the posterior mean for $A$ and $\mu$ using the samples after burn-in.
5. Perform an analytical validation by calculating the Sum of Squared Errors (SSE) between the observed intensities and the theoretical intensities using your posterior mean estimates.
6. Write the final results to `/home/user/results.json` with the exact following structure:
```json
{
  "A_mean": 4.123,
  "mu_mean": 1.234,
  "sse": 25.678
}
```

Run your Rust program and ensure the `results.json` file is successfully generated. You may use external crates like `csv`, `serde`, `serde_json`, and `rand`.