You are a machine learning engineer preparing a sensor dataset for a predictive maintenance model. The raw data comes from a fleet of sensors, but it is noisy and contains corrupted entries. You need to build a data pipeline that filters the data, applies a Bayesian update to estimate the true state of a specific sensor, and benchmarks this update process.

Complete the following objectives:

1. **ETL and Schema Enforcement**:
   - You will find a raw data file at `/home/user/raw_sensor_data.csv`.
   - Read this file and filter it strictly according to the following schema:
     - `sensor_id`: Must be a string exactly matching the format `SENS-XXXX` where `X` is a digit (e.g., `SENS-0042`).
     - `timestamp`: Must be a valid ISO 8601 datetime string.
     - `raw_value`: Must be a float between `-10.0` and `10.0` (inclusive).
   - Drop any rows that violate this schema.
   - Save the cleaned and validated dataset as a Parquet file at `/home/user/clean_sensor_data.parquet`.

2. **Bayesian Inference**:
   - We need to estimate the true underlying value for the sensor `SENS-0042`.
   - Assume the true value follows a Gaussian prior distribution with mean $\mu_0 = 0.0$ and variance $\sigma_0^2 = 10.0$.
   - Assume each valid measurement (`raw_value`) for `SENS-0042` is a noisy observation drawn from a Gaussian distribution centered at the true value with a known measurement variance $\sigma^2 = 2.0$.
   - Using *only* the validated data for `SENS-0042`, compute the posterior mean ($\mu_n$) and posterior variance ($\sigma_n^2$) of the true value.

3. **Inference Benchmarking**:
   - Wrap your Bayesian update logic (the math to compute posterior mean and variance from a list/array of values) into a standalone Python function.
   - Benchmark the execution time of this function using the valid `SENS-0042` data. Run the function exactly 10,000 times in a loop.
   - Calculate the average execution time per function call in milliseconds.

4. **Reporting**:
   - Create a JSON summary file at `/home/user/results.json` with exactly the following keys:
     - `"valid_rows_count"`: (integer) Total number of valid rows across all sensors in the Parquet file.
     - `"SENS_0042_posterior_mean"`: (float) The computed posterior mean, rounded to 4 decimal places.
     - `"SENS_0042_posterior_variance"`: (float) The computed posterior variance, rounded to 4 decimal places.
     - `"benchmark_avg_ms"`: (float) The average execution time of the update function in milliseconds.

Ensure you install any necessary Python packages (like `pandas`, `pyarrow`, `pydantic`) using `pip` before running your scripts.