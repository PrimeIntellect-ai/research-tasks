You are a data engineer debugging an ETL pipeline. A recent bug in a pandas-based ingestion service has been silently corrupting our integer columns by occasionally introducing `NaN` values or coercing integers into floats (e.g., `42.0` instead of `42`). 

You need to write a custom audit tool in **Go** to analyze a simulated large-scale data dump and quantify the extent of the corruption.

The dataset is located at `/home/user/etl_dump.csv`. It has a header and two columns: `record_id` (integer) and `value` (string representing the data).

A row is considered **corrupt** if the `value` field contains a decimal point (`.`) or is exactly the string `"NaN"`. Otherwise, it is considered clean (valid integer).

Your task is to create a Go program `/home/user/audit.go` that reads this file and performs the following analysis:
1. **Count Metrics:** Determine the total number of rows (excluding the header) and the exact number of corrupt rows.
2. **Bayesian Inference:** We want to model the probability of corruption. Assuming a conjugate Beta-Binomial model with a flat prior of Beta(1, 1), calculate the expected value (mean) of the posterior distribution for the corruption probability given the observed data.
3. **Covariance Analysis:** To understand if the corruption is data-drift related (occurring later in the dataset), calculate the **sample covariance** (using `n-1` degrees of freedom) between the `record_id` (X) and a binary corruption indicator (Y, where 1.0 = corrupt, 0.0 = clean). 

Your Go program must output these experiment tracking metrics as a JSON file at `/home/user/audit_results.json` with the exact following structure:
```json
{
  "total_rows": <int>,
  "corrupt_rows": <int>,
  "posterior_mean": <float64>,
  "covariance": <float64>
}
```

Constraints:
- You must use Go to perform the analysis. 
- You can format the floats in the JSON with standard precision (e.g., using `encoding/json` standard marshaling).
- Do not use any external Go libraries outside the standard library.

Once the program is written, execute it to generate the JSON report.