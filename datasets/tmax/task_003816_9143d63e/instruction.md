You are a performance engineer analyzing the scaling behavior of a newly implemented matrix processing algorithm. You have collected raw observational data from several test runs, located at `/home/user/profiling_data.csv`.

Your task is to reshape this observational data, build a script to validate an analytical complexity model, and output the validation metrics. 

Perform the following steps:
1. Parse the `/home/user/profiling_data.csv` file. The file has columns: `run_id`, `N` (problem size), and `time_ms` (execution time in milliseconds).
2. Reshape and aggregate the data to calculate the **mean** execution time for each unique problem size `N`.
3. Validate the analytical assumption that the algorithm has a strict quadratic time complexity ($O(N^2)$). To do this, fit the theoretical model $Time = c \cdot N^2$ (where $Time$ is the mean execution time, and there is **no y-intercept** term) to your aggregated data using Ordinary Least Squares (OLS).
4. Calculate the constant $c$ and the coefficient of determination ($R^2$) for this model. The $R^2$ should be calculated as $1 - \frac{SS_{res}}{SS_{tot}}$, where $SS_{res}$ is the sum of squared residuals of your model, and $SS_{tot}$ is the total sum of squares around the mean of the aggregated $Time$ values.
5. Create a JSON log file at `/home/user/fit_results.json` containing the results. The file must have exactly this format:
```json
{
  "c": <float_value_rounded_to_6_decimal_places>,
  "r_squared": <float_value_rounded_to_6_decimal_places>
}
```

Write and execute the necessary Python code to complete this analysis.