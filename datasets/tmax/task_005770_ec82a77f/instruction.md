You are a Machine Learning Engineer tasked with preparing a robust training dataset from raw user interaction logs. You need to enforce data quality, engineer a new feature, balance the dataset using bootstrapping, perform a hypothesis test, and ensure your entire pipeline is strictly reproducible.

Your raw input data is located at `/home/user/raw_data.csv`.
It has the following columns: `user_id`, `session_duration_sec`, `clicks`, `converted`.

Write a data preparation pipeline that does the following:
1. **Schema Enforcement**: Read `/home/user/raw_data.csv`. Keep only valid rows:
   - `user_id` must not be missing (null/empty).
   - `session_duration_sec` must be strictly greater than 0.
   - `clicks` must be greater than or equal to 0.
2. **Feature Engineering**: Create a new column `clicks_per_minute` calculated as `clicks / (session_duration_sec / 60)`.
3. **Bootstrapping (Balancing)**: Separate the valid data into two groups based on the `converted` column (0 and 1). Using a given random seed, sample *with replacement* exactly 500 rows from the `converted=0` group, and exactly 500 rows from the `converted=1` group. Combine these into a single balanced dataset of 1000 rows.
4. **Hypothesis Testing**: On this *balanced* dataset of 1000 rows, perform a standard independent 2-sample t-test (assuming equal variances) comparing the `clicks_per_minute` of the `converted=1` group against the `converted=0` group. 
5. **Outputs**: 
   - Save the balanced dataset to `/home/user/training_data.csv`. It must contain exactly the columns: `user_id`, `session_duration_sec`, `clicks`, `converted`, `clicks_per_minute`.
   - Save the t-test results to `/home/user/stats.json` in the exact format: `{"t_statistic": <float>, "p_value": <float>}`.
6. **Reproducibility**: Create an executable bash script at `/home/user/run.sh` that takes a single integer argument (the random seed) and executes your Python pipeline, applying that seed to all random operations (like pandas `sample()`) to ensure deterministic outputs.

Example usage:
```bash
chmod +x /home/user/run.sh
./run.sh 42
```
After running this command, `/home/user/training_data.csv` and `/home/user/stats.json` must be generated using seed 42. Ensure any Python script you create is properly called by `run.sh` and handles the seed properly.