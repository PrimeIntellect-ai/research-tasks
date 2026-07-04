You are an AI assistant acting as a computational researcher. We have an observed noisy time-series signal from a recent experiment and need to characterize it. We believe the signal consists of a single dominant sinusoidal component with additive Gaussian noise. 

You need to perform a three-phase analysis: Spectral Analysis, Reference Matching, and Bayesian Parameter Estimation (MCMC).

**System State & Inputs:**
There are two files in your home directory (`/home/user/`):
1. `observed_signal.csv`: Contains the noisy time-series data. Columns are `t` (time in seconds) and `y` (signal amplitude).
2. `reference.csv`: A database of known candidate signals. Columns are `name` and `frequency` (in Hz).

**Your Task:**
Write a Python script (e.g., `/home/user/analyze.py`) to perform the following steps, and execute it to produce the final results:

1. **Spectral Analysis (FFT):**
   - Compute the Fast Fourier Transform (FFT) of the observed signal `y`.
   - Identify the dominant frequency ($f_{peak}$) in Hertz. (Assume the sampling rate is uniform based on the `t` column).

2. **Reference Matching:**
   - Compare $f_{peak}$ to the frequencies in `/home/user/reference.csv`.
   - Identify the `name` of the signal with the closest frequency to $f_{peak}$.

3. **MCMC Sampling & Posterior Estimation:**
   - We model the signal as: $y(t) = A \sin(2 \pi f t + \phi) + \epsilon$, where $\epsilon \sim \mathcal{N}(0, \sigma^2)$.
   - Install and use the `emcee` Python package (via `pip`) to sample the posterior distributions of the parameters: $(A, f, \phi, \sigma)$.
   - Use the following uniform priors:
     - $A \in [0, 10]$
     - $f \in [f_{peak} - 0.5, f_{peak} + 0.5]$
     - $\phi \in [0, 2\pi]$
     - $\sigma \in [0.01, 5.0]$
   - Use a Gaussian log-likelihood for the residuals.
   - Run the MCMC sampler with 16 walkers for 2000 steps. Discard the first 500 steps as burn-in.
   - Compute the mean of the flattened posterior samples for each of the four parameters.

4. **Output:**
   - Generate a JSON file at `/home/user/results.json` with exactly the following keys and your computed values (floats for numerical values, string for the name):
     - `"dominant_frequency_fft"`
     - `"closest_reference_name"`
     - `"mcmc_mean_A"`
     - `"mcmc_mean_f"`
     - `"mcmc_mean_phi"`
     - `"mcmc_mean_sigma"`

Make sure to install any required dependencies (like `numpy`, `scipy`, `pandas`, `emcee`) using `pip` before running your script.