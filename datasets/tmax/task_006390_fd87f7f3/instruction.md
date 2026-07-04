You are acting as a Machine Learning Engineer. You have inherited a Rust-based ETL pipeline that prepares data for a similarity search recommendation system. However, the pipeline has a classic data leakage bug: it standardizes the features (Z-score normalization) using the mean and standard deviation of the *entire* dataset before splitting it into training and testing sets.

Your task is to fix this data leak, construct a reproducible pipeline, and track your experiment results.

**Project Setup:**
- A Rust project is located at `/home/user/pipeline/`.
- The input data is at `/home/user/data/interactions.csv` (contains columns: `user_id`, `feature_a`, `feature_b`).
- The current `src/main.rs` reads the CSV, calculates global mean and sample standard deviation (N-1) for `feature_a` and `feature_b`, normalizes the columns, and then splits the data (first 800 rows for training, last 200 for testing).

**Your Objectives:**
1. **Fix the Data Leak:** Modify `/home/user/pipeline/src/main.rs` so that it calculates the sample mean and sample standard deviation (using N-1) for `feature_a` and `feature_b` using *strictly the training set* (the first 800 rows). 
2. **Apply Transformations:** Use the training set statistics to normalize (Z-score: `(value - train_mean) / train_std`) both the training set and the test set.
3. **Statistical Analysis:** Calculate the 95% Confidence Interval for the mean of the *normalized* `feature_a` within the test set. Use the standard normal approximation (Z=1.960). The formula for the margin of error is `1.960 * (test_sample_std / sqrt(test_n))`, where `test_sample_std` is the sample standard deviation of the *normalized* test set `feature_a`.
4. **Outputs:**
   - Write the corrected, normalized test set to `/home/user/test_features_corrected.csv` (Headers: `user_id,feature_a_norm,feature_b_norm`).
   - Create an experiment tracking log at `/home/user/experiment_log.json` strictly matching this structure:
     ```json
     {
       "train_feature_a_mean": 0.0,
       "train_feature_a_std": 0.0,
       "test_normalized_feature_a_mean": 0.0,
       "test_normalized_feature_a_ci_lower": 0.0,
       "test_normalized_feature_a_ci_upper": 0.0
     }
     ```
     *(Round all JSON floats to 4 decimal places).*

Recompile and run your Rust pipeline to generate the required output files. You may add standard Rust crates to `Cargo.toml` if needed (e.g., `csv`, `serde`).