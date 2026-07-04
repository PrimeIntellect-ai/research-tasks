You are a performance engineer tasked with profiling and regression testing a mathematical application. The application calculates the variance of large streams of data. We need to evaluate the numerical stability and performance consistency of a custom Welford's algorithm implementation compared to a naive variance implementation.

Your task is to create a reproducible pipeline that performs numerical stability testing and calculates a bootstrap confidence interval for the performance of the algorithm.

1. Write a Python script at `/home/user/variance_test.py` that does the following:
   - Uses `numpy` to generate a test dataset: `100,000` samples from a Normal distribution with `loc=1e7` and `scale=2.5`. Use `numpy.random.RandomState(42)` to generate the samples, and cast the final array to `numpy.float32`.
   - Implement `naive_variance(arr)` which calculates variance as the mean of the squares minus the square of the mean: $E[X^2] - (E[X])^2$. All operations inside this function must use the `float32` array directly.
   - Implement `welford_variance(arr)` using the standard single-pass Welford's algorithm to compute the population variance.
   - Calculate the "true" variance by casting the `float32` array to `numpy.float64` and using `numpy.var(..., ddof=0)`.
   - Compute the absolute numerical error for both `naive_variance` and `welford_variance` against the "true" variance.
   - Profile the execution time of `welford_variance(arr)` by running it `100` separate times sequentially (using `time.perf_counter()`). Store these 100 duration measurements (in seconds).
   - Compute a 95% Bootstrap Confidence Interval for the *mean* execution time. Use exactly `1000` resamples of the 100 measurements (sampling with replacement). Use `numpy.random.RandomState(42)` for the resampling step, and use the percentile method (`2.5` and `97.5` percentiles) to find the lower and upper bounds of the confidence interval.
   - Save the results to `/home/user/report.json` with exactly the following schema:
     ```json
     {
       "naive_error": <float>,
       "welford_error": <float>,
       "welford_time_ci_low": <float>,
       "welford_time_ci_high": <float>
     }
     ```

2. Create a bash wrapper script at `/home/user/run_pipeline.sh` that:
   - Creates a Python virtual environment in `/home/user/venv`.
   - Installs `numpy` in the virtual environment.
   - Executes `/home/user/variance_test.py`.
   Make sure `/home/user/run_pipeline.sh` is executable.

Note: You do not have root access. Run everything within `/home/user`. Do not use any external profiling packages other than `numpy` and the Python standard library.