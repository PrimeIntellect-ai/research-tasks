You are a bioinformatics analyst working with raw ionic current signal data from a nanopore sequencer. Your goal is to process the noisy time-series signal, identify sequence-specific blocking events, compute the mean dwell time of these events, and validate the uncertainty of this mean both empirically (via bootstrap) and analytically.

A raw signal dataset is provided at `/home/user/nanopore_signal.csv`. It contains two columns: `time` (in milliseconds) and `current` (in picoamperes, pA). The sampling rate is 10 kHz (0.1 ms between points).

Please perform the following steps:
1. **Signal Processing:** Smooth the `current` data using a rolling mean with a window size of 10. Use pandas `rolling(10).mean().dropna()` (or equivalent) to compute this, effectively removing the first 9 points containing NaNs. Align the `time` array accordingly so it matches the smoothed signal's length.
2. **Event Detection:** Threshold the smoothed signal. We define the pore as being in a "blocked" state when the smoothed current is strictly less than `< 75.0` pA. 
3. **Dwell Time Extraction:** Identify all continuous segments where the pore is in the "blocked" state. For each continuous blocked segment, its dwell time in milliseconds is calculated as the `number_of_points_in_segment * 0.1`.
4. **Mean Dwell Time:** Calculate the sample mean of all extracted blocked dwell times. Count the total number of blocked events `N`.
5. **Bootstrap Confidence Interval:** To empirically estimate the uncertainty of the mean dwell time, perform bootstrap resampling. 
   - Set `numpy.random.seed(42)` immediately before your bootstrap loop.
   - Generate 10,000 bootstrap samples (with replacement) of the dwell times array, each of size `N`.
   - Compute the mean for each bootstrap sample.
   - Calculate the 95% confidence interval using the 2.5th and 97.5th percentiles of the bootstrap means (using `numpy.percentile` with default settings).
6. **Analytical Validation:** Assuming the dwell times follow an exponential distribution, the maximum likelihood estimate of the mean is the sample mean, and the standard error (SE) of the mean is `mean / sqrt(N)`. Compute the analytical 95% confidence interval based on the normal approximation: `[mean - 1.96 * SE, mean + 1.96 * SE]`.

Finally, output your results to `/home/user/results.json` with exactly the following keys and float values rounded to 4 decimal places (except `event_count` which should be an integer):
- `"mean_dwell_time"`
- `"bootstrap_ci_lower"`
- `"bootstrap_ci_upper"`
- `"analytical_ci_lower"`
- `"analytical_ci_upper"`
- `"event_count"`

Ensure your script handles the data correctly and runs without requiring interactive input.