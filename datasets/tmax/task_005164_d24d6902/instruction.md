You are a data scientist analyzing the reaction kinetics of a new chemical process. The sensor data you have collected measures the *rate* of product formation over time, but your mathematical models are defined in terms of the *cumulative* product formed. 

You have been provided with a dataset at `/home/user/reaction_rate.csv` containing two columns: `time` (in minutes) and `rate` (in moles per minute).

Perform the following analysis using Python:

1. **Numerical Integration:** Compute the cumulative product formed at each time step by numerically integrating the `rate` with respect to `time`. Use the trapezoidal rule. Assume the cumulative product at the first time step ($t=0$) is $0$.
2. **Model Fitting:** Fit two competing kinetic models to the `(time, cumulative_product)` data using non-linear least squares (`scipy.optimize.curve_fit`). 
   * **Exponential Model:** $C(t) = L \cdot (1 - e^{-k \cdot t})$. Use initial guesses $L=10.0$, $k=0.1$.
   * **Hyperbolic Model:** $C(t) = \frac{V_{max} \cdot t}{K_m + t}$. Use initial guesses $V_{max}=10.0$, $K_m=1.0$.
3. **Statistical Hypothesis Comparison:** Compare the two models by calculating the Akaike Information Criterion (AIC) for each. Use the formula: $AIC = n \cdot \ln(SSE/n) + 2p$, where $n$ is the number of data points, $SSE$ is the sum of squared residuals, and $p$ is the number of parameters (which is 2 for both models). Identify the "best" model as the one with the *lower* AIC.
4. **Bootstrap Confidence Interval:** For the *best* model identified in step 3, estimate the uncertainty of its **first parameter** ($L$ for the Exponential model, or $V_{max}$ for the Hyperbolic model). Calculate a 95% confidence interval using the non-parametric pairs bootstrap method.
   * Resample the `(time, cumulative_product)` data pairs with replacement $B=1000$ times.
   * Refit the best model on each resampled dataset. If a fit fails to converge, discard it and continue (do not replace the iteration).
   * Calculate the 2.5th and 97.5th percentiles of the successfully fitted first parameter.
   * **Crucial:** To ensure reproducibility, set the random seed to `42` (`numpy.random.seed(42)`) exactly once, immediately before your bootstrap loop.

Finally, output your results to a JSON file at `/home/user/model_results.json`. The JSON must contain exactly the following keys:
- `"best_model"`: A string, either `"Exponential"` or `"Hyperbolic"`.
- `"aic_exponential"`: The AIC of the exponential model (float, rounded to 2 decimal places).
- `"aic_hyperbolic"`: The AIC of the hyperbolic model (float, rounded to 2 decimal places).
- `"param1_estimate"`: The estimate of the first parameter ($L$ or $V_{max}$) from the original data fit (float, rounded to 4 decimal places).
- `"param1_ci_lower"`: The 2.5th percentile from the bootstrap (float, rounded to 4 decimal places).
- `"param1_ci_upper"`: The 97.5th percentile from the bootstrap (float, rounded to 4 decimal places).