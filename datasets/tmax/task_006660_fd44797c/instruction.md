You are an ML Engineer preparing training data for a customer behavior model. You need to combine user profile data with event logs, handle missing values and outliers, compute a composite feature using linear algebra, and log your preprocessing metrics.

You are given two files:
1. `/home/user/users.csv`: Contains `user_id` and `account_tier` (integer).
2. `/home/user/events.csv`: Contains `user_id`, `event_count` (float), and `event_value` (float).

Write and execute a Python script to perform the following exact pipeline:

1. **Multi-source Data Joining:** 
   Perform a Full Outer Join on `user_id` between the two datasets. 

2. **Missing Value Handling & Type Fixing:**
   Because of the outer join, some rows will have missing values.
   - Drop any rows where `account_tier` is missing.
   - Fill any missing values in `event_count` and `event_value` with `0.0`.
   - Ensure the `account_tier` column is cast back to a standard integer type (`int64` or `int32`). It must not remain a float.

3. **Linear Algebra Feature Creation:**
   Compute a new column named `activity_index`. For each user, this should be the dot product of their `[event_count, event_value]` vector with the weight vector `[0.4, 0.6]`.

4. **Outlier Handling:**
   Identify outliers where `activity_index` is strictly greater than `50.0`. Cap these outlier values at exactly `50.0` in the `activity_index` column.

5. **Experiment Tracking:**
   Log your preprocessing metrics to `/home/user/metrics.json`. The JSON file must contain exactly these keys:
   - `"total_rows_after_join"`: The number of rows immediately after the outer join.
   - `"rows_dropped"`: The number of rows dropped because of missing `account_tier`.
   - `"outliers_capped"`: The number of rows (after dropping missing tiers) whose `activity_index` was capped.

6. **Save Output:**
   Save the final dataset to `/home/user/clean_data.parquet` (without the dataframe index). The saved parquet schema must have `account_tier` as an integer type, not a float.

Ensure all file paths are strictly respected.