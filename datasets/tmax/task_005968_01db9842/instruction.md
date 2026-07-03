You are acting as an AI assistant for a computational chemistry researcher. They have collected some noisy spectroscopy data and need to build a reproducible computation pipeline to analyze it.

The data is located at `/home/user/spectroscopy_data.csv` (contains two columns: `wavelength` and `intensity`).

The researcher wants you to:
1. **Define two candidate models** for curve fitting:
   - **1-Peak Model:** A single Lorentzian peak plus a linear baseline.
     Formula: `I(x) = a1 / (1 + ((x - x1)/w1)**2) + m*x + c`
     (Parameters: `a1`, `x1`, `w1`, `m`, `c`. Initial guess: `[10, 50, 5, 0, 0]`)
   - **2-Peak Model:** Two Lorentzian peaks plus a linear baseline.
     Formula: `I(x) = a1 / (1 + ((x - x1)/w1)**2) + a2 / (1 + ((x - x2)/w2)**2) + m*x + c`
     (Parameters: `a1`, `x1`, `w1`, `a2`, `x2`, `w2`, `m`, `c`. Initial guess: `[10, 40, 5, 10, 60, 5, 0, 0]`)

2. **Fit both models** to the data using non-linear least squares (`scipy.optimize.curve_fit`).

3. **Compare the hypotheses** by calculating the Bayesian Information Criterion (BIC) for both models to determine which fits better.
   - Use the formula: `BIC = n * ln(RSS / n) + k * ln(n)`
   - Where `n` is the number of data points, `RSS` is the Residual Sum of Squares, and `k` is the number of parameters. (Use `numpy.log` for the natural logarithm).

4. **Compute bootstrap confidence intervals** for the peak center parameters (`x1`, and `x2` if applicable) of the **best model** (the one with the lower BIC).
   - Use exactly `500` bootstrap iterations.
   - For each iteration, resample the data pairs `(wavelength, intensity)` **with replacement**.
   - Use `numpy.random.seed(42)` immediately before the bootstrap loop to ensure reproducibility.
   - Calculate the 95% confidence interval (2.5th and 97.5th percentiles) for the peak center(s).
   - *Note: In the 2-peak model, assume `x1` corresponds to the first parameter guess (40) and `x2` to the second (60).*

5. **Save the results** in a JSON file at `/home/user/spectroscopy_results.json` with the following exact structure:
```json
{
  "bic_1peak": 123.45,
  "bic_2peak": 100.12,
  "best_model": "2-peak", 
  "bootstrap_ci_x1": [43.12, 46.88],
  "bootstrap_ci_x2": [53.50, 56.10] 
}
```
*(If the 1-peak model is best, omit `bootstrap_ci_x2`, and set `best_model` to "1-peak"). Round all floats to 2 decimal places in the final JSON.*

Please write and execute the Python script to perform this analysis and generate the output file.