You are an ML Engineer preparing a dataset for a new model. 

We have a fast Rust-based data cleaning tool located in `/home/user/data_prep`. It processes our raw CSV files before they go into the training pipeline. However, we've encountered a data integrity issue similar to Pandas' classic "silent float conversion" problem. 

Currently, the `clicks` column in our raw data contains some missing (empty) values. To handle this, the Rust tool's author lazily defined the `clicks` column as an `f64` (float) in the struct, which parses blanks as `NaN` or `0.0` and outputs floats (e.g., `15.0`) in the cleaned CSV. Our ML pipeline requires strictly integer types for count features, and missing values must be encoded as `-1`.

Your tasks are:

1. **Fix the Rust Cleaner:**
   - Modify the Rust project in `/home/user/data_prep` to parse the `clicks` column. 
   - Handle missing/empty values by converting them to `-1`.
   - Ensure the output `clicks` column is formatted as strictly integers (e.g., `15`, `-1`, not `15.0`).
   - Build the tool (`cargo build --release`).

2. **Process the Data:**
   - Run your built tool on `/home/user/raw_data.csv`.
   - Save the output to `/home/user/clean_data.csv`.

3. **Experiment Tracking & Hypothesis Testing:**
   - Analyze the `response_time` column of the *cleaned* dataset.
   - Calculate the sample mean and the 95% Confidence Interval (CI) for the mean of `response_time`. Use the standard normal distribution approximation ($Z = 1.96$).
   - Formula for CI: `Mean ± 1.96 * (Standard_Deviation / sqrt(N))`
   - Create an experiment tracking log at `/home/user/experiment.json` containing exactly this JSON structure (rounded to 3 decimal places for floats):
     ```json
     {
       "cleaned_rows": <integer_count_of_data_rows>,
       "mean_response_time": <float>,
       "ci_lower": <float>,
       "ci_upper": <float>
     }
     ```

*Note: You may use bash, python, or rust to calculate the statistics, but the data cleaner must be fixed in Rust. Do not modify the original raw data file.*