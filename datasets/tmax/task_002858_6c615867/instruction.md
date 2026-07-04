You are an AI assistant helping a data scientist debug a Rust-based data processing pipeline. 

A data leakage issue has been identified in our feature engineering step. The pipeline script located at `/home/user/etl_pipeline/src/main.rs` processes a dataset of text and numerical values. It computes the vocabulary for Bag-of-Words text encoding and the mean/standard deviation for numerical scaling. 

**The Bug:** Currently, the script computes the vocabulary and the standard scaling statistics (mean and sample standard deviation) over the *entire* dataset before splitting it. This causes information from the test set to leak into the training features.

**Your Task:**
1. Fix the Rust script at `/home/user/etl_pipeline/src/main.rs`.
2. Modify the logic so that the vocabulary and the standard scaling parameters (mean and sample standard deviation, i.e., N-1) are computed **strictly on the training set** (`is_train == "true"`).
3. Apply these training-derived parameters to transform both the train and test sets. Words in the test set that are not in the training vocabulary should be ignored. The vocabulary columns in the output must be sorted alphabetically.
4. Build and run the pipeline using `cargo run` inside `/home/user/etl_pipeline/`.

The pipeline reads `/home/user/etl_pipeline/data.csv` and outputs `output_train.csv` and `output_test.csv`. 

Verify your fix by checking `/home/user/etl_pipeline/output_test.csv`. The automated verification suite will check this file for the correct scaled values and token counts to confirm the data leak is resolved.