You are a performance engineer profiling and debugging a spectroscopy analysis pipeline. 

An existing script that calculates the decay rate of a chemical species from spectrometer logs is crashing. The species concentration follows the ODE:
dI/dt = -k * I
where I is the signal intensity and k is the decay constant. 

The previous engineer tried to solve this by linearizing the data (using `ln(I) = ln(I_0) - k*t`) and performing Ordinary Least Squares via direct matrix inversion `(X^T X)^-1 X^T Y`. However, because the signal decays to zero and contains instrument noise, later data points become negative or zero. This causes `ln(I)` to produce NaNs, creating a near-singular/invalid matrix that crashes the pipeline.

Your task is to build a robust, reproducible Python script `/home/user/analyze_spectra.py` that bypasses this singularity, fits the ODE properly, and calculates a Bootstrap Confidence Interval for the decay constant.

Here are the requirements:

1. **Observational Data Reshaping**:
   Read the raw data from `/home/user/data/raw_spectra.txt`. The file alternates between lines specifying the time and lines specifying 3 independent sensor readings.
   Format:
   `Time: 0.0`
   `Intensity: 100.2 99.8 100.5`
   Parse this file and compute the mean intensity across the 3 sensors for each time point to get a single 1D array of mean intensities `I_raw` and a 1D array of times `t`.

2. **Signal Smoothing**:
   Apply a 3-point moving average to the mean intensities to get `I_smooth`. 
   - For the interior points (0 < i < N-1): `I_smooth[i] = (I_raw[i-1] + I_raw[i] + I_raw[i+1]) / 3`
   - For the boundaries, keep the raw mean value: `I_smooth[0] = I_raw[0]`, `I_smooth[N-1] = I_raw[N-1]`

3. **Robust ODE Fitting**:
   Instead of log-linearizing, fit the analytical solution of the ODE `I(t) = I_0 * exp(-k * t)` directly to `t` and `I_smooth` using Non-Linear Least Squares (e.g., `scipy.optimize.curve_fit`). 
   - Use initial guesses: `I_0 = I_smooth[0]` and `k = 1.0`.
   - Let `I_pred` be the predicted intensities using the fitted `I_0` and `k`.

4. **Bootstrap Confidence Intervals**:
   Calculate the 95% Confidence Interval for `k` using residual resampling.
   - Calculate the residuals: `residuals = I_smooth - I_pred`
   - Set the random seed: `numpy.random.seed(42)`
   - Perform `B = 1000` bootstrap iterations. In each iteration:
     a. Sample the residuals with replacement to create `boot_residuals` (must be same length as `t`).
     b. Create bootstrap data: `I_boot = I_pred + boot_residuals`
     c. Fit `I_boot` using `curve_fit` (with the same initial guesses) to find `k_boot`. If a fit fails to converge, discard that iteration and continue.
   - The 95% CI is defined by the 2.5th and 97.5th percentiles of the successfully fitted `k_boot` values (use `numpy.percentile`).

5. **Output**:
   Save the results to `/home/user/results.json` in exactly this format:
   ```json
   {
       "k_estimate": 2.5432,
       "ci_lower": 2.1001,
       "ci_upper": 2.8992
   }
   ```
   *(Ensure values are floats, precise to at least 4 decimal places).*

You may install any required Python packages (e.g., `numpy`, `scipy`) using `pip`. Execute your script to generate the final `results.json`.