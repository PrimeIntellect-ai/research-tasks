You are helping a data analyst who is benchmarking the performance of two different ML inference engines. They have collected latency data into two files: `/home/user/engine_a.csv` and `/home/user/engine_b.csv`. Each CSV has two columns: `input_size` (in tokens) and `latency_ms` (in milliseconds).

The analyst wrote a script, `/home/user/analyze.py`, to calculate the correlation between input size and latency, and to run a t-test to see if the latency differences between the engines are statistically significant. However, the script is broken, throws errors, and produces different statistical results every time it's run because of how it handles sampling. 

Your task is to fix `/home/user/analyze.py` so that it correctly and reproducibly performs the following steps:
1. Load both CSV files using `pandas`.
2. Compute the Pearson correlation coefficient between `input_size` and `latency_ms` for both Engine A and Engine B using the full datasets.
3. For the hypothesis test, the analyst mandates that both datasets must be the exact same size. Downsample the larger dataset so its row count matches the smaller dataset. **Crucially, to ensure pipeline reproducibility, you must use `pandas.DataFrame.sample()` with `random_state=42`.**
4. Perform an independent two-sample t-test (Welch's t-test, assuming unequal variances) on the `latency_ms` of Engine A and Engine B using the now-equal-sized datasets.
5. Save the results as a JSON file at `/home/user/metrics.json` with the following exact keys and standard float values:
```json
{
    "correlation_A": <float>,
    "correlation_B": <float>,
    "t_statistic": <float>,
    "p_value": <float>
}
```

Fix the script and run it to produce the `metrics.json` file. Ensure your final script handles the downsampling and hypothesis testing correctly.