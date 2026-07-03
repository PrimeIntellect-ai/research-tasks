You are a data analyst working on a Rust-based machine learning pipeline. 

There is a Rust project located at `/home/user/pipeline` which reads a tabular dataset from `/home/user/data.csv`. The dataset has three columns: `f1`, `f2`, and `label`. There are exactly 1000 rows of data (excluding the header).

Currently, the pipeline performs a simple scaling and dimensionality reduction step to project `f1` and `f2` into a single feature `reduced_f`. It then splits the data into a training set (first 800 rows) and a test set (last 200 rows).

However, there is a data leakage bug! The pipeline computes the mean and standard deviation for scaling using the *entire* dataset before splitting it. This means information from the test set leaks into the training set's transformation.

Your task is to fix this data leakage:
1. Modify `/home/user/pipeline/src/main.rs` so that the data is split into train (first 800 rows) and test (last 200 rows) *before* any statistics are computed.
2. Compute the mean and standard deviation for `f1` and `f2` using **only** the 800 training rows. Use the sample standard deviation (divide by N-1, where N=800).
3. Apply these training statistics to scale both the training and test sets.
4. Perform the dimensionality reduction on the test set: `reduced_f = (f1_scaled + f2_scaled) / 2.0`.
5. Ensure the program writes the transformed test set to `/home/user/test_transformed.csv`. The output CSV must have a header `reduced_f,label` and contain exactly the 200 test rows, formatted to 4 decimal places for `reduced_f`.
6. To benchmark inference performance, ensure the program measures the time taken to transform the 200 test rows and prints it. You don't need to save the timing to a file, just output it to stdout.

Compile and run the fixed Rust pipeline. The success of the task will be evaluated by verifying the exact numerical values in `/home/user/test_transformed.csv`.