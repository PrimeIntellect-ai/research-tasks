You are tasked with fixing and completing a Rust-based data ETL (Extract, Transform, Load) pipeline. We have a daily batch job that processes sensor data, but the current pipeline is failing—it produces blank/NaN outputs and occasionally panics because it cannot handle misconfigured sensor outputs, missing values, and extreme outliers. 

Your objective is to build a robust Rust application that reads a raw CSV dataset, cleans it, performs a statistical regression, runs a reproducible bootstrap analysis, and benchmarks the inference time.

**Environment details:**
- A raw CSV file is located at `/home/user/data/sensor_log.csv`. 
- The CSV has three columns: `id`, `sensor_x`, and `sensor_y`.

**Requirements for the Rust Pipeline:**
1. **Data Cleaning (Missing Values & Outliers):**
   - Read `/home/user/data/sensor_log.csv`.
   - Drop any row where `sensor_x` or `sensor_y` is empty, `"NaN"`, or cannot be parsed as an `f64`.
   - Drop any row where `sensor_x` is an extreme outlier, defined as `sensor_x > 1000.0`.

2. **Statistical Modeling (Regression):**
   - Perform a Simple Ordinary Least Squares (OLS) linear regression to predict `sensor_y` from `sensor_x` on the cleaned dataset.
   - Calculate the slope ($m$) of the regression line.

3. **Sampling & Bootstrap (Reproducible):**
   - Calculate the mean of the cleaned `sensor_x` values.
   - Construct a 95% Confidence Interval for the mean of `sensor_x` using the percentile bootstrap method.
   - **Bootstrap specifications:** Use exactly 10,000 resamples. Each resample must be the same size as the cleaned dataset, sampled with replacement.
   - **Reproducibility:** You must use the `rand` and `rand_chacha` crates. Initialize a `ChaCha8Rng` with the seed `42` (`SeedableRng::seed_from_u64(42)`) to ensure the sampling is deterministic. Calculate the mean of each resample. Sort the means and pick the 2.5th percentile and 97.5th percentile (indexes `250` and `9749` after sorting).

4. **Benchmarking & Output:**
   - Measure the time it takes to perform the Regression and Bootstrap computations (excluding file I/O).
   - The application must write its final results to `/home/user/output/results.json`.

**Output Format (`/home/user/output/results.json`):**
```json
{
  "cleaned_row_count": 105,
  "slope": 2.3456,
  "mean_x": 10.5,
  "bootstrap_ci_lower": 9.2,
  "bootstrap_ci_upper": 11.8,
  "compute_time_ms": 15
}
```

**Constraints:**
- You must create a new Rust project at `/home/user/etl_pipeline` and compile/run it to generate the output file.
- Make sure to create the `/home/user/output` directory if it does not exist.
- Write your code directly, update `Cargo.toml` as needed, and execute `cargo run --release` to generate the file.