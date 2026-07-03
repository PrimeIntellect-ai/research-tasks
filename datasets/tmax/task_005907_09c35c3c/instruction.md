You are an ML engineer preparing a training dataset of battery degradation cycles. The raw data is noisy, and you need to extract the underlying degradation trend, estimate the uncertainty of the decay rate, and save the results for the downstream training pipeline.

You have been provided with a dataset at `/home/user/raw_battery_data.csv` containing two columns: `cycle` (the charge cycle number, $x$) and `capacity` (the measured battery capacity, $y$).

Your task is to write a reproducible Python script at `/home/user/prepare_data.py` that does the following:
1. Loads the CSV data.
2. Fits the non-linear exponential decay curve: $y = a \cdot e^{-b \cdot x} + c$ using least-squares optimization to find the optimal parameters $a$, $b$, and $c$. Use initial guesses: $a=1.0, b=0.01, c=0.5$.
3. Uses the bootstrap method to compute the 95% confidence interval for the decay rate parameter ($b$). 
   - Perform exactly 1000 bootstrap iterations (sample with replacement from the original dataset, same size as original).
   - For each iteration, fit the curve to the resampled data to get a new estimate of $b$. (If a fit fails to converge in an iteration, you may skip it or catch the exception, but a good fit shouldn't fail with these initial guesses).
   - Calculate the 2.5th and 97.5th percentiles of the bootstrapped $b$ values to get the lower and upper bounds of the 95% confidence interval.
4. **Crucial for reproducibility:** You must set `numpy.random.seed(42)` exactly once, immediately before your bootstrap loop, to ensure the random sampling is reproducible.
5. Saves the final optimized parameters (from the fit on the *original* data) and the confidence interval for $b$ to `/home/user/degradation_metadata.json`.

The output JSON must have exactly the following structure:
```json
{
  "a": <float>,
  "b": <float>,
  "c": <float>,
  "b_ci_lower": <float>,
  "b_ci_upper": <float>
}
```

Write the script and run it to produce the output file.