You are an AI assistant helping a machine learning engineer prepare training data. 

We have a Rust data preparation tool in `/home/user/ml_prep` that is supposed to join user profiles with their feature vectors, compute a pairwise dot-product similarity matrix for a recommendation system, and save it. Unfortunately, much like a visualization script that produces blank plots due to a misconfigured backend, our tool is producing a matrix full of `NaN`s because it fails to handle missing values properly.

Here is the setup:
1. `/home/user/data/users.csv` contains `user_id,name`.
2. `/home/user/data/features.csv` contains `user_id,f1,f2,f3`. Some feature values are missing (empty strings).
3. The Rust project at `/home/user/ml_prep` reads these files, joins them on `user_id`, and calculates the dot product for every pair of users to create a similarity matrix.
4. Currently, the missing values are being parsed as `NaN` (or causing parsing errors), ruining the output. 

Your task:
1. Modify `/home/user/ml_prep/src/main.rs` to correctly handle missing values in the features. You must impute any missing feature value with `0.0`.
2. Ensure the pairwise dot product matrix is correctly calculated using the imputed values. The matrix should be output to `/home/user/ml_prep/similarity.csv`.
3. The output file `/home/user/ml_prep/similarity.csv` should contain only the numeric matrix (comma-separated), with no headers or row indices. The rows and columns should be ordered by `user_id` in ascending order.
4. Run the Rust project to generate the fixed `similarity.csv` file.

Do not change the directory structure or add new dependencies to `Cargo.toml` unless absolutely necessary (the standard library is sufficient for basic string splitting).