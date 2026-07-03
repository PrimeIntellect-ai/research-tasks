You are an AI assistant helping a Machine Learning Engineer prepare a training pipeline for a Bayesian inference model. 

There is a Rust project located at `/home/user/bayes_pipeline`. This application reads a dataset, enforces a strict numerical schema (all values must be strictly positive), normalizes the features (Z-score normalization), performs a mock Bayesian inference benchmarking step, and logs the output.

However, the ML Engineer noticed a severe flaw: **Data Leakage**. The feature engineering step is calculating the mean and population standard deviation over the *entire* dataset before splitting it into training and testing sets. 

Your task is to:
1. Inspect the Rust source code in `/home/user/bayes_pipeline/src/main.rs`.
2. Fix the data leakage bug. The mean and population standard deviation used to normalize *both* the training and testing sets must be calculated **only** from the training set. The dataset is currently hardcoded as `[10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]` with an 80/20 train/test split (the first 8 elements are the training set).
3. Ensure you do not remove the data schema enforcement checks.
4. Compile and run the project using `cargo run --release`. 

Upon successful execution, the application will automatically generate a file at `/home/user/benchmark_metrics.json`. We will verify your success by checking the normalized values of the test set inside this file.