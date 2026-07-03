You are a machine learning engineer preparing sensor data for a new model. You have an automated pipeline task to implement in Rust that processes a raw dataset, compares it against a reference (healthy) baseline, performs regression to identify outliers, and logs the analysis in a markdown "notebook" report.

You have two datasets located at:
- `/home/user/data/reference.csv`: A baseline dataset of healthy sensor readings.
- `/home/user/data/raw.csv`: The new training data you just collected, which may contain noise or outliers.

Both CSV files have headers: `time,signal`.

Your objective is to create a Rust project in `/home/user/ml_prep` that does the following:

1. **Probability Distribution Distance & Dataset Comparison**:
   Calculate the 1-Dimensional Wasserstein distance between the `signal` values in `reference.csv` and `raw.csv`.
   *Note on 1D Wasserstein Distance:* For two empirical distributions of equal size, this is calculated by sorting the `signal` arrays of both datasets independently, and then taking the average of the absolute differences between the paired sorted elements.

2. **Curve Fitting and Regression (Outlier Detection)**:
   Perform simple Ordinary Least Squares (OLS) linear regression on `raw.csv` to fit the line `signal = m * time + c`.
   Calculate the residuals for each point in `raw.csv`. The residual is defined as the actual `signal` minus the predicted `signal`.
   Filter out any rows where the absolute value of the residual is strictly greater than `2.0`. 
   Save the filtered dataset to `/home/user/data/cleaned.csv` (maintaining the `time,signal` header).

3. **Workflow Orchestration / Reporting**:
   Your Rust program must orchestrate this workflow and output the final statistics to a markdown file at `/home/user/report.md`.
   The file must contain exactly these lines (replace `<val>` with the computed values formatted to exactly two decimal places, e.g., `1.20`):
   ```markdown
   # Data Preparation Report
   - 1D Wasserstein Distance: <val>
   - Regression Slope (m): <val>
   - Regression Intercept (c): <val>
   - Cleaned Rows Retained: <integer_count>
   ```

Requirements:
- Ensure the Cargo project is successfully compiled and executed. You may use any standard Rust crates (e.g., `csv`, `serde`) but you must configure your `Cargo.toml` appropriately.
- The datasets have exactly the same number of rows. 
- You do not need to build a Jupyter notebook, the `/home/user/report.md` serves as your final pipeline artifact.