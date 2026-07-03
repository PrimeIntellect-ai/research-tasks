You are a Machine Learning Engineer responsible for preparing training data for a predictive model. Your team uses a custom ETL pipeline written in Rust to perform Bayesian Target Encoding on categorical features. 

The project is located at `/home/user/target_encoder`. It reads a dataset from `/home/user/dataset.csv`, performs Bayesian smoothing on a categorical feature, and splits the data into training and testing sets.

**The Problem:**
A senior data scientist reviewed the pipeline and identified a severe data leakage bug: the pipeline calculates the global target mean and category-specific target means on the *entire* dataset before performing the train/test split. This means information from the test set is leaking into the training features, invalidating the model's evaluation metrics.

**Your Task:**
1. Fix the Rust code in `/home/user/target_encoder/src/main.rs`. 
   - Modify the pipeline so it performs the train/test split *first* (exactly the first 80% of rows for training, the remaining 20% for testing; if the split index is fractional, round down).
   - Calculate the `global_mean` and `category_means` *only* on the training set.
   - Apply the Bayesian target encoding to both the training set and the testing set using the statistics derived *exclusively* from the training set.
   - For unseen categories in the test set, their encoded value should just be the training set's `global_mean`.
   - The smoothing formula used in the code is: `encoded_value = (category_count * category_mean + prior_weight * global_mean) / (category_count + prior_weight)`. The `prior_weight` is heavily hardcoded to `10.0`. Do not change the smoothing formula itself.
2. The program must output two files in `/home/user/`: `train_encoded.csv` and `test_encoded.csv`. The format should be `id,category,target,encoded_feature`.
3. Create a bash script `/home/user/test_repro.sh`. This script must:
   - Compile and run the Rust project.
   - Verify that the `train_encoded.csv` does not suffer from leakage (e.g., by checking the computed values). 
   - Exit with code 0 if successful, or non-zero if the pipeline fails or leaks.

Ensure the final Rust code compiles cleanly with `cargo build`.