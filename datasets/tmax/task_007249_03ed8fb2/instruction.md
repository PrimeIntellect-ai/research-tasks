You are a data analyst debugging a pipeline. A previous analyst left a dataset at `/home/user/sensor_data.csv` containing two columns: `alpha` and `beta`. We need to extract statistical properties from this data, but it is corrupted with missing values and extreme outliers which cause our current plotting tools to fail or produce blank graphs.

Your task is to write a Rust program from scratch that cleans the data and computes specific metrics. 

Perform the following steps in Rust:
1. **Missing Value Handling**: Read `/home/user/sensor_data.csv`. Parse `alpha` and `beta` as 64-bit floats (`f64`). Completely discard any row where either column is empty, missing, or fails to parse as a valid float.
2. **Outlier Rejection**: 
   - First, calculate the sample mean and sample standard deviation (using N-1) of the `alpha` column across all successfully parsed rows.
   - Then, filter the dataset by keeping *only* the rows where the `alpha` value falls within 2 standard deviations of the mean (i.e., $| \text{alpha} - \text{mean} | \le 2 \times \text{std}$).
3. **Covariance Analysis**: Calculate the sample covariance (using N-1) between the `alpha` and `beta` columns of the *cleaned* dataset.
4. **Bayesian Inference**: Estimate the true mean of the `beta` variable using the cleaned dataset. 
   - Assume the observations in the cleaned `beta` column are drawn from a Normal distribution with unknown mean $\mu$ and known variance $\sigma^2 = 4.0$.
   - Use a Normal prior for $\mu$ with mean $\mu_0 = 10.0$ and variance $\sigma_0^2 = 2.0$.
   - Calculate the posterior mean of $\mu$.
5. **Reporting**: Write the computed sample covariance and posterior mean of beta to a JSON file at `/home/user/results.json` exactly in this format (round to 4 decimal places):
```json
{
  "covariance": <float>,
  "posterior_mean_beta": <float>
}
```

You can use standard Cargo project creation (`cargo new`) and add dependencies if you wish, or just write a standalone Rust script. Make sure you execute your code and that `/home/user/results.json` is created with the correct answers.