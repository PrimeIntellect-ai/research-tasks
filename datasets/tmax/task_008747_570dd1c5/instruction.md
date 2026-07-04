You are a performance engineer analyzing a server's thermal throttling behavior and its impact on application response times. You have been given two datasets:
1. `/home/user/thermal_model.csv`: Contains `time` and `temperature` columns. The server's cooling process follows Newton's Law of Cooling: $T(t) = (T_0 - T_{env})e^{-kt} + T_{env}$, where $T_{env} = 20.0^\circ\text{C}$.
2. `/home/user/perf_log.csv`: Contains `time` (sampled at 10 Hz) and `response_time` (in milliseconds). The response times exhibit periodic spikes due to background interference.

Your task is to write a script (Python is recommended) to analyze these logs and generate a JSON report at `/home/user/report.json` containing the following exact keys:

1. `"decay_constant"`: Extract the empirical cooling rate $k$ from `thermal_model.csv`. Validate the analytical solution by estimating $k$ using the data points. Round to 3 decimal places.
2. `"dominant_frequency"`: Perform a Fast Fourier Transform (FFT) on the `response_time` column of `perf_log.csv` to find the dominant frequency (the frequency greater than 0 Hz with the highest magnitude). Round to 2 decimal places.
3. `"bootstrap_ci_lower"` and `"bootstrap_ci_upper"`: Compute a 95% bootstrap confidence interval for the mean `response_time` using exactly 10,000 resamples. **You must set the random seed to 42** before generating the bootstrap samples (e.g., `np.random.seed(42)`). Calculate the sample mean for each resample, and find the 2.5th and 97.5th percentiles. Round the bounds to 2 decimal places.

The output `/home/user/report.json` must be a valid JSON object matching this structure:
```json
{
  "decay_constant": 0.000,
  "dominant_frequency": 0.00,
  "bootstrap_ci_lower": 0.00,
  "bootstrap_ci_upper": 0.00
}
```
Ensure you install any necessary libraries (like `numpy` or `pandas` or `scipy`) via pip if you need them.