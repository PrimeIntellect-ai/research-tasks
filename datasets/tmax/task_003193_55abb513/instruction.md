You are an ML Engineer preparing training data for a physical sensor emulator. You have two datasets: a clean reference dataset and a new, potentially noisy batch of raw sensor readings.

Your raw files are:
- `/home/user/reference.csv` (contains a single column "value" of clean historical data)
- `/home/user/batch.csv` (contains a single column "value" of new incoming data)

Your task is to implement a robust statistical filtering and evaluation pipeline in Python to validate the new batch. Perform the following steps:

1. **Density Estimation:** Fit a Gaussian Kernel Density Estimator (KDE) to the `reference.csv` data. Use the default bandwidth estimator (Scott's Rule).
2. **Integration and Root Finding:** The KDE does not have a simple closed-form CDF. You must numerically integrate the KDE's Probability Density Function (PDF) and solve a nonlinear equation to find the exact threshold $T$ where the Cumulative Distribution Function (CDF) equals 0.90 (i.e., the 90th percentile of the KDE).
3. **Data Filtering:** Filter the `batch.csv` data to keep only the values that are less than or equal to $T$.
4. **Bootstrap Confidence Intervals:** Calculate the mean of the filtered batch data. Then, compute the 95% bootstrap confidence interval for this mean using exactly 1000 resamples, the 'BCa' (bias-corrected and accelerated) method, and a random seed of `42`.

Save your final results to a JSON file at `/home/user/metrics.json`. The JSON file must contain exactly the following keys, with values rounded to 4 decimal places:
- `"threshold"`: The calculated 90th percentile threshold $T$.
- `"filtered_mean"`: The mean of the filtered batch data.
- `"ci_lower"`: The lower bound of the 95% bootstrap confidence interval.
- `"ci_upper"`: The upper bound of the 95% bootstrap confidence interval.

Ensure your code is completely self-contained and executable. Do not modify the original CSV files.