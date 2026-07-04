You are a data scientist dealing with a challenging spectral fitting problem. You have a spectrum that consists of three overlapping Gaussian peaks. However, two of the peaks are highly collinear (severely overlapping), causing standard Ordinary Least Squares (OLS) regression to fail or give non-physical (negative) amplitudes due to a near-singular design matrix. 

Your task is to estimate the amplitudes of these peaks using a Bayesian approach, specifically Markov Chain Monte Carlo (MCMC), to enforce strict positivity constraints. After fitting, you will compare the distributions using a probability distribution distance metric.

**Step 1: Data Generation**
Write a Python script to generate the synthetic experimental data.
- Use `numpy` and set `np.random.seed(42)` at the very beginning.
- Create an `x` array of 100 points linearly spaced between 0 and 10 (inclusive).
- The three basis functions (unscaled peaks) are:
  - $f_1(x) = \exp\left(-\frac{(x - 2.0)^2}{2 \times 0.5^2}\right)$
  - $f_2(x) = \exp\left(-\frac{(x - 6.0)^2}{2 \times 0.8^2}\right)$
  - $f_3(x) = \exp\left(-\frac{(x - 6.1)^2}{2 \times 0.8^2}\right)$
- The true amplitudes are $A_1=2.0$, $A_2=1.0$, $A_3=0.5$.
- Compute the true signal: $y_{true} = A_1 f_1 + A_2 f_2 + A_3 f_3$.
- Add Gaussian noise with a mean of 0.0 and standard deviation of 0.1 to create `y_noisy`.

**Step 2: MCMC Sampling**
Use the `emcee` library (you may need to install it) to sample the posterior distribution of the three amplitudes $(A_1, A_2, A_3)$.
- **Prior**: Uniform distribution between 0 and 10 for all three amplitudes. If any amplitude is outside this range, the log-prior is `-inf`.
- **Likelihood**: Gaussian likelihood with the known standard deviation of $\sigma = 0.1$.
- Initialize 10 walkers tightly clustered around the true values (e.g., true value + a small random Gaussian perturbation of $10^{-4}$).
- Run the sampler for 5,000 steps.
- Discard the first 1,000 steps as burn-in and flatten the remaining chain.
- Calculate the posterior mean for the three amplitudes from these flat samples.

**Step 3: Distance Metric and Visualization**
- Reconstruct the model signal `y_recon` using the posterior mean amplitudes.
- Clip any negative values in `y_noisy` to 0, creating `y_noisy_clipped`.
- Normalize both `y_noisy_clipped` and `y_recon` so they sum to 1.0 (treating them as probability mass functions over the grid `x`).
- Compute the 1D Wasserstein distance between these two normalized distributions over the domain `x`. Use `scipy.stats.wasserstein_distance(x, x, u_weights=..., v_weights=...)`.
- Create a visualization plotting `y_noisy` (as scatter points) and `y_recon` (as a solid line), and save it to `/home/user/mcmc_fit.png`.

**Step 4: Save Results**
Create a JSON file at `/home/user/results.json` containing the calculated values. The file must have exactly these keys (values should be standard floats):
```json
{
    "A1_mean": <float>,
    "A2_mean": <float>,
    "A3_mean": <float>,
    "wasserstein_distance": <float>
}
```

Ensure your code is clean and reproducible. You can use standard terminal commands to install any missing libraries.