You are an MLOps engineer responsible for testing and validating experiment artifacts for our machine learning platform. 

We have simulated a large-scale data storage environment by partitioning our latest experiment's prediction logs into multiple gzipped CSV files. These files are located in `/home/user/artifacts/`. Each file is named `part-XXXX.csv.gz` and contains the headers `id,y_true,y_pred_A,y_pred_B`. 

Model A is our current baseline regression model, and Model B is a new release candidate. We need to determine if Model B represents a statistically significant improvement over Model A using a paired t-test on their squared errors.

Your task is to write a Go program (`/home/user/evaluate.go`) that performs the following steps:
1. Reads and decompresses all `part-*.csv.gz` files in `/home/user/artifacts/`.
2. Computes the Mean Squared Error for both models (`MSE_A` and `MSE_B`).
3. Computes the difference in squared errors for each prediction: $D_i = (y_{true, i} - y_{pred\_A, i})^2 - (y_{true, i} - y_{pred\_B, i})^2$.
4. Calculates the paired t-statistic for these differences: $t = \frac{\bar{D}}{s_D / \sqrt{N}}$, where $\bar{D}$ is the sample mean of $D$, $s_D$ is the sample standard deviation of $D$ (using $N-1$ degrees of freedom), and $N$ is the total number of records across all files.
5. Determines if Model B is significantly better than Model A. We consider it significant if $t > 1.96$.
6. Writes the results to `/home/user/report.json` with the following exact JSON structure:
```json
{
  "mse_a": 1.2345,
  "mse_b": 1.1234,
  "t_stat": 2.3456,
  "is_significant": true
}
```
(Note: Use standard float serialization for the JSON, precision is fine as long as it's within 1e-4 of the true values).

After writing the Go program, compile and run it to produce `/home/user/report.json`. You may use standard Go libraries only.