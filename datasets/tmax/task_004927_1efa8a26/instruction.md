You are helping an astrophysics researcher analyze a large dataset of simulated light curves. The data is stored in HDF5 format. The researcher has a pipeline to filter out instrumental anomalies (the "evil" data) from the actual astrophysical signals (the "clean" data), but the environment is broken and the filtering script needs to be written.

Here is what you need to do:

1. **Fix and Install the Vendored Package:**
   The researcher uses a custom package located at `/app/vendored/astro_core`. It provides a highly optimized numerical differentiation function. However, the package is currently broken due to a deliberate perturbation (a syntax error or typo introduced during a bad merge).
   - Find and fix the bug in `/app/vendored/astro_core`.
   - Install the package into your Python environment so it can be imported as `astro_core`.

2. **Develop the Classifier Script:**
   Write a Python script at `/home/user/classify.py`. This script must act as a filter/classifier for individual HDF5 files. 
   - **Invocation:** `python3 /home/user/classify.py <path_to_h5_file>`
   - **Output/Behavior:** The script must exit with code `0` if the file is a "clean" signal, and exit with code `1` if the file is an "evil" anomaly.

3. **Classification Logic:**
   Each HDF5 file contains two datasets at the root level: `time` and `flux`.
   To classify a file as "clean", **both** of the following conditions must be met:
   
   **Condition A (Numerical Differentiation):**
   Use the fixed `astro_core.compute_derivative(time, flux)` function to compute the derivative $d(\text{flux})/d(\text{time})$. The maximum absolute value of this derivative must be **strictly less than 50.0**. (Instrumental anomalies often contain sudden, unphysical spikes).
   
   **Condition B (MCMC Posterior Estimation):**
   The underlying clean signal is expected to follow a quadratic model: $\text{flux} = a \cdot \text{time}^2 + b \cdot \text{time} + c$. 
   Use the `emcee` library to perform MCMC sampling to estimate the posterior distributions of the parameters $a$, $b$, and $c$. 
   - Assume uniform priors: $a \in [-100, 100]$, $b \in [-100, 100]$, $c \in [-100, 100]$.
   - Assume a Gaussian likelihood with a fixed standard deviation of $\sigma = 1.0$ for the residuals.
   - Run the sampler with 32 walkers for 500 steps, discarding the first 100 steps as burn-in.
   - Compute the median of the posterior samples for the parameter **$a$**.
   - For the file to be clean, the median of **$a$** must be **strictly greater than 0.0**. (We are looking for concave-up signals).

If either Condition A is violated (max absolute derivative $\ge 50.0$) or Condition B is violated (posterior median of $a \le 0.0$), the script must exit with code `1` (evil). Otherwise, exit with code `0` (clean).

Ensure your script is robust and deterministic. You may install `emcee`, `h5py`, and any other standard numerical libraries you need.