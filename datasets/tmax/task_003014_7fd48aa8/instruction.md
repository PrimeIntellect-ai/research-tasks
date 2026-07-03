You are a bioinformatics analyst studying the expression levels of a specific RNA sequence probe over time in a bioreactor. You have raw fluorescence signal data that is contaminated with high-frequency noise.

Your goal is to smooth the signal, model the population dynamics, validate your numerical solver against an analytical solution, and statistically compare two growth hypotheses.

The raw data is located at `/home/user/probe_signal.csv` and contains two columns: `time` (in seconds) and `signal`.

Please perform the following steps using Python:

1. **Signal Processing**: 
   Load the CSV data. Apply a Butterworth low-pass filter to the `signal` to remove high-frequency noise. Use `scipy.signal.butter` with order `N=2` and critical frequency `Wn=0.2` (default digital frequency where Nyquist is 1). Apply the filter using `scipy.signal.filtfilt` to produce the `smoothed_signal`.

2. **Numerical ODE Solving**:
   Model the expression dynamics using two competing models. The initial expression at `t=0` is `P0 = 10`. The intrinsic growth rate is `r = 0.05`. For Model B, the carrying capacity is `K = 500`.
   - **Model A (Exponential)**: dP/dt = r * P
   - **Model B (Logistic)**: dP/dt = r * P * (1 - P/K)
   
   Use `scipy.integrate.solve_ivp` to numerically integrate both models over the time points in the CSV. Use `method='RK45'`, `rtol=1e-6`, `atol=1e-9`, and pass the CSV's time array to `t_eval` to get the solutions at the exact data points.

3. **Analytical Validation**:
   Calculate the analytical solution for Model B at the given time points using the standard logistic growth equation: 
   `P(t) = K / (1 + ((K - P0) / P0) * exp(-r * t))`
   Find the maximum absolute difference between your numerical solution for Model B and this analytical solution.

4. **Statistical Hypothesis Comparison**:
   Calculate the Sum of Squared Errors (SSE) between the `smoothed_signal` and the numerical solutions for both Model A and Model B.
   Calculate the Akaike Information Criterion (AIC) for both models using the formula:
   `AIC = n * ln(SSE / n) + 2 * k`
   where `n` is the number of data points, `ln` is the natural logarithm, `k=1` for Model A, and `k=2` for Model B.
   Determine which model is a better fit (lower AIC).

5. **Output**:
   Create a JSON file at `/home/user/analysis_results.json` with the following keys. Round all numerical values to exactly 4 decimal places.
   - `"max_diff"`: Float, maximum absolute difference between Model B's numerical and analytical solutions.
   - `"sse_A"`: Float, SSE for Model A.
   - `"sse_B"`: Float, SSE for Model B.
   - `"aic_A"`: Float, AIC for Model A.
   - `"aic_B"`: Float, AIC for Model B.
   - `"best_model"`: String, either `"A"` or `"B"`.

Ensure your Python script is self-contained and handles all the steps.