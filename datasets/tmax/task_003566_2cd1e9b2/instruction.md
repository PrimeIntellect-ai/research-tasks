You are an ML Engineer tasked with preparing training data and computing a simple Bayesian prior-posterior update. 

We have two CSV files:
1. `/home/user/features.csv` - Contains `user_id` (integer) and `feature_a` (float).
2. `/home/user/labels.csv` - Contains `user_id` (integer) and `label` (integer, 0 or 1). However, some rows have missing values for `label`.

In data pipelines, a common silent bug occurs when joining data with missing values: integers are coerced into floats so that `NaN` can be used to represent missingness. Downstream probabilistic modeling code that expects strict boolean or integer events often fails or computes incorrect bounds when fed floats.

Your task:
1. Initialize a new Rust binary project at `/home/user/pipeline`.
2. Use the `polars` crate to read and join the two CSV files on `user_id`.
3. Drop any rows where `label` is missing. **Crucially**, ensure the `label` column is strictly typed as an integer (e.g., `i32`) in your final data frame and is never allowed to silently coerce to a floating-point type due to the missing values.
4. Filter the joined, cleaned dataset to keep only rows where `feature_a > 0.5`.
5. Treat `label == 1` as a "success" and `label == 0` as a "failure". 
6. Using a Uniform Beta prior (Beta where alpha=1, beta=1), compute the exact Bayesian posterior parameters for the probability of success given the filtered data.
7. Output the resulting posterior parameters as a JSON file at `/home/user/posterior.json` with the exact format: `{"alpha": <integer>, "beta": <integer>}`.

You must write and run the Rust code to produce this JSON file. You may use any necessary cargo dependencies.