You are an expert data scientist and Rust developer. We need to build a robust ETL and analysis pipeline in Rust to process a batch of dirty sensor data. 

You have been provided with a dataset at `/home/user/sensor_data.csv`. The CSV has three columns: `Temperature`, `Pressure`, and `Humidity`. The data is noisy, contains missing values (represented as empty strings), and includes outliers.

Your objective is to create a Rust project in `/home/user/etl_pipeline` that reads this CSV, cleans it, performs statistical analysis, and outputs the results to `/home/user/results.json`.

Here are the exact pipeline steps you must implement:

1. **Missing Value Imputation**: First, calculate the mean of all valid (non-empty, parseable) `Humidity` values. Replace any missing `Humidity` values with this mean.
2. **Outlier Filtering**: After imputation, filter out invalid rows. Drop a row entirely if:
   - `Temperature` is missing, less than `-50.0`, or greater than `50.0`.
   - `Pressure` is missing, less than `800.0`, or greater than `1200.0`.
3. **Correlation Analysis**: On the final cleaned dataset, calculate the Pearson correlation coefficient between `Temperature` and `Pressure`.
4. **Bayesian Inference**: We want to estimate the true mean `Temperature` using Bayesian inference with a conjugate prior (Normal-Normal model).
   - Assume a prior distribution for the mean Temperature: $\mu_0 = 20.0$, prior variance $\sigma_0^2 = 25.0$.
   - Assume the population variance of Temperature is known to be $\sigma^2 = 16.0$.
   - Using the cleaned dataset's `Temperature` values as your observations, calculate the posterior mean and posterior variance. 

*Hint for Bayesian Normal-Normal update:*
Posterior variance: $\sigma_n^2 = \frac{1}{\frac{1}{\sigma_0^2} + \frac{n}{\sigma^2}}$
Posterior mean: $\mu_n = \sigma_n^2 \left( \frac{\mu_0}{\sigma_0^2} + \frac{\sum_{i=1}^{n} x_i}{\sigma^2} \right)$
*(where $n$ is the number of cleaned observations and $x_i$ are the cleaned Temperature values).*

Write your results to a file named `/home/user/results.json` with the following exact structure (use standard 64-bit floats):
```json
{
  "cleaned_row_count": 100,
  "correlation_temp_pressure": 0.1234,
  "posterior_mean_temp": 21.5678,
  "posterior_variance_temp": 0.4321
}
```

Ensure your Rust code handles the CSV reading and JSON writing natively or using standard crates like `csv` and `serde`. Run your Rust pipeline so that the output JSON is generated.