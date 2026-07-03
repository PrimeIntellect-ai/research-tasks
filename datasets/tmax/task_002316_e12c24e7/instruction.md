You are tasked with building a data cleaning and analysis script in Rust. A messy tabular dataset of user metrics has been provided, but it contains silent anomalies that often break downstream pipelines or skew results.

The dataset is located at `/home/user/data/users.csv` and contains the following columns:
`user_id` (string), `group` (string: "Control" or "Treatment"), `feature_a` (string/float), `feature_b` (string/float), `feature_c` (string/float).

Your objective is to write a Rust program in `/home/user/cleaner/` that performs the following steps:
1. Parse the CSV file. 
2. Clean the data: Some numerical fields contain anomalies representing missing data: `"NaN"`, `"-9999"`, and empty strings `""`. Identify any row containing at least one of these anomalies in features A, B, or C, and drop the entire row.
3. Compute Group Difference: Calculate the mean of `feature_a` for the "Treatment" group and the "Control" group in the cleaned dataset. Compute the difference: `(Treatment Mean) - (Control Mean)`.
4. Similarity Search: Using the cleaned dataset, compute the Euclidean distance between the user with `user_id` `"U_TARGET"` and all other valid users based on their `feature_a`, `feature_b`, and `feature_c` values. Identify the `user_id`s of the 3 most similar users (those with the smallest Euclidean distance to U_TARGET).

Write your findings to a JSON file at `/home/user/results.json` strictly matching this structure:
```json
{
  "mean_diff": 29.466666666666665,
  "similar_users": ["U_X", "U_Y", "U_Z"]
}
```
*Note: The `mean_diff` should be a standard 64-bit float. The `similar_users` array must contain exactly 3 strings ordered from most similar (smallest distance) to 3rd most similar.*

You may create a new Rust project via `cargo new` and use crates like `csv` and `serde`.