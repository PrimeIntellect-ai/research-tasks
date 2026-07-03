You are an MLOps engineer debugging a broken data pipeline. A recent pandas update silently introduced NaN values into an experiment artifact dataset, which coerced what should have been strict integer identifiers into floats and empty strings. Downstream Rust-based modeling tools are now crashing.

You need to write a Rust utility that strictly enforces the data schema, performs basic dimensionality reduction, and fits a simple linear regression model on the cleaned data.

Here are your instructions:

1. A raw experiment dataset is located at `/home/user/data/experiment_metrics.csv`.
   It has the following headers: `id,feature_a,feature_b,target`

2. Create a Rust project in `/home/user/schema_enforcer`. You may use standard crates like `csv` and `serde`.

3. Your Rust tool must parse the CSV and strictly enforce this schema:
   - `id`: Must parse successfully as a 32-bit unsigned integer (`u32`).
   - `feature_a`: 64-bit float (`f64`).
   - `feature_b`: 64-bit float (`f64`).
   - `target`: 64-bit float (`f64`).
   *Rule:* Any row that fails to parse into these strict types (e.g., an `id` that is an empty string, or formatted as a float like `4.0`) must be entirely dropped from the dataset. Do not crash; just ignore the malformed rows.

4. Apply dimensionality reduction:
   Combine `feature_a` and `feature_b` into a single 1D feature called `pca_approx` by taking their exact mean:
   `pca_approx = (feature_a + feature_b) / 2.0`

5. Statistical Modeling:
   Using only the valid, parsed rows, perform a Simple Linear Regression (Least Squares) using `pca_approx` as the independent variable ($X$) and `target` as the dependent variable ($Y$).
   Compute the slope ($m$) and intercept ($c$).
   $m = \frac{n(\sum XY) - (\sum X)(\sum Y)}{n(\sum X^2) - (\sum X)^2}$
   $c = \frac{\sum Y - m(\sum X)}{n}$

6. Write the final model parameters to `/home/user/regression_result.json` in the following exact JSON format (round values to 4 decimal places):
   ```json
   {
     "slope": 1.2345,
     "intercept": 6.7890
   }
   ```

Run your Rust tool and ensure the final JSON file is generated successfully.