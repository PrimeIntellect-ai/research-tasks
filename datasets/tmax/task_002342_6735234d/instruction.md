You are a data analyst working with high-dimensional sensor data. To begin your dimensionality reduction pipeline, you need to write a Rust tool that processes a dataset, computes its covariance matrix, and logs the experiment metadata.

The dataset is located at `/home/user/data.csv`. It contains numerical data with no headers.

Write and execute a Rust program in a new Cargo project located at `/home/user/pca_prep` that does the following:
1. Reads all the numerical data from `/home/user/data.csv`.
2. Loads it into a dense matrix (you may use the `nalgebra` crate).
3. Computes the mean of each column.
4. Centers the data by subtracting the column means from the respective columns.
5. Computes the sample covariance matrix $C = \frac{1}{N-1} X_c^T X_c$, where $X_c$ is the centered data matrix and $N$ is the number of rows.
6. Computes the total variance of the dataset, which is the trace (sum of the main diagonal elements) of the covariance matrix.
7. Generates an experiment tracking log by creating a JSON file at `/home/user/experiment_log.json` with the following exact schema:
```json
{
  "rows": <integer>,
  "cols": <integer>,
  "total_variance": <float_rounded_to_exactly_4_decimal_places>
}
```

Constraints:
- You must use Rust to perform the computation.
- Round `total_variance` to exactly 4 decimal places in the JSON output.
- The CSV file has no headers and is comma-separated. All values can be parsed as `f64`.

Please create the Rust project, write the code, run it, and ensure `/home/user/experiment_log.json` is correctly populated.