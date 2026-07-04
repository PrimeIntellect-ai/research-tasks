You are a Data Scientist tasked with cleaning and analyzing a dirty dataset using Rust.

A raw dataset of sensor readings has been collected and saved at `/home/user/sensor_data.csv`. The dataset contains the following columns: `id,sensor_1,sensor_2,sensor_3,outcome`.

You need to write a standalone Rust program (no external crates allowed, only standard library) that processes this dataset and extracts specific statistical insights.

Perform the following steps in your Rust program:
1. **Outlier Handling**: Read the dataset and drop any rows where `sensor_1` is an outlier. An outlier is defined as strictly greater than `50.0`.
2. **Missing Value Imputation**: The `sensor_2` column has some missing values (represented as empty strings). Calculate the mean of the valid `sensor_2` values *after* the outliers have been removed. Impute the missing values in `sensor_2` with this calculated mean.
3. **Covariance Analysis**: Calculate the population covariance (divide by N, where N is the number of valid rows after outlier removal) between `sensor_1` and the imputed `sensor_2`.
4. **Bayesian Inference**: The `sensor_3` and `outcome` columns are binary (0 or 1). Using the cleaned dataset (post-outlier removal), calculate the conditional probability: P(outcome = 1 | sensor_3 = 1).

Your Rust program should compute these three values and output them to a JSON file located precisely at `/home/user/results.json`.
The format of the JSON must be exactly as follows (use standard f64 formatting, accurate to at least 4 decimal places):
```json
{
  "imputed_mean_sensor_2": <value>,
  "covariance_1_2": <value>,
  "prob_outcome_given_sensor_3": <value>
}
```

Constraints:
- Do not use external crates (e.g., `csv`, `serde`, `serde_json`). Parse the CSV and format the JSON string manually using standard Rust.
- Compile and run your code to generate the file.
- `sensor_1` and `sensor_2` should be parsed as 64-bit floats (`f64`).