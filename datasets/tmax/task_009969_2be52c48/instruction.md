You are a machine learning engineer tasked with evaluating the data drift of a specific feature between your training and validation datasets.

You have been provided with two text files:
- `/home/user/train_feature.txt`
- `/home/user/val_feature.txt`
Each file contains one floating-point number per line, representing the feature values in the respective datasets.

Your task is to write and execute a Python script `/home/user/evaluate_drift.py` that performs the following steps:
1. Load the data from the two text files as numpy arrays.
2. Compute the 1D Wasserstein distance between the training and validation distributions using `scipy.stats.wasserstein_distance`.
3. Compute a 95% bootstrap confidence interval for this Wasserstein distance using exactly 1000 bootstrap iterations.
   - For each iteration, independently resample (with replacement) from the training features to create a bootstrap training sample (same size as the original training data), and from the validation features to create a bootstrap validation sample (same size as the original validation data).
   - Compute the Wasserstein distance between these two bootstrap samples.
   - Calculate the 95% confidence interval using the 2.5th and 97.5th percentiles of the 1000 bootstrap distances (use `numpy.percentile` with its default interpolation).
4. To ensure a reproducible computation pipeline, you must set `numpy.random.seed(42)` exactly once, immediately before starting the loop/vectorized operation that generates the bootstrap resamples.
5. Save the results to `/home/user/drift_metrics.json` in the following JSON format, with all floating-point values rounded to exactly 4 decimal places:
```json
{
  "distance": 0.1234,
  "ci_lower": 0.1000,
  "ci_upper": 0.1500
}
```

Run your script to produce the `/home/user/drift_metrics.json` file.